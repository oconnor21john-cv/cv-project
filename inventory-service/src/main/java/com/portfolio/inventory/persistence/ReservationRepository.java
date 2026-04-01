package com.portfolio.inventory.persistence;

import java.util.Optional;
import java.util.UUID;

import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ReservationRepository extends JpaRepository<ReservationEntity, UUID> {
	@EntityGraph(attributePaths = "items")
	Optional<ReservationEntity> findWithItemsByOrderId(UUID orderId);
}

