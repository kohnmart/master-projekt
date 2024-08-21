import {
    displayImage,
    nextImage,
    prevImage,
    loadImages,
    state,
    imageDelete,
} from './image.js';

import {
    canvas,
    deleteFromCanvas,
    enableRectangleDrawing,
    saveBoundingBoxes,
} from './canvas.js';

import { getFolderStructure, putImageFileName } from './fetch.js';

const sampleLengthTotalElement = document.createElement('p');
sampleLengthTotalElement.id = 'counter';
const clear = document.getElementById('clearCanvas');
clear.addEventListener('click', deleteFromCanvas);

let counter = 0;

document
    .getElementById('addRectangle')
    .addEventListener('click', enableRectangleDrawing);

document.addEventListener('DOMContentLoaded', async () => {
    setupKeyboardNavigation();
    addClothTypes();
    //getFolderStructure();
    await loadImages();
    sampleLengthTotalElement.textContent = `0 / ${state.images.length}`;
    actions.appendChild(sampleLengthTotalElement);
    document.getElementById('file-name').textContent = state.images[counter];
    displayImage();
});

function setupKeyboardNavigation() {
    document.addEventListener('keydown', event => {
        if (event.key === 'ArrowRight') {
            nextImage();
            counter += 1;
            document.getElementById('file-name').textContent =
                state.images[counter];

            let name = state.images[counter - 1].split('_')[1];
            name = name.split('.')[0];

            document.getElementById(name).style.borderColor = 'lightgrey';

            name = state.images[counter].split('_')[1];
            name = name.split('.')[0];
            document.getElementById(name).style.borderColor = 'red';
        } else if (event.key === 'ArrowLeft') {
            prevImage();
            counter -= 1;
            document.getElementById('file-name').textContent =
                state.images[counter];

            let name = state.images[counter + 1].split('_')[1];
            name = name.split('.')[0];
            document.getElementById(name).style.borderColor = 'lightgrey';

            name = state.images[counter].split('_')[1];
            name = name.split('.')[0];
            document.getElementById(name).style.borderColor = 'red';
        } else if (event.key === 'Delete') {
            imageDelete();
        }
    });
}
const clothButtons = [];
let btnBeforeId = null;
function addClothTypes() {
    const clothes = [
        'dress',
        'skirt',
        'sweatshirt',
        'shirt',
        'short',
        'pant',
        'jacket',
        'poloshirt',
        't-shirt',
    ];
    const actions = document.getElementById('actions');
    const div = document.createElement('div');
    div.id = 'cloth-types';

    clothes.forEach(cloth => {
        const button = document.createElement('button');
        button.textContent = cloth;
        button.id = cloth;
        button.addEventListener('click', async () => {
            if (btnBeforeId != null) {
                document.getElementById(btnBeforeId).style.borderColor =
                    'lightgrey'; // Change to 'lightgrey'
            }
            button.style.borderColor = 'red';
            //const rect = canvas.getActiveObject();
            //rect.set({ label: cloth });

            let name = state.images[counter];

            let frame = name.split('_')[0];

            let new_name = frame + '_' + cloth + '.jpg';

            document.getElementById('file-name').textContent = new_name;

            canvas.renderAll();
            btnBeforeId = button.id;

            await putImageFileName(name, new_name);
            state.images[counter] = new_name;
        });
        div.appendChild(button);
        clothButtons.push(button);
    });

    actions.appendChild(div);
}

/*canvas.on('mouse:down', function (options) {
    if (options.target && options.target.type === 'rect') {
        const rect = options.target;
        const index = clothButtons.find(btn => btn.textContent == rect.label);
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
});*/

document
    .getElementById('saveBBoxes')
    .addEventListener('click', saveBoundingBoxes);
