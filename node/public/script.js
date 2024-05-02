import { fetchImages } from "./fetch.js";

const state = {
    images: [],
    currentIndex: 0
};

const canvas = new fabric.Canvas('c', {
    isDrawingMode: true
  });
  

  // Function to load an image onto the canvas
function loadImage(url) {
    fabric.Image.fromURL(url, function(img) {
      // Scale image to fit canvas if it's too large
      const imgScale = Math.min(
        canvas.width / img.width,
        canvas.height / img.height
      );
      img.scale(imgScale).set({
        left: 10,
        top: 10,
        angle: 0
      });
      canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
    });
  }

  // Function to enable rectangle drawing mode
function enableRectangleDrawing() {
    canvas.isDrawingMode = false; // Disable free drawing mode
    const rect = new fabric.Rect({
      left: 50,
      top: 50,
      fill: 'transparent',
      width: 100,
      height: 100,
      stroke: 'red',
      strokeWidth: 1,
      selectable: true
    });
  
    canvas.add(rect);
    canvas.setActiveObject(rect);
  }

  function saveRectangles() {
    const rectangles = canvas.getObjects().filter(obj => obj.type === 'rect');
    console.log(rectangles);
  }

const saveBboxes = document.getElementById('saveBBoxes')
saveBboxes.addEventListener('click', saveRectangles)


  // Optional: function to clear all shapes
function clearCanvas() {
    canvas.getObjects().forEach((obj) => {
      if (obj.type === 'rect') {
        canvas.remove(obj);
      }
    });
  }
  
const clear = document.getElementById('clearCanvas')
clear.addEventListener('click', clearCanvas)


  
  // Function to toggle drawing mode
  function toggleDrawingMode() {
    canvas.isDrawingMode = !canvas.isDrawingMode;
    if (canvas.isDrawingMode) {
      // Set drawing properties if necessary
      canvas.freeDrawingBrush.color = 'blue';
      canvas.freeDrawingBrush.width = 5;
      console.log('Free drawing mode activated.');
    } else {
      console.log('Drawing mode deactivated.');
    }
  }
document.getElementById('addRectangle').addEventListener('click', enableRectangleDrawing);
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
    loadImage(`images/${state.images[state.currentIndex]}`)
}

function updateImageCounter() {
    const text = document.getElementById('imagesCount') || document.createElement('p');
    text.id = 'imagesCount';
    text.innerHTML = `${state.currentIndex}/${state.images.length - 1}`;
    document.body.appendChild(text);
}

function nextImage() {

    uploadBBoxes()
    state.currentIndex = (state.currentIndex + 1) % state.images.length;
    displayImage();
    clearCanvas()
}

function prevImage() {
    state.currentIndex = (state.currentIndex - 1 + state.images.length) % state.images.length;
    displayImage();
    uploadBBoxes()
    clearCanvas()
}

async function uploadBBoxes() {
  try {
    // Filter only rectangle objects from the canvas
    var rectangles = canvas.getObjects().filter(obj => obj.type === 'rect');
    if (rectangles.length != 0)
    {
    const updatedRectangles = rectangles.map(rect => ({
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
  
    // Post the data to the server
    await axios.post('/canvas', { canvas: [state.images[state.currentIndex], updatedRectangles] });
}
  } catch (error) {
    // Log or handle errors
    console.error('Error uploading rectangles:', error);
  }
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
