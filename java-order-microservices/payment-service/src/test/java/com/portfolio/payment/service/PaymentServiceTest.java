package com.portfolio.payment.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.math.BigDecimal;
import java.util.Optional;
import java.util.UUID;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.portfolio.payment.domain.PaymentStatus;
import com.portfolio.payment.messaging.SqsEventPublisher;
import com.portfolio.payment.persistence.PaymentEntity;
import com.portfolio.payment.persistence.PaymentRepository;

@ExtendWith(MockitoExtension.class)
class PaymentServiceTest {

    @Mock private PaymentRepository paymentRepository;
    @Mock private SqsEventPublisher sqsEventPublisher;

    private PaymentService service;

    @BeforeEach
    void setUp() {
        service = new PaymentService(paymentRepository, sqsEventPublisher, "");
    }

    @Nested
    @DisplayName("createOrGet()")
    class CreateOrGet {

        @Test
        @DisplayName("succeeds for amounts within the threshold")
        void happyPath() {
            var orderId = UUID.randomUUID();
            var amount = new BigDecimal("99.99");

            when(paymentRepository.findByOrderId(orderId)).thenReturn(Optional.empty());

            var result = service.createOrGet(orderId, amount);

            assertThat(result.succeeded()).isTrue();
            assertThat(result.message()).isEqualTo("Payment succeeded");

            var captor = ArgumentCaptor.forClass(PaymentEntity.class);
            verify(paymentRepository).save(captor.capture());
            assertThat(captor.getValue().getStatus()).isEqualTo(PaymentStatus.SUCCEEDED);
            assertThat(captor.getValue().getAmount()).isEqualByComparingTo(amount);
        }

        @Test
        @DisplayName("declines amounts exceeding 1000.00")
        void declinedHighAmount() {
            var orderId = UUID.randomUUID();
            var amount = new BigDecimal("1500.00");

            when(paymentRepository.findByOrderId(orderId)).thenReturn(Optional.empty());

            var result = service.createOrGet(orderId, amount);

            assertThat(result.succeeded()).isFalse();
            assertThat(result.message()).contains("decline");

            var captor = ArgumentCaptor.forClass(PaymentEntity.class);
            verify(paymentRepository).save(captor.capture());
            assertThat(captor.getValue().getStatus()).isEqualTo(PaymentStatus.FAILED);
        }

        @Test
        @DisplayName("boundary: exactly 1000.00 succeeds")
        void boundaryExact() {
            var orderId = UUID.randomUUID();
            var amount = new BigDecimal("1000.00");

            when(paymentRepository.findByOrderId(orderId)).thenReturn(Optional.empty());

            var result = service.createOrGet(orderId, amount);

            assertThat(result.succeeded()).isTrue();
        }

        @Test
        @DisplayName("boundary: 1000.01 is declined")
        void boundaryJustOver() {
            var orderId = UUID.randomUUID();
            var amount = new BigDecimal("1000.01");

            when(paymentRepository.findByOrderId(orderId)).thenReturn(Optional.empty());

            var result = service.createOrGet(orderId, amount);

            assertThat(result.succeeded()).isFalse();
        }

        @Test
        @DisplayName("returns idempotent response for already-succeeded payment")
        void idempotentSucceeded() {
            var orderId = UUID.randomUUID();
            var existing = new PaymentEntity(orderId, new BigDecimal("50.00"), PaymentStatus.SUCCEEDED);

            when(paymentRepository.findByOrderId(orderId)).thenReturn(Optional.of(existing));

            var result = service.createOrGet(orderId, new BigDecimal("50.00"));

            assertThat(result.succeeded()).isTrue();
            assertThat(result.message()).isEqualTo("Already paid");
            verify(paymentRepository, never()).save(any());
        }

        @Test
        @DisplayName("returns idempotent response for already-failed payment")
        void idempotentFailed() {
            var orderId = UUID.randomUUID();
            var existing = new PaymentEntity(orderId, new BigDecimal("2000.00"), PaymentStatus.FAILED);

            when(paymentRepository.findByOrderId(orderId)).thenReturn(Optional.of(existing));

            var result = service.createOrGet(orderId, new BigDecimal("2000.00"));

            assertThat(result.succeeded()).isFalse();
            assertThat(result.message()).isEqualTo("Already failed");
            verify(paymentRepository, never()).save(any());
        }
    }
}
