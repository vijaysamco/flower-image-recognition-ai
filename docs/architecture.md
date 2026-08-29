# FlowerVision AI — Architecture

## 1. Overview

FlowerVision AI is a lightweight AI web application that classifies
flower species from uploaded images.

The application is designed with the following principles:

- Simplicity
- Readability
- Maintainability
- Security
- Performance
- Scalability

The system separates the user interface, API layer, image processing,
AI inference, testing, security, documentation, and deployment
responsibilities.

The primary workflow is:

1. User uploads a flower image.
2. Frontend sends the image to the backend.
3. Backend validates the uploaded file.
4. Image processor prepares the image.
5. Predictor service performs AI inference.
6. The trained model predicts the flower class.
7. Backend returns the prediction and confidence.
8. Frontend displays the result to the user.

## 2. High-Level Architecture

FlowerVision AI follows a layered architecture in which each major
component has a clearly defined responsibility.

The high-level system flow is:

```text
                         User
                           |
                           v
                +----------------------+
                |      Frontend        |
                |   HTML / CSS / JS    |
                +----------+-----------+
                           |
                           | HTTP Request
                           v
                +----------------------+
                |      FastAPI          |
                |      Backend          |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   File Validation    |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   Image Processor    |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |  Predictor Service   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   MobileNetV3-Small  |
                |  Flower Classifier   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Prediction +         |
                | Confidence Score     |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |      Frontend        |
                |   Display Result     |
                +----------------------+
