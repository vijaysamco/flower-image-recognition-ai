"use strict";

/*
 * FlowerVision AI
 * Frontend Application
 *
 * Responsibilities:
 * - Image selection
 * - Drag and drop
 * - Image preview
 * - API prediction request
 * - Loading state
 * - Prediction result
 * - Error handling
 * - Reset / retry
 */


// --------------------------------------------------
// Configuration
// --------------------------------------------------

const API_URL =
    FLOWERVISION_CONFIG.API_BASE_URL +
    FLOWERVISION_CONFIG.PREDICT_ENDPOINT;


// --------------------------------------------------
// DOM Elements
// --------------------------------------------------

const dropZone =
    document.getElementById("dropZone");

const chooseButton =
    document.getElementById("chooseButton");

const fileInput =
    document.getElementById("fileInput");

const previewContainer =
    document.getElementById(
        "previewContainer"
    );

const previewImage =
    document.getElementById(
        "previewImage"
    );

const fileName =
    document.getElementById(
        "fileName"
    );

const predictButton =
    document.getElementById(
        "predictButton"
    );

const changeButton =
    document.getElementById(
        "changeButton"
    );

const loading =
    document.getElementById(
        "loading"
    );

const errorMessage =
    document.getElementById(
        "errorMessage"
    );

const result =
    document.getElementById(
        "result"
    );

const prediction =
    document.getElementById(
        "prediction"
    );

const confidence =
    document.getElementById(
        "confidence"
    );

const confidenceFill =
    document.getElementById(
        "confidenceFill"
    );

const resultFileName =
    document.getElementById(
        "resultFileName"
    );

const resetButton =
    document.getElementById(
        "resetButton"
    );


// --------------------------------------------------
// Application State
// --------------------------------------------------

let selectedFile = null;

let previewUrl = null;


// --------------------------------------------------
// Choose Image
// --------------------------------------------------

chooseButton.addEventListener(
    "click",
    () => {
        fileInput.click();
    }
);


fileInput.addEventListener(
    "change",
    (event) => {

        const file =
            event.target.files[0];

        if (file) {
            handleFile(file);
        }
    }
);


// --------------------------------------------------
// Drag & Drop
// --------------------------------------------------

dropZone.addEventListener(
    "dragover",
    (event) => {

        event.preventDefault();

        dropZone.classList.add(
            "drag-over"
        );
    }
);


dropZone.addEventListener(
    "dragleave",
    () => {

        dropZone.classList.remove(
            "drag-over"
        );
    }
);


dropZone.addEventListener(
    "drop",
    (event) => {

        event.preventDefault();

        dropZone.classList.remove(
            "drag-over"
        );

        const file =
            event.dataTransfer.files[0];

        if (file) {
            handleFile(file);
        }
    }
);


// --------------------------------------------------
// Handle Selected File
// --------------------------------------------------

function handleFile(file) {

    clearError();

    if (!isValidFile(file)) {

        showError(
            "Please select a JPG, PNG, or WebP image."
        );

        return;
    }


    selectedFile = file;


    // Release previous preview URL.

    if (previewUrl) {

        URL.revokeObjectURL(
            previewUrl
        );
    }


    previewUrl =
        URL.createObjectURL(file);


    previewImage.src =
        previewUrl;


    fileName.textContent =
        file.name;


    dropZone.classList.add(
        "hidden"
    );


    result.classList.add(
        "hidden"
    );


    previewContainer.classList.remove(
        "hidden"
    );
}


// --------------------------------------------------
// Validate File
// --------------------------------------------------

function isValidFile(file) {

    const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/webp",
    ];


    return allowedTypes.includes(
        file.type
    );
}


// --------------------------------------------------
// Prediction Button
// --------------------------------------------------

predictButton.addEventListener(
    "click",
    async () => {

        if (!selectedFile) {

            showError(
                "Please select an image first."
            );

            return;
        }


        await predictFlower(
            selectedFile
        );
    }
);


