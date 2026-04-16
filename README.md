# Minimarket AI Monitor

Minimarket AI Monitor is an intelligent computer vision system designed to track customers, monitor interactions with shelves and fridges, and generate behavior logs. It integrates a computer vision pipeline with a backend management server to record events for future conciliation with Point-of-Sale (POS) data.

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

## 🛠 Technology Stack

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **Computer Vision** | Python + OpenCV | Frame capture and manipulation (RTSP/Webcam). |
| **AI Model** | YOLOv8 (Ultralytics) | Person and object detection (classes: person, hand, bag). |
| **Tracking** | ByteTrack / Supervision | Persistent tracking and counting lines/zones. |
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
git clone https://github.com/your-username/minimarket-ai-monitor.git
cd minimarket-ai-monitor

# Start the services (Docker integration in progress)
docker-compose up --build
```
*(Note: Complete Docker configuration is pending)*

---

## 📌 Development Roadmap Status

Based on an inspection of the current project structure, here is what has been achieved so far and what is left to implement:

### ✅ Done
- **Python Script for Entry/Exit Detection (Virtual Line):** Virtual line crossings are already being detected in `ai-engine/main.py`.
- **Python -> Spring Boot Integration via REST:** The AI-engine leverages `EventService` to post JSON payloads to the Spring Boot backend (`http://localhost:8082/api/events`), which receives them on `MonitoramentoController.java` and saves them to the repository.
- **Interaction Zones Logic (Fridges):** Fridge zones have been mapped and trigger events (`FRIDGE_INTERACTION`) based on detections.

### 🚧 To Do
- **Docker and Database Environment Setup:** Provide root `docker-compose.yml` to smoothly launch MySQL, Backend, and AI-Engine together.
- **Stay Duration Calculation:** Calculate exactly how long an individual has remained in the store.
- **Payment Conciliation Logic:** Link exit routines with a PoS validation mock.
- **Reporting Dashboard:** Develop a frontend interface or dashboard to visualize stored interactions.

