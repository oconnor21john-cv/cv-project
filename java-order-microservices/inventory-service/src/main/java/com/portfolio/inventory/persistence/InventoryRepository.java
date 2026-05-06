package com.portfolio.inventory.persistence;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import jakarta.persistence.LockModeType;

public interface InventoryRepository extends JpaRepository<InventoryEntity, String> {
	@Lock(LockModeType.PESSIMISTIC_WRITE)
	@Query("select i from InventoryEntity i where i.sku = :sku")
	Optional<InventoryEntity> findBySkuForUpdate(@Param("sku") String sku);

	/**
	 * Find all inventory records by SKU list.
	 * Used to fetch current stock levels for display.
	 */
	List<InventoryEntity> findBySkuIn(List<String> skus);
}

