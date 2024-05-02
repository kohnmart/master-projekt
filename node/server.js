const express = require('express');
const fs = require('fs');
const path = require('path');
const mongoose = require('mongoose')

const boundingSchema = new mongoose.Schema({
    _id: { type: String, required: true },  // Use UUID v4 as default value for _id
    type: { type: String, required: true },
    originX: { type: String, required: true },
    originY: { type: String, required: true },
    left: { type: Number, required: true },
    top: { type: Number, required: true },
    width: { type: Number, required: true },
    height: { type: Number, required: true },
    scaleX: { type: Number, required: true },
    scaleY: { type: Number, required: true }
  }, { timestamps: true});  // Enable timestamps for createdAt and updatedAt

// Create a model from the schema
const BoundingBox = mongoose.model('BoundingBox', boundingSchema);

const app = express();

app.use(express.json());

app.use(express.static('public')); // Serve static files from the 'public' directory

app.use('/images', express.static(path.join(__dirname, '../dataset/generator/output')));
// Endpoint to get the list of images
app.get('/images', (req, res) => {
    const images = fs.readdirSync('../dataset/generator/output/');
    res.json(images);
});

app.post('/canvas', (req, res) => {
    const canvData = req.body.canvas;
    console.log(canvData)
})

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

const uri = "mongodb+srv://mkohnle:Gni1Km1F0nWFXoNw@cluster0.t1akszl.mongodb.net/?retryWrites=true&w=majority";

async function run() {
  try {
    // Connect to MongoDB through Mongoose
    await mongoose.connect(uri, { dbName: 'detex-ai', useNewUrlParser: true, useUnifiedTopology: true });
    console.log("Connected to MongoDB");

    await createBounding();  // Create and save a bounding box

    // Since `createBounding` saves the document, you don't need to log `bboxes` as a collection object
    // If you want to fetch and log all bounding boxes, use:
    const bboxes = await BoundingBox.find({});
    console.log('All bounding boxes:', bboxes);
  } catch (error) {
    console.error('Error in running the operation:', error);
  } finally {
    // Ensures that the connection will close when you finish/error
    await mongoose.connection.close();
    console.log("MongoDB connection closed");
  }
}

run().catch(console.dir);

async function createBounding() {
  try {
    const rectData = {
      _id: 'testads',
      type: 'rect',
      originX: 'left',
      originY: 'top',
      left: 100,
      top: 200,
      width: 500,
      height: 300,
      scaleX: 1,
      scaleY: 1
    };
    const bounding = new BoundingBox(rectData);
    console.log(bounding)
    await bounding.save();
    console.log('Rectangle saved:', bounding);
  } catch (error) {
    console.error('Error saving rectangle:', error);
  }
}

