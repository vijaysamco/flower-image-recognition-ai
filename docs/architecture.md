# FlowerVision AI — Architecture

## 1. Overview

FlowerVision AI is a lightweight AI web application that classifies
flower species from uploaded images.

The project is designed around:

- Simplicity
- Readability
- Maintainability
- Security
- Performance
- Scalability

The application consists of a frontend, FastAPI backend, image
processing pipeline, trained PyTorch model, testing layer, and
deployment infrastructure.

---

# 2. High-Level Architecture

```text
                         User
                           |
                           v
                +----------------------+
                |      Frontend        |
                | HTML / CSS / JS       |
                +----------+-----------+
                           |
                           | HTTP
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
    | File Validation   |      | API Error Handling|
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
    | Prediction Result  |
    | + Confidence      |
    +-------------------+