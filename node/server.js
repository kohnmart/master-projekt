const express = require('express');
const path = require('path');
const imageRoutes = require('./route/image');
const canvasRoutes = require('./route/canvas');
const app = express();

app.use(express.json());

app.use(express.static('public'));

app.use(
  '/images',
  express.static(path.join(__dirname, '../dataset/segmentator/output'))
);

app.use(imageRoutes);
app.use(canvasRoutes);

const server = app.listen(3000, () => {
  const address = server.address(); // Get the server's address information
  const host = address.address;
  const port = address.port;
  console.log(`Server is running at http://${host}:${port}`);
});
