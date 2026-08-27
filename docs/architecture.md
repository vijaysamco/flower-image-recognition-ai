# FlowerVision AI — Architecture

## 1. Overview

FlowerVision AI is a lightweight AI web application that classifies
flower species from uploaded images.

The project is designed around the following principles:

- Simplicity
- Readability
- Maintainability
- Security
- Performance
- Scalability

The application consists of a frontend, FastAPI backend, image
processing pipeline, trained PyTorch model, testing layer, and
deployment infrastructure.

The architecture separates user interface, API handling, image
processing, AI inference, testing, documentation, security, and
deployment responsibilities.

# 2. High-Level Architecture

The FlowerVision AI application follows a layered architecture.

```text
                         User
                           |
                           v
                +----------------------+
                |      Frontend        |
                | HTML / CSS / JS      |
                +----------+-----------+
                           |
                           | HTTP Request
                           v
                +----------------------+
                |      FastAPI          |
                |      Backend          |
                +----------+-----------+
                           |
              +------------+------------+
              |                         |
              v                         v
    +-------------------+      +-------------------+
    | File Validation   |      | Error Handling    |
    +---------+---------+      +-------------------+
              |
              v
    +-------------------+
    | Image Processor   |
    +---------+---------+
              |
              v
    +-------------------+
    | Predictor Service |
    +---------+---------+
              |
              v
    +-------------------+
    | MobileNetV3-Small |
    | Flower Classifier |
    +---------+---------+
              |
              v
    +-------------------+
    | Prediction Result |
    | + Confidence      |
    +-------------------+




This gives the document its core architectural diagram before we document individual components.

---

## Step 3 — Add the Frontend Architecture

Next section:

```markdown
# 3. Frontend

The frontend is responsible for the user interface and communication
with the backend prediction API.

The current frontend provides:

- Image selection
- Drag-and-drop image upload
- Image preview
- Prediction request
- Loading state
- Error handling
- Prediction display
- Confidence display
- Reset and retry functionality

The current frontend structure is:

```text
frontend/
├── index.html
├── style.css
├── app.js
├── config.js
└── README.md



---

## Step 4 — Add the Backend Architecture

```markdown
# 4. Backend

The backend is implemented using FastAPI.

The backend is responsible for:

- API endpoints
- Request validation
- File validation
- Image processing
- AI inference
- Error handling
- Logging
- Health checks

The backend follows a separation-of-responsibilities approach so that
business logic is not placed directly inside API route handlers.

The current backend structure is:

```text
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logger.py
│   │
│   ├── exceptions/
│   │   └── handlers.py
│   │
│   ├── middleware/
│   │   └── logging.py
│   │
│   ├── models/
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── prediction.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── image_processor.py
│   │   └── predictor.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── file_validator.py
│   │
│   ├── __init__.py
│   └── main.py
│
├── models/
│   ├── flower_classifier.pth
│   └── class_names.json
│
├── tests/
│   ├── test_flowers.py
│   ├── test_health.py
│   └── test_predict.py
│
└── requirements.txt


---

### 🧩 Your `architecture.md` currently contains

```text
docs/architecture.md
│
├── 1. Overview
├── 2. High-Level Architecture
├── 3. Frontend
└── 4. Backend

