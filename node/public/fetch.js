const fetchImages = async () => {
  try {
    const response = await axios.get('/images');
    return response.data;
  } catch (error) {
    console.error('Error fetching images:', error);
    alert('Error fetching images. Please try again.');
  }
};

const fetchBboxes = async (id) => {
  try {
    const url = `/canvas/${id}`;
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching images:', error);
    alert('Error fetching images. Please try again.');
  }
};

const fetchAllBboxes = async (id) => {
  try {
    const url = `/canvas`;
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching images:', error);
    alert('Error fetching images. Please try again.');
  }
};

const deleteBboxes = async (id) => {
  try {
    const url = `/canvas/${id}`;
    const response = await axios.delete(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching images:', error);
    alert('Error fetching images. Please try again.');
  }
};

export { fetchImages, fetchBboxes, deleteBboxes, fetchAllBboxes };
