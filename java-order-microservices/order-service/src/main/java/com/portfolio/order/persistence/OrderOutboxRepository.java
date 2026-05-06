package com.portfolio.order.persistence;

import java.util.List;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface OrderOutboxRepository extends JpaRepository<OrderOutboxEntity, UUID> {
	/**
	 * Find all unsent outbox events ordered by creation time.
	 * Used by the scheduled poller to drain events to SQS.
	 */
	@Query("SELECT o FROM OrderOutboxEntity o WHERE o.sent = false ORDER BY o.createdAt ASC")
	List<OrderOutboxEntity> findUnsentEvents();
}
