const mongoose = require('mongoose')

const Schema = mongoose.Schema

const boundingSchema = new Schema({
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

exports.boundingSchema = boundingSchema;


