const fs = require('fs');
const path = require('path');
const express = require('express');
const router = express.Router();

const getFolderStructure = (dirPath) => {
  const structure = {};
  const files = fs.readdirSync(__dirname);
  files.forEach((file) => {
    const filePath = path.join(dirPath, file);
    const stats = fs.statSync(filePath);
    if (stats.isDirectory()) {
      structure[file] = getFolderStructure(filePath);
    }
  });
  return structure;
};

// Endpoint to get the folder structure
router.get('/struct/folder-structure', (req, res) => {
  const structure = getFolderStructure(path.join(__dirname, 'public'));
  console.log('test');
  res.json(structure);
});

module.exports = router;
