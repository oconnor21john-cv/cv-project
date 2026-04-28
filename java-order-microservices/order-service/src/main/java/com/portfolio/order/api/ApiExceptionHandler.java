package com.portfolio.order.api;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiExceptionHandler {
	@ExceptionHandler(IllegalArgumentException.class)
	@ResponseStatus(HttpStatus.NOT_FOUND)
	public ProblemDetail notFound(IllegalArgumentException ex) {
		var pd = ProblemDetail.forStatus(HttpStatus.NOT_FOUND);
		pd.setDetail(ex.getMessage());
		return pd;
	}

	@ExceptionHandler(IllegalStateException.class)
	@ResponseStatus(HttpStatus.CONFLICT)
	public ProblemDetail conflict(IllegalStateException ex) {
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
	@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
	public ProblemDetail catchAll(Exception ex) {
		var pd = ProblemDetail.forStatus(HttpStatus.INTERNAL_SERVER_ERROR);
		pd.setDetail("An unexpected error occurred");
		return pd;
	}
}

