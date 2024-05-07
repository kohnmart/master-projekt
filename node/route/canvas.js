// routes/canvasRoutes.js
const express = require('express');
const router = express.Router();
const BoundingBox = require('../mongo/mongodb');

router.put('/canvas', async (req, res) => {
  const canvas = req.body.canvas;
  try {
    // Iterate over each bounding box
    BoundingBox.post(canvas[0]);
    // Respond with success message
    res.status(200).json({ message: 'Canvas data updated successfully' });
  } catch (error) {
    // If an error occurs, respond with an error message
    console.error('Error updating or creating canvas data:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.delete('/canvas/:id', async (req, res) => {
  try {
    // Iterate over each bounding box
    const sample_id = req.params.id;
    await BoundingBox.deleteAll(sample_id);

    // Respond with success message
    res.status(200).json({ message: 'All Bboxes deleted' });
  } catch (error) {
    // If an error occurs, respond with an error message
    console.error('Error updating or creating canvas data:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.get('/canvas/:id', async (req, res) => {
  try {
    // Iterate over each bounding box
    const sample_id = req.params.id;
    bboxes = await BoundingBox.getAll(sample_id);

    // Respond with success message
    res.status(200).json({ bboxes });
  } catch (error) {
    // If an error occurs, respond with an error message
    console.error('Error updating or creating canvas data:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.get('/canvas', async (req, res) => {
  try {
    // Iterate over each bounding box
    bboxes = await BoundingBox.getAllEntries();
    // Respond with success message
    res.status(200).json({ bboxes });
  } catch (error) {
    // If an error occurs, respond with an error message
    console.error('Error updating or creating canvas data:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
