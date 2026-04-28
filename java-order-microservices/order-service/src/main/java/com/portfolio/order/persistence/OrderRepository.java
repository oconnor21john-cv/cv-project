package com.portfolio.order.persistence;

import java.util.List;
import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface OrderRepository extends JpaRepository<OrderEntity, UUID> {

	@Modifying
	@Query(value = "DELETE FROM orders WHERE created_by = :username", nativeQuery = true)
	void deleteByCreatedBy(@Param("username") String username);

	@Query("SELECT DISTINCT o FROM OrderEntity o LEFT JOIN FETCH o.items WHERE o.createdBy = :createdBy ORDER BY o.createdAt DESC")
	List<OrderEntity> findByCreatedByOrderByCreatedAtDesc(String createdBy);

	@Query("SELECT DISTINCT o FROM OrderEntity o LEFT JOIN FETCH o.items ORDER BY o.createdAt DESC")
	List<OrderEntity> findAllByOrderByCreatedAtDesc();
}
