package com.portfolio.order.persistence;

import java.util.List;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<OrderEntity, UUID> {
	List<OrderEntity> findByCreatedByOrderByCreatedAtDesc(String createdBy);
	List<OrderEntity> findAllByOrderByCreatedAtDesc();
}
