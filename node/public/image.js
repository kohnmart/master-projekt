import { fetchImages } from './fetch.js';
import { clearCanvas, loadBoundingBoxes, canvas } from './canvas.js';

const state = {
  images: [],
  currentIndex: 0,
};

function displayImage() {
  loadImage(`images/${state.images[state.currentIndex]}`);
}

function nextImage() {
  state.currentIndex = (state.currentIndex + 1) % state.images.length;
  displayImage();
  clearCanvas();
  loadBoundingBoxes(state.images[state.currentIndex]);
}

function prevImage() {
  state.currentIndex =
    (state.currentIndex - 1 + state.images.length) % state.images.length;
  displayImage();
  clearCanvas();
  loadBoundingBoxes(state.images[state.currentIndex]);
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

function loadImage(url) {
  fabric.Image.fromURL(url, function (img) {
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
    console.log(state.images);
  } catch (error) {
    console.error('Failed to load images:', error);
  }
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
