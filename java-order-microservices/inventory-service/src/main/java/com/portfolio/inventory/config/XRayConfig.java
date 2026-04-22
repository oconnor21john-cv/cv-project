package com.portfolio.inventory.config;

import com.amazonaws.xray.AWSXRay;
import com.amazonaws.xray.AWSXRayRecorderBuilder;
import jakarta.annotation.PostConstruct;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Configuration
@Profile("aws")
public class XRayConfig {
	@PostConstruct
	void initXRay() {
		AWSXRayRecorderBuilder builder = AWSXRayRecorderBuilder.standard()
				.withDefaultPlugins();
		AWSXRay.setGlobalRecorder(builder.build());
	}
}
