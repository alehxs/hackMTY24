let selectedFile = null;

function handleFileChange(event) {
    const file = event.target.files[0];
    const fileSizeLimit = 5 * 1024 * 1024; // 5 MB Limit
    const validTypes = ['image/jpeg', 'image/png'];

    const errorElement = document.getElementById('error');
    const fileNameElement = document.getElementById('fileName');
    const previewImageElement = document.getElementById('previewImage');
    const outputImageElement = document.getElementById('outputImage');
    const fileLabel = document.querySelector('.file-label');
    const labelTextElements = fileLabel.querySelectorAll('p');
    labelTextElements.forEach(text => text.style.display = 'none');

    // Reset error message
    errorElement.textContent = '';

    if (!file) return;

    // Validate file type
    if (!validTypes.includes(file.type)) {
        errorElement.textContent = "Only .jpg or .png files are allowed.";
        selectedFile = null;
        return;
    }

    // Validate file size
    if (file.size > fileSizeLimit) {
        errorElement.textContent = "File size exceeds the 5MB limit.";
        selectedFile = null;
        return;
    }

    // Set selected file and display file name and preview
    selectedFile = file;
    fileNameElement.textContent = file.name;

    // Show the image preview only when a valid image is selected
    previewImageElement.src = URL.createObjectURL(file);
    previewImageElement.style.display = 'block';  // Display the preview image
}

function handleSubmit() {
    const errorElement = document.getElementById('error');
    const outputImageElement = document.getElementById('outputImage');

    if (!selectedFile) {
        errorElement.textContent = "Please select a valid file.";
        return;
    }

    // FormData logic for file upload
    const formData = new FormData();
    formData.append('image', selectedFile);

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const imgUrl = URL.createObjectURL(blob);
        outputImageElement.src = imgUrl; // Display the predicted depth image
        outputImageElement.style.display = 'block'; // Show the predicted image
    })
    .catch(error => {
        errorElement.textContent = "Error uploading the file.";
        console.error('Upload error:', error);
    });
}

function redirectTo3DModel() {
    window.location.href = 'http://127.0.0.1:7860/';
}

function showChatbotText() {
    const chatbotTextElement = document.getElementById('chatbotText');
    chatbotTextElement.style.display = 'block'; // Make the text visible
}