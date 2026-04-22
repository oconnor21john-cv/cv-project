package com.portfolio.inventory.messaging;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.SendMessageRequest;

@Component
public class SqsEventPublisher {
	private final boolean enabled;
	private final ObjectMapper objectMapper;
	private final SqsClient sqsClient;

	public SqsEventPublisher(
			ObjectMapper objectMapper,
			@Value("${app.sqs.enabled:false}") boolean enabled,
			@Value("${AWS_REGION:eu-west-2}") String awsRegion
	) {
		this.enabled = enabled;
		this.objectMapper = objectMapper;
		this.sqsClient = enabled
				? SqsClient.builder().region(Region.of(awsRegion)).build()
				: null;
	}

	public void publish(String queueUrl, Object payload) {
		if (!enabled || queueUrl == null || queueUrl.isBlank()) {
			return;
		}

		try {
			var body = objectMapper.writeValueAsString(payload);
			sqsClient.sendMessage(SendMessageRequest.builder()
					.queueUrl(queueUrl)
					.messageBody(body)
					.build());
		} catch (JsonProcessingException ex) {
			throw new IllegalStateException("Failed to serialize event payload", ex);
		}
	}
}
