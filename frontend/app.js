"use strict";


// --------------------------------------------------
// Configuration
// --------------------------------------------------

const API_URL =
    "http://127.0.0.1:8000/api/v1/predict";


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
// Handle File
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


    // Revoke previous preview URL.

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
// Prediction
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


        const data =
            await response.json();


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
            "Prediction error:",
            error
        );


        showError(
            error.message ||
            "Unable to connect to FlowerVision AI."
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
// Reset
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

    errorMessage.textContent = "";

    errorMessage.classList.add(
        "hidden"
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