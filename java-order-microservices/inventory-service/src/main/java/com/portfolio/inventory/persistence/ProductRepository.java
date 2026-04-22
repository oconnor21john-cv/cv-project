package com.portfolio.inventory.persistence;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductRepository extends JpaRepository<ProductEntity, String> {
	List<ProductEntity> findBySkuIn(List<String> skus);
}
