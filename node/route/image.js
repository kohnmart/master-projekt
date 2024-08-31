// ./route/image.js
const fs = require('fs');
const path = require('path');
const express = require('express');
const router = express.Router();

let sub_path = '';

router.get('/images', (req, res) => {
    sub_path = path.join(
        __dirname,
        `../../src/pipeline/stream_extracted/setup-v2/recording_2024-08-52_base`
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

// Endpoint to rename an image
router.put('/images/:imageName', (req, res) => {
    const imageName = req.params.imageName;
    const newImageName = req.body.newImageName; // The new name should be provided in the request body
    const imagePath = path.join(sub_path, imageName);
    const newImagePath = path.join(sub_path, newImageName);

    fs.rename(imagePath, newImagePath, error => {
        if (error) {
            console.error('Error renaming image:', error);
            return res.status(500).json({ error: 'Internal server error' });
        }
        res.status(200).json({ message: 'Image renamed successfully' });
    });
});

module.exports = router;