// --------------------------------------------------
// Predict Flower
// --------------------------------------------------

async function predictFlower(file) {

    clearError();

    setLoading(true);


    const formData =
        new FormData();


    formData.append(
        "file",
        file
    );


    try {

        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",
                    body: formData,
                }
            );


        let data;

        try {

            data =
                await response.json();

        } catch (jsonError) {

            throw new Error(
                "The server returned an invalid response."
            );
        }


        if (!response.ok) {

            const message =
                data?.error?.details ||
                data?.detail ||
                "Prediction failed.";

            throw new Error(
                message
            );
        }


        displayResult(data);


    } catch (error) {

        console.error(
            "FlowerVision AI prediction error:",
            error
        );


        showError(
            getErrorMessage(error)
        );


    } finally {

        setLoading(false);
    }
}


// --------------------------------------------------
// Display Prediction Result
// --------------------------------------------------

function displayResult(data) {

    const flower =
        data.prediction;


    const confidenceValue =
        Number(
            data.confidence
        );


    prediction.textContent =
        capitalize(flower);


    confidence.textContent =
        `${confidenceValue.toFixed(2)}%`;


    confidenceFill.style.width =
        `${Math.min(
            Math.max(
                confidenceValue,
                0
            ),
            100
        )}%`;


    resultFileName.textContent =
        `Image: ${
            data.filename ||
            selectedFile.name
        }`;


    previewContainer.classList.add(
        "hidden"
    );


    result.classList.remove(
        "hidden"
    );
}


// --------------------------------------------------
// Loading State
// --------------------------------------------------

function setLoading(isLoading) {

    if (isLoading) {

        predictButton.disabled =
            true;

        changeButton.disabled =
            true;

        chooseButton.disabled =
            true;

        loading.classList.remove(
            "hidden"
        );

        result.classList.add(
            "hidden"
        );

    } else {

        predictButton.disabled =
            false;

        changeButton.disabled =
            false;

        chooseButton.disabled =
            false;

        loading.classList.add(
            "hidden"
        );
    }
}


// --------------------------------------------------
// Change Image
// --------------------------------------------------

changeButton.addEventListener(
    "click",
    () => {

        fileInput.value = "";

        fileInput.click();
    }
);


// --------------------------------------------------
// Reset Application
// --------------------------------------------------

resetButton.addEventListener(
    "click",
    resetApplication
);


function resetApplication() {

    selectedFile = null;

    fileInput.value = "";


    if (previewUrl) {

        URL.revokeObjectURL(
            previewUrl
        );

        previewUrl = null;
    }


    previewImage.src = "";

    fileName.textContent = "";

    prediction.textContent = "";

    confidence.textContent =
        "0%";

    confidenceFill.style.width =
        "0%";

    resultFileName.textContent =
        "";


    previewContainer.classList.add(
        "hidden"
    );


    result.classList.add(
        "hidden"
    );


    dropZone.classList.remove(
        "hidden"
    );


    clearError();
}


// --------------------------------------------------
// Error Handling
// --------------------------------------------------

function showError(message) {

    errorMessage.textContent =
        message;

    errorMessage.classList.remove(
        "hidden"
    );
}


function clearError() {

    errorMessage.textContent =
        "";

    errorMessage.classList.add(
        "hidden"
    );
}


// --------------------------------------------------
// Friendly Error Messages
// --------------------------------------------------

function getErrorMessage(error) {

    if (!error) {

        return "An unexpected error occurred.";
    }


    if (
        error instanceof TypeError &&
        error.message === "Failed to fetch"
    ) {

        return (
            "Unable to connect to FlowerVision AI. " +
            "Make sure the backend is running."
        );
    }


    return (
        error.message ||
        "Prediction failed. Please try again."
    );
}


// --------------------------------------------------
// Helper
// --------------------------------------------------

function capitalize(value) {

    if (!value) {
        return "";
    }


    return (
        value.charAt(0).toUpperCase() +
        value.slice(1)
    );
}