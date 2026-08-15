# 🌸 FlowerVision AI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)
![React](https://img.shields.io/badge/React-19-61DAFB.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![AI](https://img.shields.io/badge/AI-Computer%20Vision-orange.svg)

### AI-powered Flower Image Recognition Web Application

*A production-ready full-stack AI application for recognizing flower species from uploaded images using deep learning.*

---

### Built With

Python • FastAPI • React • PyTorch • OpenCV • Pillow • SQLite • Docker • GitHub Actions

</div>

---

# 📖 Overview

FlowerVision AI is a modern end-to-end computer vision application that enables users to upload an image of a flower and receive an AI-powered prediction of its species along with the model's confidence score.

The project is designed to demonstrate how modern AI systems are built in production using clean architecture, REST APIs, lightweight deep learning models, containerization, automated testing, and continuous integration.

Unlike a simple machine learning notebook, this repository follows software engineering best practices and is organized as a scalable full-stack application.

---

# ✨ Features

## AI Features

- 🌸 Flower species classification
- 🧠 Deep learning powered prediction
- 📷 Image upload support
- 📊 Confidence score visualization
- ⚡ Fast inference
- 🖼️ Image preprocessing pipeline
- 🔍 Prediction details
- 📈 Lightweight pretrained model

---

## Backend Features

- FastAPI REST API
- Automatic Swagger Documentation
- OpenAPI Specification
- Image validation
- Error handling
- Structured logging
- Modular architecture
- Dependency Injection
- Configuration management
- Unit testing

---

## Frontend Features

- Modern React UI
- Responsive Design
- Drag & Drop Upload
- Image Preview
- Prediction Dashboard
- Confidence Meter
- Loading Animations
- Error Notifications
- Mobile Friendly

---

## DevOps Features

- Docker Support
- Docker Compose
- GitHub Actions
- Automated Testing
- Code Formatting
- Linting
- Environment Variables
- Production Ready Structure

---

# 🎯 Objectives

The primary objective of this project is to demonstrate an end-to-end AI application that combines machine learning with modern web technologies.

The application focuses on:

- Building a production-ready AI backend
- Developing a modern frontend
- Serving ML models through REST APIs
- Containerizing applications
- Implementing CI/CD pipelines
- Following clean architecture principles
- Maintaining professional documentation

---

# 🏗️ High-Level Architecture

```text
                    +---------------------+
                    |     Web Browser     |
                    +----------+----------+
                               |
                               |
                               ▼
                  +-------------------------+
                  |      React Frontend     |
                  +------------+------------+
                               |
                    HTTP / REST API
                               |
                               ▼
                 +---------------------------+
                 |      FastAPI Backend      |
                 +------------+--------------+
                              |
          +-------------------+-------------------+
          |                                       |
          ▼                                       ▼
 Image Processing                      AI Prediction Engine
(OpenCV + Pillow)                     (PyTorch MobileNetV3)
          |                                       |
          +-------------------+-------------------+
                              |
                              ▼
                      Prediction Result
                              |
                              ▼
                        JSON Response
```

---

# 📁 Repository Structure

```
flower-image-recognition-ai/

├── README.md
├── product-spec.md
├── AGENTS.md
├── openapi.yaml
├── docker-compose.yml
│
├── backend/
│
├── frontend/
│
├── docs/
│
├── security/
│
├── ops/
│
├── models/
│
├── tests/
│
└── .github/
    └── workflows/
```

---

# 🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python 3.12 |
| Backend | FastAPI |
| Frontend | React + Vite |
| AI Framework | PyTorch |
| Computer Vision | OpenCV |
| Image Processing | Pillow |
| Database | SQLite |
| API Documentation | OpenAPI |
| Containerization | Docker |
| Version Control | Git |
| CI/CD | GitHub Actions |

---

# 🚀 Planned Features

- Image Upload
- AI Prediction
- Confidence Score
- Prediction History
- Model Information
- REST API
- OpenAPI Documentation
- Docker Deployment
- GitHub Actions
- Unit Tests
- Integration Tests
- Security Best Practices
- Monitoring
- Logging
- Health Checks

---

# 📸 Application Preview

The application will include:

- Modern Landing Page
- Drag & Drop Upload
- Image Preview
- AI Prediction Card
- Confidence Visualization
- Prediction History
- Responsive Dashboard
- Error Handling
- Loading Animation

> Screenshots and GIF demonstrations will be added after the frontend implementation is completed.

---

# 🌼 Supported Flower Species

The initial release will support classification of common flower species such as:

- Daisy
- Dandelion
- Rose
- Sunflower
- Tulip

Additional species can be added by retraining or fine-tuning the model.

---

# 🔮 Future Enhancements

- Multi-flower detection
- Object detection with bounding boxes
- Real-time webcam prediction
- Mobile application
- Model versioning
- Cloud deployment
- User authentication
- Prediction analytics
- Explainable AI (Grad-CAM)
- Multi-language support

---

## ⭐ Why This Project?

This repository is intended to serve as a reference implementation for building production-quality AI web applications. It combines machine learning, backend development, frontend engineering, DevOps practices, and software architecture into a single cohesive project.

Whether you are learning AI engineering, exploring FastAPI, or building your portfolio, FlowerVision AI demonstrates how to move from a trained model to a deployable application using industry-standard tools and practices.

---

**📌 End of README Part 1**

➡️ Next: **Part 2** will include:
- Installation and setup
- Local development
- Docker usage
- Environment configuration
- Backend setup
- Frontend setup
- Running the application
- API overview
- Development workflow
- Git conventions



---

# 💻 System Requirements

The application has been designed to run efficiently on a standard developer laptop.

## Minimum Requirements

| Component | Requirement |
|------------|-------------|
| CPU | Dual-Core Processor |
| RAM | 8 GB |
| Storage | 5 GB Free Disk Space |
| Python | 3.12+ |
| Node.js | 20+ |
| Git | Latest |
| Docker | Latest (Optional) |

---

## Recommended Requirements

| Component | Recommendation |
|------------|----------------|
| CPU | Intel i5 / AMD Ryzen 5 or higher |
| RAM | 16 GB |
| Storage | SSD |
| GPU | Optional (CPU inference supported) |
| Operating System | Ubuntu 24.04 LTS / Windows 11 / macOS |

---

# 📦 Installation

Clone the repository.

```bash
git clone https://github.com/<your-github-username>/flower-image-recognition-ai.git

cd flower-image-recognition-ai
```

---

# 🐍 Backend Setup

Navigate to the backend directory.

```bash
cd backend
```

Create a virtual environment.

### Windows

```bash
python -m venv .venv
```

Activate the environment.

```bash
.venv\Scripts\activate
```

---

### Linux/macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

Install project dependencies.

```bash
pip install -r requirements.txt
```

Start the backend server.

```bash
uvicorn app.main:app --reload
```

The backend API will be available at:

```
http://localhost:8000
```

---

# ⚛️ Frontend Setup

Move to the frontend directory.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Start the development server.

```bash
npm run dev
```

The frontend application will run at

```
http://localhost:5173
```

---

# 🐳 Docker Setup

Build the project.

```bash
docker compose build
```

Run the containers.

```bash
docker compose up
```

Run in detached mode.

```bash
docker compose up -d
```

Stop the containers.

```bash
docker compose down
```

---

# 🌍 Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
APP_NAME=FlowerVision AI

APP_ENV=development

DEBUG=True

HOST=0.0.0.0

PORT=8000

MODEL_PATH=models/mobilenet_v3.pth

DATABASE_URL=sqlite:///flowervision.db

MAX_UPLOAD_SIZE=10485760
```

---

# ▶️ Running the Application

Start the backend.

```bash
uvicorn app.main:app --reload
```

Open another terminal.

Start the frontend.

```bash
npm run dev
```

Visit

```
http://localhost:5173
```

Upload a flower image and receive an AI prediction.

---

# 📡 API Overview

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | API Status |
| GET | /health | Health Check |
| POST | /predict | Flower Prediction |
| GET | /flowers | Supported Flower Classes |
| GET | /docs | Swagger Documentation |
| GET | /openapi.json | OpenAPI Specification |

---

# 🧪 Running Tests

Backend tests

```bash
pytest
```

Run with coverage.

```bash
pytest --cov
```

Frontend tests

```bash
npm test
```

---

# 🧹 Code Formatting

Python formatting

```bash
black .
```

Import sorting

```bash
isort .
```

Lint Python code

```bash
ruff check .
```

Frontend linting

```bash
npm run lint
```

---

# 📖 API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

OpenAPI JSON

```
http://localhost:8000/openapi.json
```

---

# 🔄 Development Workflow

1. Create a new feature branch.
2. Implement the feature.
3. Add or update tests.
4. Run formatting tools.
5. Run linting.
6. Verify all tests pass.
7. Commit changes.
8. Open a Pull Request.

---

# 🌿 Git Branch Strategy

| Branch | Purpose |
|----------|-----------|
| main | Production |
| develop | Active Development |
| feature/* | New Features |
| bugfix/* | Bug Fixes |
| release/* | Release Preparation |
| hotfix/* | Production Hotfixes |

---

# 📝 Commit Message Convention

Examples

```text
feat: add flower prediction endpoint

fix: correct image preprocessing bug

docs: update README

refactor: improve API architecture

test: add prediction unit tests

chore: update dependencies
```

---

# 🗂️ Project Workflow

```text
Create Feature

↓

Implement Code

↓

Write Tests

↓

Run Linter

↓

Run Formatter

↓

Commit Changes

↓

Push Branch

↓

Open Pull Request

↓

Code Review

↓

Merge into Main
```

---

# 🧠 AI Model Pipeline

```text
Upload Image

↓

Validate Request

↓

Resize Image

↓

Normalize

↓

Convert Tensor

↓

Run PyTorch Model

↓

Predict Flower

↓

Confidence Score

↓

Return JSON Response
```

---

# ⚙️ Performance Goals

| Metric | Target |
|----------|---------|
| API Response | < 500 ms |
| Prediction Time | < 300 ms |
| Image Upload | < 10 MB |
| Cold Start | < 3 sec |
| Model Loading | < 5 sec |

---

# 🔐 Security Highlights

- File type validation
- File size limits
- Input sanitization
- Secure HTTP headers
- Environment variable configuration
- Dependency scanning
- Docker security best practices

---

# 📚 Additional Documentation

Detailed project documentation is available in the `docs/` directory.

Topics include:

- System Architecture
- Backend Design
- Frontend Design
- Deployment Guide
- Docker Guide
- API Reference
- Troubleshooting
- FAQ

---

**📌 End of README Part 2**

➡️ Next: **Part 3 (Final)** will include:
- Contributing
- Coding standards
- Project roadmap
- FAQ
- Troubleshooting
- License
- Acknowledgements
- Maintainers
- Contact
- Badges
- Final project summary


---

# 🤝 Contributing

Thank you for your interest in contributing to **FlowerVision AI**!

We welcome contributions from developers, AI engineers, designers, testers, technical writers, and open-source enthusiasts. Whether you are fixing a bug, improving documentation, optimizing the AI model, or adding a new feature, your contributions are highly appreciated.

## Ways to Contribute

- 🐞 Report bugs
- ✨ Suggest new features
- 📚 Improve documentation
- 🎨 Enhance the frontend UI/UX
- ⚡ Optimize backend performance
- 🧠 Improve AI model accuracy
- 🧪 Write unit and integration tests
- 🔐 Improve security
- 🐳 Enhance Docker configuration
- 📦 Update project dependencies

---

# 🛠️ Development Guidelines

Please follow these principles while contributing:

- Write clean, readable, and maintainable code.
- Keep functions small and focused.
- Avoid unnecessary complexity.
- Follow the existing project architecture.
- Add comments only where necessary.
- Write tests for new functionality.
- Keep commits small and meaningful.
- Update documentation whenever functionality changes.

---

# 🐍 Python Coding Standards

The backend follows modern Python best practices.

### Style Guide

- Follow **PEP 8**
- Use type hints wherever possible
- Write descriptive variable names
- Use dataclasses or Pydantic models when appropriate
- Keep business logic separate from API routes

### Example

```python
def predict_flower(image: Image.Image) -> PredictionResult:
    """Predict the flower species from an uploaded image."""
```

---

# ⚛️ React Coding Standards

Frontend code should be modular and reusable.

Guidelines:

- Use functional components.
- Prefer React Hooks.
- Keep components small.
- Separate UI and business logic.
- Reuse components whenever possible.
- Use descriptive component names.
- Avoid deeply nested component trees.

---

# 📂 Folder Organization

Each directory has a single responsibility.

| Folder | Responsibility |
|----------|---------------|
| backend | API and AI inference |
| frontend | User interface |
| docs | Documentation |
| security | Security policies |
| ops | Deployment and operations |
| models | AI model files |
| tests | Automated testing |
| .github | GitHub workflows |

---

# 🌿 Branching Strategy

We follow a simplified Git Flow model.

```
main
│
├── develop
│
├── feature/image-upload
│
├── feature/api
│
├── feature/frontend
│
├── bugfix/upload-error
│
└── release/v1.0
```

### Branch Naming

Feature

```
feature/add-history-page
```

Bug Fix

```
bugfix/fix-upload-validation
```

Hotfix

```
hotfix/security-patch
```

Documentation

```
docs/update-readme
```

---

# 🔀 Pull Request Process

Before opening a Pull Request:

- Ensure all tests pass.
- Run formatters.
- Run linting.
- Update documentation.
- Resolve merge conflicts.
- Write a meaningful PR description.

### Pull Request Checklist

- [ ] Code builds successfully
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No unnecessary files added
- [ ] Code follows project standards
- [ ] Feature works as expected

---

# 🧪 Testing Strategy

The project includes multiple layers of testing.

## Unit Tests

Test individual functions.

Example:

- Image preprocessing
- Prediction utilities
- Configuration loading

---

## Integration Tests

Test interactions between components.

Example:

- Upload endpoint
- Prediction endpoint
- Database interactions

---

## End-to-End Tests

Validate the complete application flow.

Example:

```
Upload Image

↓

Backend Validation

↓

Model Prediction

↓

Return JSON

↓

Frontend Display
```

---

# 📏 Code Quality Standards

The project prioritizes quality over quantity.

Every contribution should be:

- Readable
- Modular
- Testable
- Maintainable
- Documented
- Secure

---

# 🔍 Static Analysis Tools

Backend

- Ruff
- Black
- isort
- MyPy

Frontend

- ESLint
- Prettier

---

# 📈 Project Roadmap

## Version 1.0

- Image Upload
- Flower Classification
- REST API
- React Frontend
- Docker
- Swagger Documentation
- CI/CD Pipeline

---

## Version 1.1

- Prediction History
- Confidence Charts
- Improved UI
- Additional Flower Species

---

## Version 2.0

- Object Detection
- Multi-Flower Recognition
- Webcam Support
- Explainable AI (Grad-CAM)
- User Authentication

---

## Version 3.0

- Mobile Application
- Cloud Deployment
- Model Versioning
- Analytics Dashboard
- Model Monitoring

---

# 🎯 Project Goals

This repository aims to demonstrate:

- Production-ready AI development
- Modern backend architecture
- Responsive frontend development
- Clean software engineering
- AI model deployment
- REST API development
- Docker containerization
- Continuous Integration
- Automated testing

---

# 🔒 Security Policy

Security is a priority.

Please do **not** publicly disclose security vulnerabilities.

Instead:

1. Create a private report.
2. Include reproduction steps.
3. Describe the impact.
4. Suggest mitigation if possible.

Future releases will include a dedicated `SECURITY.md` document.

---

# 📋 Supported Platforms

| Platform | Status |
|-----------|--------|
| Ubuntu | ✅ Supported |
| Windows | ✅ Supported |
| macOS | ✅ Supported |

---

# ❓ Frequently Asked Questions

## Does this project require a GPU?

No.

CPU inference is fully supported.

---

## Can I train my own model?

Yes.

The application is designed so the prediction model can be replaced with your own trained model.

---

## Can I add more flower species?

Absolutely.

Simply retrain or fine-tune the model using an expanded dataset and update the label mappings.

---

## Is Docker required?

No.

Docker is optional but recommended for a consistent development environment.

---

## Is this suitable for beginners?

Yes.

The project is structured to help learners understand how AI models integrate into real web applications while following professional engineering practices.

---

## 💡 Best Practices

- Write self-documenting code.
- Keep functions focused.
- Avoid duplicated logic.
- Handle errors gracefully.
- Validate all user input.
- Keep dependencies up to date.
- Document architectural decisions.
- Review code before merging.
- Write tests for every new feature.
- Think about scalability from the beginning.

---

**📌 End of README Part 3A**

➡️ **Next:** **Part 3B (Final)** will complete the README with:
- Troubleshooting
- Performance optimization
- Monitoring & logging
- License
- Acknowledgements
- Maintainers
- Contact
- Citation
- Support
- Final project summary
- Professional closing section



