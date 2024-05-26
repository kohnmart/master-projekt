const fs = require('fs');
const path = require('path');
const express = require('express');
const router = express.Router();

let sub_path = '';

router.get('/images/:id', (req, res) => {
  const cloth_class = req.params.id;
  sub_path = `../../dataset/${cloth_class}/train`;
  const imagesDir = path.join(__dirname, sub_path);
  try {
    // Read the contents of the directory
    const images = fs.readdirSync(imagesDir);
    res.json(images);
  } catch (error) {
    console.error('Error reading images directory:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Endpoint to delete an image
router.delete('/images/:imageName', (req, res) => {
  const imageName = req.params.imageName;
  const imagePath = path.join(__dirname, sub_path, imageName);
  fs.unlinkSync(imagePath); // Delete the image file
  res.sendStatus(200);
});
