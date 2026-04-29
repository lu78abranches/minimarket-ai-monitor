package com.minimarket.backend_api.dto;

import java.util.List;

public record JornadaClienteDTO(
        String personId,
        String tempoPermanencia,
        List<String> locaisVisitados,
        String statusAuditoria) {
}
