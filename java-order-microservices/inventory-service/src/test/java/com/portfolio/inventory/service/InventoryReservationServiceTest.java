package com.portfolio.inventory.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.List;
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

import com.portfolio.inventory.api.ReserveStockRequest;
import com.portfolio.inventory.api.ReserveStockRequestItem;
import com.portfolio.inventory.domain.ReservationStatus;
import com.portfolio.inventory.messaging.SqsEventPublisher;
import com.portfolio.inventory.persistence.InventoryEntity;
import com.portfolio.inventory.persistence.InventoryRepository;
import com.portfolio.inventory.persistence.ReservationEntity;
import com.portfolio.inventory.persistence.ReservationRepository;

@ExtendWith(MockitoExtension.class)
class InventoryReservationServiceTest {

    @Mock private InventoryRepository inventoryRepository;
    @Mock private ReservationRepository reservationRepository;
    @Mock private SqsEventPublisher sqsEventPublisher;

    private InventoryReservationService service;

    @BeforeEach
    void setUp() {
        service = new InventoryReservationService(
                inventoryRepository, reservationRepository, sqsEventPublisher, "");
    }

    @Nested
    @DisplayName("reserve()")
    class Reserve {

        @Test
        @DisplayName("reserves stock when sufficient inventory exists")
        void happyPath() {
            var orderId = UUID.randomUUID();
            var request = new ReserveStockRequest(orderId,
                    List.of(new ReserveStockRequestItem("SKU-APPLE", 3)));
            var inventory = new InventoryEntity("SKU-APPLE", 100, 0);

            when(reservationRepository.findWithItemsByOrderId(orderId)).thenReturn(Optional.empty());
            when(inventoryRepository.findBySkuForUpdate("SKU-APPLE")).thenReturn(Optional.of(inventory));

            var result = service.reserve(request);

            assertThat(result.reserved()).isTrue();
            assertThat(result.message()).isEqualTo("Reserved");
            assertThat(inventory.getReserved()).isEqualTo(3);
            verify(reservationRepository).save(any(ReservationEntity.class));
        }

        @Test
        @DisplayName("returns idempotent response when already reserved")
        void idempotent() {
            var orderId = UUID.randomUUID();
            var request = new ReserveStockRequest(orderId,
                    List.of(new ReserveStockRequestItem("SKU-APPLE", 1)));
            var existing = new ReservationEntity(orderId, ReservationStatus.RESERVED);

            when(reservationRepository.findWithItemsByOrderId(orderId)).thenReturn(Optional.of(existing));

            var result = service.reserve(request);

            assertThat(result.reserved()).isTrue();
            assertThat(result.message()).isEqualTo("Already reserved");
            verify(inventoryRepository, never()).findBySkuForUpdate(anyString());
        }

        @Test
        @DisplayName("fails when SKU does not exist")
        void unknownSku() {
            var orderId = UUID.randomUUID();
            var request = new ReserveStockRequest(orderId,
                    List.of(new ReserveStockRequestItem("SKU-UNKNOWN", 1)));

            when(reservationRepository.findWithItemsByOrderId(orderId)).thenReturn(Optional.empty());
            when(inventoryRepository.findBySkuForUpdate("SKU-UNKNOWN")).thenReturn(Optional.empty());

            var result = service.reserve(request);

            assertThat(result.reserved()).isFalse();
            assertThat(result.message()).contains("Unknown SKU");
        }

        @Test
        @DisplayName("fails when insufficient stock available")
        void insufficientStock() {
            var orderId = UUID.randomUUID();
            var request = new ReserveStockRequest(orderId,
                    List.of(new ReserveStockRequestItem("SKU-APPLE", 50)));
            var inventory = new InventoryEntity("SKU-APPLE", 10, 5);

            when(reservationRepository.findWithItemsByOrderId(orderId)).thenReturn(Optional.empty());
            when(inventoryRepository.findBySkuForUpdate("SKU-APPLE")).thenReturn(Optional.of(inventory));

            var result = service.reserve(request);

            assertThat(result.reserved()).isFalse();
            assertThat(result.message()).contains("Insufficient stock");
        }

        @Test
        @DisplayName("reserves multiple SKUs atomically")
        void multipleSkus() {
            var orderId = UUID.randomUUID();
            var request = new ReserveStockRequest(orderId, List.of(
                    new ReserveStockRequestItem("SKU-APPLE", 2),
                    new ReserveStockRequestItem("SKU-BANANA", 5)
            ));
            var apple = new InventoryEntity("SKU-APPLE", 100, 0);
            var banana = new InventoryEntity("SKU-BANANA", 100, 0);

            when(reservationRepository.findWithItemsByOrderId(orderId)).thenReturn(Optional.empty());
            when(inventoryRepository.findBySkuForUpdate("SKU-APPLE")).thenReturn(Optional.of(apple));
            when(inventoryRepository.findBySkuForUpdate("SKU-BANANA")).thenReturn(Optional.of(banana));

            var result = service.reserve(request);

            assertThat(result.reserved()).isTrue();
            assertThat(apple.getReserved()).isEqualTo(2);
            assertThat(banana.getReserved()).isEqualTo(5);
        }
    }

    @Nested
    @DisplayName("release()")
    class Release {

        @Test
        @DisplayName("releases reserved stock and updates status")
        void happyPath() {
            var orderId = UUID.randomUUID();
            var reservation = new ReservationEntity(orderId, ReservationStatus.RESERVED);
            reservation.addItem("SKU-APPLE", 3);
            var inventory = new InventoryEntity("SKU-APPLE", 100, 10);

            when(reservationRepository.findWithItemsByOrderId(orderId)).thenReturn(Optional.of(reservation));
            when(inventoryRepository.findBySkuForUpdate("SKU-APPLE")).thenReturn(Optional.of(inventory));

            var result = service.release(orderId);

            assertThat(result.reserved()).isTrue();
            assertThat(result.message()).isEqualTo("Released");
            assertThat(reservation.getStatus()).isEqualTo(ReservationStatus.RELEASED);
            assertThat(inventory.getReserved()).isEqualTo(7);
        }

        @Test
        @DisplayName("no-op when no reservation found")
        void noReservation() {
            var orderId = UUID.randomUUID();
            when(reservationRepository.findWithItemsByOrderId(orderId)).thenReturn(Optional.empty());

            var result = service.release(orderId);

            assertThat(result.message()).contains("noop");
        }

        @Test
        @DisplayName("no-op when reservation is not in RESERVED state")
        void alreadyReleased() {
            var orderId = UUID.randomUUID();
            var reservation = new ReservationEntity(orderId, ReservationStatus.RELEASED);

            when(reservationRepository.findWithItemsByOrderId(orderId)).thenReturn(Optional.of(reservation));

            var result = service.release(orderId);

            assertThat(result.message()).contains("noop");
            verify(inventoryRepository, never()).findBySkuForUpdate(anyString());
        }
    }
}
