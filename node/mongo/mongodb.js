const mongoose = require('mongoose');
const uuid = require('uuid');
const boundingSchema = new mongoose.Schema(
  {
    _id: { type: String, required: true }, // Use UUID v4 as default value for _id
    sample_id: { type: String, required: true },
    type: { type: String, required: true },
    left: { type: Number, required: true },
    top: { type: Number, required: true },
    width: { type: Number, required: true },
    height: { type: Number, required: true },
    label: { type: Array, required: true },
    iou_score: { type: Number, required: false },
  },
  { timestamps: true }
); // Enable timestamps for createdAt and updatedAt

const URI =
  'mongodb+srv://mkohnle:Gni1Km1F0nWFXoNw@cluster0.t1akszl.mongodb.net/?retryWrites=true&w=majority';

// Create a model from the schema
const Model = mongoose.model('BoundingBox', boundingSchema);

const post = async (bboxes) => {
  try {
    await mongoose.connect(URI, {
      dbName: 'detex_ai',
    });
    console.log(bboxes);
    console.log('Connected to MongoDB');

    for (const bbox of bboxes) {
      let boundingBox;
      if (bbox._id != '') {
        boundingBox = await Model.findByIdAndUpdate(bbox._id, bbox, {
          new: true,
        });
      } else {
        bbox._id = uuid.v4();
        boundingBox = new Model(bbox);
      }

      await boundingBox.save();
    }
  } catch (error) {
    console.error('Error:', error);
  } finally {
    await mongoose.disconnect();
    console.log('Disconnected from MongoDB');
  }
};

const deleteAll = async (sample_id) => {
  try {
    await mongoose.connect(URI, {
      dbName: 'detex_ai',
    });

    const res = await Model.deleteMany({ sample_id: sample_id });
    console.log(res.deletedCount, 'documents deleted');
  } catch (err) {
    console.log('Error on Delete', err);
  } finally {
    await mongoose.connection.close();
  }
};

const deleteSingle = async (_id) => {
  try {
    await mongoose.connect(URI, {
      dbName: 'detex_ai',
    });

    const res = await Model.deleteMany({ _id: _id });
    console.log(res.deletedCount, 'documents deleted');
  } catch (err) {
    console.log('Error on Delete', err);
  } finally {
    await mongoose.connection.close();
  }
};

const getAll = async (sample_id) => {
  try {
    await mongoose.connect(URI, {
      dbName: 'detex_ai',
    });

    const res = await Model.find({ sample_id: sample_id });
    return res;
  } catch (err) {
    console.error('Error fetching all rectangles:', err);
  } finally {
    await mongoose.connection.close();
  }
};

const getAllEntries = async () => {
  try {
    await mongoose.connect(URI, {
      dbName: 'detex_ai',
    });

    const res = await Model.find().toArray();
    return res;
  } catch (err) {
    console.error('Error fetching all rectangles:', err);
  } finally {
    await mongoose.connection.close();
  }
};

module.exports = {
  Model,
  post,
  getAll,
  getAllEntries,
  deleteAll,
  deleteSingle,
};
