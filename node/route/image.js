// ./route/image.js
const fs = require('fs');
const path = require('path');
const express = require('express');
const router = express.Router();

let sub_path = '';

router.get('/images', (req, res) => {
  sub_path = path.join(
    __dirname,
    `../../dataset/classifier/train/recording_2024-07-05-9_base`
  );
  try {
    // Read the contents of the directory
    const images = fs.readdirSync(sub_path);
    res.json(images);
  } catch (error) {
    console.error('Error reading images directory:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Endpoint to delete an image
router.delete('/images/:imageName', (req, res) => {
  const imageName = req.params.imageName;
  const imagePath = path.join(sub_path, imageName);
  try {
    fs.unlinkSync(imagePath); // Delete the image file
    res.sendStatus(200);
  } catch (error) {
    console.error('Error deleting image:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
