import {
  displayImage,
  nextImage,
  prevImage,
  imageDelete,
  loadImages,
  state,
} from './image.js';

import {
  canvas,
  deleteFromCanvas,
  enableRectangleDrawing,
  saveBoundingBoxes,
} from './canvas.js';

const sampleLengthTotalElement = document.createElement('p');
sampleLengthTotalElement.id = 'counter';
const clear = document.getElementById('clearCanvas');
clear.addEventListener('click', deleteFromCanvas);

document
  .getElementById('addRectangle')
  .addEventListener('click', enableRectangleDrawing);

document.addEventListener('DOMContentLoaded', async () => {
  setupKeyboardNavigation();
  addClothTypes();
  await loadImages();
  sampleLengthTotalElement.textContent = `0 / ${state.images.length}`;
  actions.appendChild(sampleLengthTotalElement);
  displayImage();
});

function setupKeyboardNavigation() {
  document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') nextImage();
    else if (event.key === 'ArrowLeft') prevImage();
    else if (event.key === 'ArrowDown') imageDelete();
  });
}
const clothButtons = [];
let btnBefore = null;
function addClothTypes() {
  const clothes = [
    'Jacket',
    'Shirt',
    'T-Shirt',
    'Polo',
    'Dress',
    'Pant',
    'Short',
    'Skirt',
    'Unkown',
  ];
  const actions = document.getElementById('actions');
  const div = document.createElement('div');
  div.id = 'cloth-types';

  clothes.forEach((cloth) => {
    const button = document.createElement('button');
    button.textContent = cloth;
    button.addEventListener('click', () => {
      if (btnBefore != null) {
        btnBefore.style.borderColor = 'lightgrey'; // Change to 'lightgrey'
      }
      button.style.borderColor = 'red';
      const rect = canvas.getActiveObject();
      rect.set({ label: cloth });
      canvas.renderAll();
      btnBefore = button;
    });
    div.appendChild(button);
    clothButtons.push(button);
  });

  actions.appendChild(div);
}

canvas.on('mouse:down', function (options) {
  if (options.target && options.target.type === 'rect') {
    const rect = options.target;
    const index = clothButtons.find((btn) => btn.textContent == rect.label);
    if (index) {
      if (btnBefore) {
        btnBefore.style.borderColor = 'lightgrey';
      }
      index.style.borderColor = 'red';
      btnBefore = index;
    }
  } else {
    btnBefore.style.borderColor = 'lightgrey';
  }
});

document
  .getElementById('saveBBoxes')
  .addEventListener('click', saveBoundingBoxes);
