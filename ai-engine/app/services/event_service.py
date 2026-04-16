import requests
import datetime

class EventService:
    def __init__(self, backend_url="http://localhost:8082/api/events"):
        self.backend_url = backend_url

    def send_event(self, person_id, action):
        payload = {
            "personId": person_id,
            "action": action, # 'ENTER', 'EXIT' ou 'FRIDGE_INTERACTION'
            "timestamp": datetime.datetime.now().isoformat(),
            "location": "MAIN_ENTRANCE"
        }
        
        try:
            # Envio real para o Backend Spring Boot
            response = requests.post(self.backend_url, json=payload, timeout=2.0)
            
            if response.status_code == 201:
                print(f"[SUCESSO] Evento persistido no MySQL via Spring. Status: {response.status_code}")
            else:
                print(f"[AVISO] Spring recebeu, mas retornou status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"[ERRO] O Spring Boot não parece estar rodando na porta 8082.")
        except Exception as e:
            print(f"[ERRO REDE] Falha ao conectar com o Backend: {e}")


