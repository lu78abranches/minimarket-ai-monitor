package com.minimarket.backend_api.repository;

import com.minimarket.backend_api.model.Evento;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest // Configura um banco em memória para testar apenas a camada de persistência
public class EventoRepositoryTest {

    @Autowired
    private EventoRepository repository;

    @Test
    public void deveSalvarEventoComSucesso() {
        // Arrange
        Evento evento = new Evento();
        evento.setPersonId("10");
        evento.setAction("ENTER");
        evento.setLocation("GELADEIRA_01");

        // Act
        Evento salvo = repository.save(evento);

        // Assert
        assertThat(salvo.getId()).isNotNull();
        assertThat(salvo.getPersonId()).isEqualTo("10");
    }
}
