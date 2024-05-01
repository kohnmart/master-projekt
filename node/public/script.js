import { fetchImages } from "./fetch.js";

const state = {
    images: [],
    currentIndex: 0
};

document.addEventListener('DOMContentLoaded', async () => {
    const body = document.body;
    setupButtons(body);
    setupKeyboardNavigation();
    await loadImages();
    displayImage();
});

function setupButtons(body) {
    const backButton = createButton('Back', 'btn_back', prevImage);
    const forwardButton = createButton('Forward', 'btn_forward', nextImage);
    body.appendChild(backButton);
    body.appendChild(forwardButton);
}

function createButton(text, id, eventHandler) {
    const button = document.createElement('button');
    button.id = id;
    button.textContent = text;
    button.addEventListener('click', eventHandler);
    return button;
}

function setupKeyboardNavigation() {
    document.addEventListener('keydown', (event) => {
        if (event.key === "ArrowRight") {
            nextImage();
        } else if (event.key === "ArrowLeft") {
            prevImage();
        } else if (event.key === "ArrowDown") {
            imageDelete();
        }
    });
}

async function loadImages() {
    try {
        state.images = await fetchImages();
        console.log(state.images);
    } catch (error) {
        console.error('Failed to load images:', error);
    }
}

function displayImage() {
    const imageContainer = document.querySelector('.image-container');
    imageContainer.innerHTML = ''; // Clear the container
    const img = document.createElement('img');
    img.src = `images/${state.images[state.currentIndex]}`;
    img.classList.add('image-item');
    imageContainer.appendChild(img);
    updateImageCounter();
}

function updateImageCounter() {
    const text = document.getElementById('imagesCount') || document.createElement('p');
    text.id = 'imagesCount';
    text.innerHTML = `${state.currentIndex}/${state.images.length - 1}`;
    document.body.appendChild(text);
}

function nextImage() {
    state.currentIndex = (state.currentIndex + 1) % state.images.length;
    displayImage();
}

function prevImage() {
    state.currentIndex = (state.currentIndex - 1 + state.images.length) % state.images.length;
    displayImage();
}

async function imageDelete() {
    try {
        await axios.delete(`/images/${state.images[state.currentIndex]}`);
        state.images.splice(state.currentIndex, 1);
        if (state.images.length === 0) {
            alert('No more images available.');
            return;
        }
        nextImage();
        alert('Image deleted successfully!');
    } catch (error) {
        console.error('Error deleting image:', error);
        alert('Error deleting image. Please try again.');
    }
}
