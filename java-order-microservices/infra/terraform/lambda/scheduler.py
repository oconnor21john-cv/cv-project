"""
Sleep / wake scheduler for the cost-optimised stack.

Triggered by two EventBridge Scheduler rules:
  * "sleep" event: scales every ECS service to 0 and stops the RDS instance.
  * "wake"  event: starts RDS and scales every service back to its desired count.

Service desired-count for wake is read from the SERVICES env var.
"""

import json
import logging
import os
import time

import boto3
from botocore.exceptions import ClientError

log = logging.getLogger()
log.setLevel(logging.INFO)

ecs = boto3.client("ecs")
rds = boto3.client("rds")

CLUSTER = os.environ["ECS_CLUSTER"]
DB_INSTANCE = os.environ["DB_INSTANCE_IDENTIFIER"]
# {"order-service": 1, "inventory-service": 1, "payment-service": 1}
SERVICES = json.loads(os.environ["SERVICES"])


def _scale(desired: int) -> None:
    for service, _ in SERVICES.items():
        target = SERVICES[service] if desired != 0 else 0
        log.info("ECS %s/%s -> desired_count=%s", CLUSTER, service, target)
        ecs.update_service(
            cluster=CLUSTER,
            service=service,
            desiredCount=target,
        )


def _stop_db() -> None:
    try:
        rds.stop_db_instance(DBInstanceIdentifier=DB_INSTANCE)
        log.info("RDS %s stop requested", DB_INSTANCE)
    except ClientError as err:
        code = err.response.get("Error", {}).get("Code", "")
        if code in {"InvalidDBInstanceState", "DBInstanceNotFound"}:
            log.info("RDS %s already stopped or missing (%s)", DB_INSTANCE, code)
        else:
            raise


def _start_db() -> None:
    try:
        rds.start_db_instance(DBInstanceIdentifier=DB_INSTANCE)
        log.info("RDS %s start requested", DB_INSTANCE)
    except ClientError as err:
        code = err.response.get("Error", {}).get("Code", "")
        if code in {"InvalidDBInstanceState", "DBInstanceNotFound"}:
            log.info("RDS %s already running or missing (%s)", DB_INSTANCE, code)
        else:
            raise


def handler(event, context):
    action = (event or {}).get("action", "sleep")
    log.info("scheduler action=%s event=%s", action, event)

    if action == "sleep":
        _scale(0)
        # Give ECS a beat to drain before stopping the DB.
        time.sleep(5)
        _stop_db()
        return {"status": "sleeping"}

    if action == "wake":
        _start_db()
        _scale(1)
        return {"status": "waking"}

    raise ValueError(f"Unknown action: {action!r}")
