import numpy as np
import supervision as sv
from app.core.monitor import MarketMonitor

def test_person_inside_fridge_zone():
    monitor = MarketMonitor()
    
    # 1. Definimos uma zona quadrada (ex: Geladeira 01)
    fridge_zone_coords = np.array([[100, 100], [200, 100], [200, 200], [100, 200]])
    monitor.add_fridge_zone(fridge_zone_coords)
    
    # 2. Simulamos uma detecção de pessoa exatamente no meio da geladeira (150, 150)
    fake_detections = sv.Detections(
        xyxy=np.array([[140, 140, 160, 160]]), # Bounding box pequena
        class_id=np.array([0]) # Classe 'person'
    )
    
    # 3. O teste espera que o monitor confirme a interação
    is_interacting = monitor.check_fridge_interaction(fake_detections)
    assert is_interacting is True
