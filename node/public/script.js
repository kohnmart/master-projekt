import {
    displayImage,
    nextImage,
    prevImage,
    loadImages,
    state,
    imageDelete,
} from './image.js';

import { saveBoundingBoxes } from './canvas.js';

import { putImageFileName } from './fetch.js';

const sampleLengthTotalElement = document.createElement('p');
sampleLengthTotalElement.id = 'counter';

let counter = 0;

document
    .getElementById('deleteMarker')
    .addEventListener('click', markForDeletion);

document
    .getElementById('deleteAll')
    .addEventListener('click', deleteMarkedStorage);

document.addEventListener('DOMContentLoaded', async () => {
    addClothTypes();
    //getFolderStructure();
    await loadImages();
    setupKeyboardNavigation();
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

            let old_name = state.images[counter - 1].split('_')[1];
            old_name = old_name.split('.')[0];
            document.getElementById(old_name).style.borderColor = 'lightgrey';

            let new_name = state.images[counter].split('_')[1];
            new_name = new_name.split('.')[0];
            document.getElementById(new_name).style.borderColor = 'red';
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
                    'lightgrey';
            }
            button.style.borderColor = 'red';

            let name = state.images[counter];

            let frame = name.split('_')[0];

            let new_name = frame + '_' + cloth + '.jpg';

            document.getElementById('file-name').textContent = new_name;

            //canvas.renderAll();
            btnBeforeId = button.id;

            await putImageFileName(name, new_name);
            state.images[counter] = new_name;
        });
        div.appendChild(button);
        clothButtons.push(button);
    });

    actions.appendChild(div);
}

let delStorage = [];

function markForDeletion() {
    console.log(state.images[state.currentIndex]);
    delStorage.push(state.images[state.currentIndex]);
}

function deleteMarkedStorage() {
    delStorage.forEach(imageName => {
        imageDelete(imageName);
    });
}

document
    .getElementById('saveBBoxes')
    .addEventListener('click', saveBoundingBoxes);
