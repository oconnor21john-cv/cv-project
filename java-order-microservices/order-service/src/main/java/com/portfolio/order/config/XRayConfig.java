package com.portfolio.order.config;

import com.amazonaws.xray.AWSXRay;
import com.amazonaws.xray.AWSXRayRecorderBuilder;
import jakarta.servlet.Filter;
import com.amazonaws.xray.javax.servlet.AWSXRayServletFilter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Configuration
@Profile("aws")
public class XRayConfig {
	static {
		AWSXRayRecorderBuilder builder = AWSXRayRecorderBuilder.standard()
				.withDefaultPlugins();
		AWSXRay.setGlobalRecorder(builder.build());
	}

	@Bean
	public Filter tracingFilter() {
		return new AWSXRayServletFilter("order-service");
	}
}
