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

```
## 3. Frontend Architecture

The frontend provides the user interface for interacting with
FlowerVision AI.

Its primary responsibility is to allow users to select a flower image,
send the image to the backend prediction API, and display the returned
prediction.

### 3.1 Frontend Responsibilities

The frontend is responsible for:

- Providing the flower image upload interface.
- Supporting image selection.
- Supporting drag-and-drop image upload.
- Displaying an image preview before prediction.
- Sending the image to the backend API.
- Displaying a loading state while prediction is in progress.
- Displaying prediction errors when a request fails.
- Displaying the predicted flower class.
- Displaying the prediction confidence.
- Allowing the user to identify another flower.

### 3.2 Current Frontend Structure

The current frontend consists of the following files:

```text
frontend/
├── index.html
├── style.css
├── app.js
├── config.js
└── README.md

```

### 3.3 Frontend Components

The frontend is currently organized into the following components:

#### `index.html`

Provides the main structure of the FlowerVision AI user interface.

It contains:

- Application header.
- Flower upload area.
- File selection control.
- Image preview area.
- Prediction button.
- Loading state.
- Error message area.
- Prediction result area.
- Confidence display.
- Reset functionality.

#### `style.css`

Provides the visual presentation of the application.

It is responsible for:

- Page layout.
- Upload area styling.
- Buttons.
- Image preview.
- Loading indicator.
- Prediction result presentation.
- Error messages.
- Responsive behavior.

#### `app.js`

Contains the frontend application logic.

It handles:

- File selection.
- Drag-and-drop events.
- Image preview.
- File submission.
- Communication with the prediction API.
- Loading state management.
- Error handling.
- Displaying prediction results.
- Displaying confidence.
- Resetting the application.

#### `config.js`

Contains frontend configuration values, including the backend API
base URL used by the application.

Keeping the API configuration separate allows the backend URL to be
changed without modifying the main application logic.

#### `README.md`

Provides frontend-specific documentation, including information
about the frontend structure, setup, configuration, and usage.

### 3.4 Frontend-to-Backend Communication

The frontend communicates with the FastAPI backend through HTTP
requests.

The backend API base URL is configured in `config.js`, allowing the
frontend configuration to be changed without modifying the main
application logic.

### Prediction Request

For flower recognition, the frontend sends an HTTP `POST` request to:

```text
/api/v1/predict
```

### 3.5 Frontend Error Handling

The frontend handles errors that may occur during image selection,
validation, API communication, and prediction.

The goal is to provide clear feedback to the user while avoiding the
exposure of unnecessary internal implementation details.

#### 3.5.1 Invalid File

The frontend should prevent unsupported files from being submitted
for prediction.

Examples of invalid input include:

- No file selected.
- Unsupported file type.
- Invalid image file.
- File that exceeds the configured size limit.

When an invalid file is detected, the frontend displays an appropriate
error message and does not send the prediction request.

#### 3.5.2 API Request Failure

If the frontend cannot communicate with the backend, the application
displays a user-friendly error message.

Possible causes include:

- Backend server is not running.
- Incorrect API URL.
- Network connection failure.
- CORS configuration issue.
- Request timeout.

The frontend should not expose technical stack traces to the user.

#### 3.5.3 Backend Error Response

If the backend returns an error response, the frontend checks the HTTP
response status and displays an appropriate message.

The frontend should distinguish between:

- Client-side validation errors.
- Invalid image errors.
- Model or service availability errors.
- Unexpected server errors.

#### 3.5.4 Loading State

While the prediction request is being processed, the frontend displays
a loading state.

The loading state provides visual feedback that the request is being
processed.

During this state, duplicate prediction requests should be prevented
until the current request has completed.

The flow is:

```text
User submits image
        |
        v
Loading state enabled
        |
        v
Prediction request
        |
        +------------------+
        |                  |
        v                  v
    Success              Error
        |                  |
        v                  v
Display result       Display error
        |                  |
        +--------+---------+
                 |
                 v
          Loading disabled
