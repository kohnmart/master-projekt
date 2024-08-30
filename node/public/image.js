import { fetchImages, deleteBboxes } from './fetch.js';
import { clearCanvas, loadBoundingBoxes, canvas } from './canvas.js';

const state = {
    images: [],
    currentIndex: 0,
};

let counterElement = '';

function updateCounter() {
    counterElement.textContent = `${state.currentIndex + 1} / ${
        state.images.length
    }`;
}

function displayImage() {
    loadImage(`images/${state.images[state.currentIndex]}`);
    clearCanvas();
    updateCounter();
    // Uncomment if bounding boxes need to be loaded
    // loadBoundingBoxes(state.images[state.currentIndex]);
}

function nextImage() {
    state.currentIndex = (state.currentIndex + 1) % state.images.length;
    displayImage();
}

function prevImage() {
    state.currentIndex =
        (state.currentIndex - 1 + state.images.length) % state.images.length;
    displayImage();
}

async function imageDelete(imageName) {
    try {
        await axios.delete(`/images/${imageName}`);
        alert('Image deleted successfully!');
    } catch (error) {
        handleError('deleting image', error);
    }
}

function loadImage(url) {
    counterElement = document.getElementById('counter');
    fabric.Image.fromURL(url, img => {
        const imgScale = Math.min(
            canvas.width / img.width,
            canvas.height / img.height
        );
        img.scale(imgScale).set({ left: 10, top: 10, angle: 0 });
        canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
    });
}

async function loadImages() {
    try {
        state.images = await fetchImages();
        if (state.images.length > 0) {
            displayImage();
        } else {
            alert('No images found.');
        }
    } catch (error) {
        handleError('loading images', error);
    }
}

function handleError(action, error) {
    console.error(`Error ${action}:`, error);
    alert(`Error ${action}. Please try again.`);
}

export {
    displayImage,
    nextImage,
    prevImage,
    imageDelete,
    loadImage,
    loadImages,
    state,
};
