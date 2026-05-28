package com.portfolio.order.messaging;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.SendMessageRequest;

/**
 * Publishes serialized event payloads to AWS SQS.
 * Used by OrderOutboxPoller to drain outbox events to SQS.
 *
 * When app.sqs.enabled=false (default for local dev), this is a no-op —
 * the outbox row simply gets marked sent without an actual network call,
 * which keeps the local Docker stack working without AWS credentials.
 */
@Component
public class SqsEventPublisher {
	private final boolean enabled;
	private final ObjectMapper objectMapper;
	private final SqsClient sqsClient;

	public SqsEventPublisher(
			ObjectMapper objectMapper,
			@Value("${app.sqs.enabled:false}") boolean enabled,
			@Value("${AWS_REGION:eu-west-2}") String awsRegion
	) {
		this.enabled = enabled;
		this.objectMapper = objectMapper;
		this.sqsClient = enabled
				? SqsClient.builder().region(Region.of(awsRegion)).build()
				: null;
	}

	public void publish(String queueUrl, Object payload) {
		if (!enabled || queueUrl == null || queueUrl.isBlank()) {
			return;
		}

		try {
			var body = objectMapper.writeValueAsString(payload);
			sqsClient.sendMessage(SendMessageRequest.builder()
					.queueUrl(queueUrl)
					.messageBody(body)
					.build());
		} catch (JsonProcessingException ex) {
			throw new IllegalStateException("Failed to serialize event payload", ex);
		}
	}
}