```

### 3.6 Frontend Design Principles

The FlowerVision AI frontend follows a set of design principles that
focus on simplicity, usability, maintainability, and clear separation
of responsibilities.

#### 3.6.1 Simplicity

The frontend should remain lightweight and easy to understand.

Unnecessary dependencies, complex abstractions, and redundant
functionality should be avoided.

#### 3.6.2 Separation of Responsibilities

The frontend is responsible for:

- User interface presentation.
- User interaction.
- Image selection.
- Image preview.
- API communication.
- Displaying prediction results.
- Displaying user-friendly errors.

The frontend should not contain the AI inference logic.

Image processing and model inference are handled by the backend.

#### 3.6.3 Maintainability

Frontend code should be organized into logical files and components.

Related functionality should be kept together while avoiding large
files that contain unrelated responsibilities.

Configuration values such as the backend API URL should be maintained
separately from application logic.

#### 3.6.4 Reusability

Frontend functionality should be designed so that commonly used
operations can be reused.

Examples include:

- File validation.
- API requests.
- Error handling.
- Loading state management.
- Result rendering.

Reusable functionality makes future feature development easier.

#### 3.6.5 Responsive User Interface

The frontend should provide a usable experience across different
screen sizes.

The interface should work on:

- Desktop screens.
- Laptop screens.
- Tablet screens.
- Mobile screens.

The layout should adapt without requiring separate applications for
different device types.

#### 3.6.6 Clear User Feedback

The interface should provide feedback for important application
states.

These states include:

- Waiting for an image.
- Image selected.
- Image preview available.
- Prediction in progress.
- Prediction completed.
- Prediction failed.

Users should always have a clear indication of what the application
is currently doing.

#### 3.6.7 Backend Responsibility

The frontend should treat the backend as the source of truth for
flower classification.

The frontend should not attempt to reproduce:

- Image preprocessing.
- Model loading.
- Model inference.
- Confidence calculation.
- Flower classification logic.

These responsibilities belong to the backend prediction service.

#### 3.6.8 Configuration Management

Environment-specific configuration should not be hardcoded throughout
the frontend application.

The backend API URL should be maintained through the frontend
configuration mechanism.

This allows the same frontend codebase to be adapted for different
environments.

#### 3.6.9 Security

The frontend should avoid exposing sensitive information.

The frontend must not contain:

- API secrets.
- Passwords.
- Private keys.
- Database credentials.
- Other sensitive configuration.

Only configuration that is safe to expose to the browser should be
included in frontend code.

#### 3.6.10 Future Extensibility

The frontend architecture should allow additional features to be
introduced without requiring a complete rewrite.

Potential future frontend capabilities include:

- Flower information.
- Prediction history.
- Recommendations.
- Improved accessibility.
- Additional UI components.
- React and Vite migration.

New functionality should be added incrementally while preserving the
existing prediction workflow.

## 4. Backend Architecture

The FlowerVision AI backend is built using FastAPI and provides the
API layer responsible for receiving requests, validating input,
processing images, performing AI inference, and returning prediction
results.

The backend follows a separation-of-responsibilities approach.
API routes handle HTTP communication, while dedicated services handle
image processing and AI prediction.

### 4.1 Backend Responsibilities

The backend is responsible for:

- Providing REST API endpoints.
- Validating incoming requests.
- Validating uploaded image files.
- Processing images before inference.
- Loading the trained AI model.
- Performing flower classification.
- Returning prediction results.
- Handling application errors.
- Providing health-check information.
- Logging important application events.
- Supporting automated backend testing.

### 4.2 Backend Structure

The backend application is organized as follows:

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

```
### 4.13 API Endpoints

FlowerVision AI exposes REST API endpoints through the FastAPI
application.

The API provides endpoints for:

- Application information.
- Backend health status.
- Supported flower classes.
- Flower image prediction.

All API endpoints are implemented in:

```text
backend/app/api/routes.py
```

### 4.14 Prediction Service Architecture

The prediction service is responsible for performing flower image
classification using the trained MobileNetV3-Small model.

The prediction pipeline is:

```text
Uploaded Image
      |
      v
File Validation
      |
      v
Image Processor
      |
      v
Preprocessed Image
      |
      v
Predictor Service
      |
      v
MobileNetV3-Small Model
      |
      v
Predicted Flower Class
      |
      v
Confidence Score
      |
      v
Prediction Response
```

### 4.15 Model Architecture and Training

FlowerVision AI uses a lightweight **MobileNetV3-Small** model with
transfer learning for flower image classification.

The model was initialized with ImageNet-pretrained weights and
adapted for the five flower classes supported by the application.

#### Model Summary

| Item | Details |
|---|---|
| Architecture | MobileNetV3-Small |
| Learning Approach | Transfer Learning |
| Pretrained Weights | ImageNet |
| Training Device | CPU |
| Training Images | 2,936 |
| Validation Images | 734 |
| Training Epochs | 5 |
| Flower Classes | 5 |
| Best Validation Accuracy | 89.92% |
| Model File | `flower_classifier.pth` |
| Class Mapping | `class_names.json` |

#### Dataset

The training dataset contains five flower categories:

- Daisy
- Dandelion
- Rose
- Sunflower
- Tulip

The complete prepared dataset contains **3,670 images**.

#### Training Results

The model achieved the following validation accuracy during training:

```text
Epoch 1: 85.69%
Epoch 2: 88.28%
Epoch 3: 88.96%
Epoch 4: 89.37%
Epoch 5: 89.92%

```

### 4.16 Model Inference Flow

The model inference flow describes how FlowerVision AI processes an
uploaded flower image and generates a prediction.

The inference pipeline is:

```text
Uploaded Image
      |
      v
File Validation
      |
      v
Image Processing
      |
      v
Image Tensor
      |
      v
MobileNetV3-Small
      |
      v
Model Output
      |
      v
Class Mapping
      |
      v
Flower Prediction
      |
      v
Confidence Score
      |
      v
API Response

```
