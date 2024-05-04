import {
  displayImage,
  nextImage,
  prevImage,
  imageDelete,
  loadImages,
} from './image.js';

import {
  deleteFromCanvas,
  enableRectangleDrawing,
  saveBoundingBoxes,
} from './canvas.js';

const clear = document.getElementById('clearCanvas');
clear.addEventListener('click', deleteFromCanvas);

document
  .getElementById('addRectangle')
  .addEventListener('click', enableRectangleDrawing);

document.addEventListener('DOMContentLoaded', async () => {
  //setupButtons(document.body);
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

document
  .getElementById('saveBBoxes')
  .addEventListener('click', saveBoundingBoxes);
