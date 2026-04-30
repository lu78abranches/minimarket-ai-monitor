package com.minimarket.backend_api.controller;

import com.minimarket.backend_api.service.AuditoriaService;
import com.minimarket.backend_api.repository.EventoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;
import java.util.stream.Collectors;

@Controller // Note que é @Controller, não @RestController
public class DashboardController {

    @Autowired
    private EventoRepository repository;

    @Autowired
    private AuditoriaService auditoriaService;

    @GetMapping("/dashboard")
    public String exibirDashboard(Model model) {
        // Busca todos os IDs únicos que passaram pela loja
        List<String> idsUnicos = repository.findAll().stream()
                .map(e -> e.getPersonId())
                .distinct()
                .collect(Collectors.toList());

        // Gera um relatório para cada ID
        var relatorios = idsUnicos.stream()
                .map(id -> auditoriaService.gerarRelatorioCliente(id))
                .collect(Collectors.toList());

        model.addAttribute("relatorios", relatorios);
        return "dashboard"; // Nome do arquivo HTML em /templates
    }
}

