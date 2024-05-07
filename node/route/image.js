const fs = require('fs');
const path = require('path');
const express = require('express');
const router = express.Router();

router.get('/images', (req, res) => {
  const imagesDir = path.join(__dirname, '../../dataset/generator/output/');
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
  const imagePath = path.join(
    __dirname,
    '../../dataset/generator/output/',
    imageName
  );
  fs.unlinkSync(imagePath); // Delete the image file
  res.sendStatus(200);
});

module.exports = router;
