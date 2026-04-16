package com.minimarket.backend_api.dto;

// Usando Record para simplificar (Java 17+)
public record EventoDTO(String personId, String action, String location) {
}
