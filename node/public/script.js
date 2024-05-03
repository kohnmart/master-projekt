import { fetchImages, fetchBboxes, deleteBboxes } from './fetch.js';

const state = {
  images: [],
  currentIndex: 0,
};

const canvas = new fabric.Canvas('c', {
  isDrawingMode: false,
});

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

function enableRectangleDrawing() {
  const rect = new fabric.Rect({
    left: 250,
    top: 250,
    fill: 'transparent',
    width: 200,
    height: 200,
    stroke: 'red',
    strokeWidth: 1,
    selectable: true,
  });
  canvas.add(rect);
  canvas.setActiveObject(rect);
}

function clearCanvas() {
  canvas.getObjects().forEach((obj) => {
    if (obj.type === 'rect') canvas.remove(obj);
  });
}

function deleteFromCanvas() {
  deleteBboxes(state.images[state.currentIndex]);
}

const clear = document.getElementById('clearCanvas');
clear.addEventListener('click', deleteFromCanvas);

document
  .getElementById('addRectangle')
  .addEventListener('click', enableRectangleDrawing);

document.addEventListener('DOMContentLoaded', async () => {
  setupButtons(document.body);
  setupKeyboardNavigation();
  await loadImages();
  displayImage();
});

function setupButtons(body) {
  body.appendChild(createButton('Back', 'btn_back', prevImage));
  body.appendChild(createButton('Forward', 'btn_forward', nextImage));
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
    if (event.key === 'ArrowRight') nextImage();
    else if (event.key === 'ArrowLeft') prevImage();
    else if (event.key === 'ArrowDown') imageDelete();
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

async function loadBoundingBoxes() {
  try {
    const data = await fetchBboxes(state.images[state.currentIndex]);
    console.log(data['bboxes']);
    data['bboxes'].forEach((bbox) => {
      const rect = new fabric.Rect({
        left: bbox.left,
        top: bbox.top,
        width: bbox.width,
        height: bbox.height,
        fill: 'transparent',
        stroke: 'red',
        strokeWidth: 2,
      });
      canvas.add(rect);
      canvas.setActiveObject(rect);
    });
  } catch (err) {
    console.log(err);
  }
}

function displayImage() {
  loadImage(`images/${state.images[state.currentIndex]}`);
}

function nextImage() {
  state.currentIndex = (state.currentIndex + 1) % state.images.length;
  displayImage();
  clearCanvas();
  loadBoundingBoxes();
}

function prevImage() {
  state.currentIndex =
    (state.currentIndex - 1 + state.images.length) % state.images.length;
  displayImage();
  clearCanvas();
  loadBoundingBoxes();
}

async function saveBoundingBoxes() {
  try {
    const rectangles = canvas.getObjects().filter((obj) => obj.type === 'rect');
    if (rectangles.length !== 0) {
      const updatedRectangles = rectangles.map((rect) => ({
        id: rect.id,
        sample_id: rect.sample_id ?? state.images[state.currentIndex],
        type: rect.type,
        originX: rect.originX,
        originY: rect.originY,
        left: rect.left,
        top: rect.top,
        width: rect.width,
        height: rect.height,
        scaleX: rect.scaleX,
        scaleY: rect.scaleY,
      }));
      await axios.put('/canvas', { canvas: [updatedRectangles] });
    }
  } catch (error) {
    console.error('Error uploading rectangles:', error);
  }
}

document
  .getElementById('saveBBoxes')
  .addEventListener('click', saveBoundingBoxes);

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
