package com.portfolio.order.api;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.annotation.AnnotationUtils;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiExceptionHandler {
	private static final Logger log = LoggerFactory.getLogger(ApiExceptionHandler.class);
	@ExceptionHandler(OrderNotFoundException.class)
	@ResponseStatus(HttpStatus.NOT_FOUND)
	public ProblemDetail notFound(OrderNotFoundException ex) {
		var pd = ProblemDetail.forStatus(HttpStatus.NOT_FOUND);
		pd.setDetail(ex.getMessage());
		return pd;
	}

	@ExceptionHandler(OrderAccessDeniedException.class)
	@ResponseStatus(HttpStatus.FORBIDDEN)
	public ProblemDetail forbidden(OrderAccessDeniedException ex) {
		var pd = ProblemDetail.forStatus(HttpStatus.FORBIDDEN);
		pd.setDetail(ex.getMessage());
		return pd;
	}

	@ExceptionHandler(OrderStateConflictException.class)
	@ResponseStatus(HttpStatus.CONFLICT)
	public ProblemDetail stateConflict(OrderStateConflictException ex) {
		var pd = ProblemDetail.forStatus(HttpStatus.CONFLICT);
		pd.setDetail(ex.getMessage());
		return pd;
	}

	@ExceptionHandler(MethodArgumentNotValidException.class)
	@ResponseStatus(HttpStatus.BAD_REQUEST)
	public ProblemDetail validation(MethodArgumentNotValidException ex) {
		var pd = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
		pd.setDetail("Validation error");
		return pd;
	}

	@ExceptionHandler(Exception.class)
	public ProblemDetail catchAll(Exception ex) {
		// Honour @ResponseStatus on the thrown exception (e.g. InvalidCredentialsException → 401)
		// rather than blanket-converting everything to 500.
		var responseStatus = AnnotationUtils.findAnnotation(ex.getClass(), ResponseStatus.class);
		if (responseStatus != null) {
			var status = responseStatus.value();
			log.warn("Handled exception with @ResponseStatus: status={}, type={}, message={}",
					status, ex.getClass().getSimpleName(), ex.getMessage());
			var pd = ProblemDetail.forStatus(status);
			pd.setDetail(ex.getMessage() != null ? ex.getMessage() : status.getReasonPhrase());
			return pd;
		}
		// Truly unexpected — log the full stack trace so it never disappears silently.
		log.error("Unhandled exception", ex);
		var pd = ProblemDetail.forStatus(HttpStatus.INTERNAL_SERVER_ERROR);
		pd.setDetail("An unexpected error occurred");
		return pd;
	}
}

