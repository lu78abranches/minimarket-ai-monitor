import requests
import datetime

class EventService:
    def __init__(self, backend_url="http://localhost:8080/api/events"):
        self.backend_url = backend_url

    def send_event(self, person_id, action):
        payload = {
            "personId": person_id,
            "action": action, # 'ENTER' ou 'EXIT'
            "timestamp": datetime.datetime.now().isoformat(),
            "location": "MAIN_ENTRANCE"
        }
        try:
            # Por enquanto vai falhar porque o Spring não subiu, 
            # então usamos um print de log
            print(f"[EVENTO] Enviando: {payload}")
            # response = requests.post(self.backend_url, json=payload, timeout=0.5)
        except Exception as e:
            print(f"Erro ao conectar com o Backend: {e}")
