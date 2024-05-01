const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();

app.use(express.static('public')); // Serve static files from the 'public' directory
app.use('/images', express.static(path.join(__dirname, '../dataset/generator/output')));
// Endpoint to get the list of images
app.get('/images', (req, res) => {
    const images = fs.readdirSync('../dataset/generator/output/');
    res.json(images);
});

// Endpoint to delete an image
app.delete('/images/:imageName', (req, res) => {
    const imageName = req.params.imageName;
    const imagePath = path.join(__dirname, '../dataset/generator/output/', imageName);

    fs.unlinkSync(imagePath); // Delete the image file
    res.sendStatus(200);
});

const server = app.listen(3000, () => {
    const address = server.address(); // Get the server's address information
    const host = address.address;
    const port = address.port;

    console.log(`Server is running at http://${host}:${port}`);
});