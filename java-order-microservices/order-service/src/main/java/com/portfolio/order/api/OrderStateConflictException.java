package com.portfolio.order.api;

import java.util.UUID;

import com.portfolio.order.domain.OrderStatus;

/**
 * Thrown when an operation cannot be performed due to the order being in an invalid state.
 * For example: attempting to cancel an order that is already cancelled.
 */
public class OrderStateConflictException extends RuntimeException {
	public OrderStateConflictException(UUID orderId, OrderStatus currentStatus, String operation) {
		super("Cannot " + operation + " order " + orderId + ": order is in status " + currentStatus);
	}

	public OrderStateConflictException(String message) {
		super(message);
	}
}
