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
    iou_score: 1.0,
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
  const rect = canvas.getActiveObject();
  deleteBboxes(rect.id);
  canvas.remove(rect);
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
        fill: 'transparent',
        stroke: 'red',
        strokeWidth: 2,
        label: bbox.label[0],
        iou_score: bbox.iou_score,
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
        left: rect.left,
        top: rect.top,
        width: rect.width * rect.scaleX.toFixed(2),
        height: rect.height * rect.scaleY.toFixed(2),
        label: rect.label,
        iou_score: 1.0,
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
