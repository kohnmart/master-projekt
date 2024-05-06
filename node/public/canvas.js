import { fetchBboxes, deleteBboxes } from './fetch.js';
import { state } from './image.js';
const canvas = new fabric.Canvas('c', {
  isDrawingMode: false,
  width: 500,
  height: 500,
});

function enableRectangleDrawing() {
  const rect = new fabric.Rect({
    id: '',
    left: 0,
    top: 0,
    fill: 'transparent',
    width: 200,
    height: 200,
    stroke: 'red',
    strokeWidth: 1,
    selectable: true,
    label: '',
  });
  canvas.add(rect);
  canvas.setActiveObject(rect);
}

function clearCanvas() {
  canvas.getObjects().forEach((obj) => {
    canvas.remove(obj);
  });
}

function deleteFromCanvas() {
  deleteBboxes(state.images[state.currentIndex]);
  clearCanvas();
}

async function loadBoundingBoxes(sample_id) {
  try {
    const data = await fetchBboxes(sample_id);
    data['bboxes'].forEach((bbox) => {
      const rect = new fabric.Rect({
        id: bbox._id,
        left: bbox.left,
        top: bbox.top,
        width: bbox.width,
        height: bbox.height,
        scaleX: bbox.scaleX,
        scaleY: bbox.scaleY,
        fill: 'transparent',
        stroke: 'red',
        strokeWidth: 2,
        label: bbox.label,
      });
      canvas.add(rect);
      canvas.setActiveObject(rect);
    });
  } catch (err) {
    console.log(err);
  }
}

async function saveBoundingBoxes() {
  try {
    const rectangles = canvas.getObjects().filter((obj) => obj.type === 'rect');
    if (rectangles.length !== 0) {
      const updatedRectangles = rectangles.map((rect) => ({
        _id: rect.id,
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
        label: rect.label,
      }));
      await axios.put('/canvas', { canvas: [updatedRectangles] });
    }
  } catch (error) {
    console.error('Error uploading rectangles:', error);
  }
}

export {
  enableRectangleDrawing,
  clearCanvas,
  deleteFromCanvas,
  loadBoundingBoxes,
  saveBoundingBoxes,
  canvas,
};
