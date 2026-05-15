# Minimarket AI Monitor

Minimarket AI Monitor is an intelligent computer vision system designed to track customers, monitor interactions with shelves and fridges, and generate behavior logs. It integrates a computer vision pipeline with a backend management server to record events for future conciliation with Point-of-Sale (POS) data.

## 🔗 Demonstração em Produção

> 🌐 **Acesse o Dashboard Interativo:** [MiniMarket AI Dashboard](https://minimarket-ai-monitor.onrender.com/dashboard)
>
> ⚠️ **Nota Técnica sobre a Hospedagem (Plano Gratuito):** A aplicação está hospedada na infraestrutura gratuita do Render. Se o sistema estiver inativo por alguns minutos, o servidor entrará em modo de hibernação (*cold start*). O primeiro carregamento pode levar cerca de **45 a 60 segundos** para inicializar o contêiner Docker e conectar ao PostgreSQL. Os acessos seguintes serão instantâneos.

🔗 Production Demo

🌐 Access the Interactive Dashboard: MiniMarket AI Dashboard

⚠️ Technical Note About Hosting (Free Plan): The application is hosted on Render’s free-tier infrastructure. If the system remains inactive for a few minutes, the server will enter hibernation mode (cold start). The first load may take around 45 to 60 seconds to initialize the Docker container and connect to PostgreSQL. Subsequent accesses will be instantaneous.


## 📋 System Requirements

### 1. Functional Requirements (FR)
- **FR01 - Individual Tracking:** The system must assign a unique ID to each person entering the premises.
- **FR02 - Entry/Exit Monitoring:** Record the exact timestamp when an ID crosses the virtual door line.
- **FR03 - Stay Duration Calculation:** Calculate the total time (in seconds/minutes) each ID stayed in the store.
- **FR04 - Interaction Detection:** Identify when a customer interacts with critical areas (fridges and shelves) via Regions of Interest (ROI).
- **FR05 - Payment Conciliation:** Cross-reference customer exit data with POS data (via Backend) to validate purchases.
- **FR06 - Reporting Generation:** Generate an event log consolidated by customer, accessible via API/Dashboard.

### 2. Non-Functional Requirements (NFR)
- **NFR01 - Low Latency:** Video processing must maintain a minimum rate of 10-15 FPS to avoid losing track of objects.
- **NFR02 - ID Persistence:** The tracker must be able to recover a customer's ID in case of partial occlusion (e.g., behind shelves).
- **NFR03 - Scalability:** The architecture must support the addition of up to 3 simultaneous cameras in the same 4m² environment.
- **NFR04 - Isolation:** The system must run in containers to facilitate deployment.


## 🛠 Monorepo Architecture

```text
minimarket-ai-monitor/
├── 🐍 ai-engine                # Python Computer Vision Service (YOLOv8 + Supervision)
│   ├── 📁 app/core             # AI Engine core logic (monitor.py)
│   ├── 📁 app/services         # HTTP Client for event reporting
│   └── 🛠 get_coordinates.py    # Spatial calibration utility
├── ☕ backend-api              # REST API & Orchestrator (Spring Boot 3.x + Java 17)
└── 🐳 docker-compose.yml       # Infrastructure orchestrator
```

## 🚀 Technology Stack

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **👁 Computer Vision** | `Python` + `OpenCV` | Frame capture and manipulation. |
| **🧠 AI Model** | `YOLOv8` (Ultralytics) | Object detection (person, hand, products). |
| **📍 Tracking** | `ByteTrack` + `Supervision` | Persistent tracking and zone/line logic. |
| **Backend** | Spring Boot (Java 17) | Event orchestration, business rules, and APIs. |
| **Database** | MySQL | Persistence of logs, users, and transactions. |
| **Infrastructure** | Docker & Docker Compose | Containerization of all services. |

## 📐 Proposed Architecture

1. **AI-Engine (Python):** Processes the video stream -> Detects movement -> Sends events (JSON) via POST to the Backend.
2. **API Gateway (Spring Boot):** Receives events -> Validates business rules -> Saves to the Database.
3. **Database (MySQL):** Stores the history for future auditing.

## 🚀 How to Run (Preview)

Make sure you have Docker and Nvidia Container Toolkit (if using GPU) installed.

```bash
# Clone the repository
git clone https://github.com/lu78abranches/minimarket-ai-monitor.git
cd minimarket-ai-monitor

# Start the services (Database and Backend)
docker-compose up --build

# Run the AI Engine locally (to access webcam)
cd ai-engine
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## 📌 Development Roadmap Status

Based on an inspection of the current project structure, here is what has been achieved so far and what is left to implement:

### ✅ Done
- **Python Script for Entry/Exit Detection (Virtual Line):** Virtual line crossings are already being detected in `ai-engine/main.py`.
- **Python -> Spring Boot Integration via REST:** The AI-engine leverages `EventService` to post JSON payloads to the Spring Boot backend (`http://localhost:8082/api/events`), which receives them on `MonitoramentoController.java` and saves them to the repository.
- **Interaction Zones Logic (Fridges):** Fridge zones have been mapped and trigger events (`FRIDGE_INTERACTION`) based on detections.
- **Stay Duration Calculation:** Implemented in `AuditoriaService` to calculate exactly how long an individual has remained in the store.
- **Payment Conciliation Logic:** Mock logic added in `AuditoriaService` to flag suspicious behavior (e.g., interacted with items and left without paying).
- **Reporting Dashboard:** Created `DashboardController` and frontend interface to visualize stored interactions and customer journeys.
- **Docker and Database Environment Setup:** Full containerization with `docker-compose.yml` for MySQL 8.0, Spring Boot Backend, and Python AI-Engine (Headless).

### 🚧 To Do
- **Real-time RTSP/NVR Integration:** Connect the AI-Engine to real IP cameras instead of local webcams.
- **Multi-Camera Sync:** Correlate IDs across multiple cameras for a seamless customer journey.
- **Production-Ready Security:** Implement OAuth2/JWT for API security and production database credentials.

### 📬 Contact & Developer

[![GitHub/Luis Abranches](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/lu78abranches)

[![LinkedIn/Luis Abranches](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/luis-abranches/)

