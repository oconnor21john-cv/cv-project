package com.portfolio.order.api;

import java.util.UUID;

public class OrderAccessDeniedException extends RuntimeException {
    public OrderAccessDeniedException(UUID orderId) {
        super("You do not have permission to modify order: " + orderId);
    }
}
