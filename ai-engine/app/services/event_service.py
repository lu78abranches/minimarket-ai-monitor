import requests
import datetime
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class EventService:
    def __init__(self, backend_url="http://localhost:8082/api/events"):
        self.backend_url = backend_url
        self.session = self._create_session_with_retries()

    def _create_session_with_retries(self):
        """Create a session with automatic retry logic for network failures"""
        session = requests.Session()
        
        # Retry strategy for connection errors and timeouts
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[408, 429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def send_event(self, person_id, action):
        payload = {
            "personId": person_id,
            "action": action,  # 'ENTER', 'EXIT' ou 'FRIDGE_INTERACTION'
            "timestamp": datetime.datetime.now().isoformat(),
            "location": "MAIN_ENTRANCE"
        }
        
        try:
            print(f"[LOG] Enviando evento ao backend: {self.backend_url}")
            print(f"[LOG] Payload: person_id={person_id}, action={action}")
            
            # Envio real para o Backend Spring Boot com retry
            response = self.session.post(
                self.backend_url, 
                json=payload, 
                timeout=5.0
            )
            
            if response.status_code == 201:
                print(f"[SUCESSO] ✓ Evento persistido no PostgreSQL! Status: {response.status_code}")
                return True
            else:
                print(f"[AVISO] ⚠ Backend retornou status: {response.status_code}")
                print(f"[AVISO] Response: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError as e:
            print(f"[ERRO] ✗ Falha de conexão - Backend não está acessível em {self.backend_url}")
            print(f"[ERRO] Detalhes: {str(e)}")
            return False
        except requests.exceptions.Timeout:
            print(f"[ERRO] ✗ Timeout ao conectar com o backend (>5s)")
            return False
        except Exception as e:
            print(f"[ERRO] ✗ Erro inesperado ao enviar evento: {type(e).__name__}: {str(e)}")
            return False


