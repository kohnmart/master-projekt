
const fetchImages = async () =>  {
    try {
        const response = await axios.get('/images');
        return response.data;
                
    } catch (error) {
        console.error('Error fetching images:', error);
        alert('Error fetching images. Please try again.');
    }
}

export {fetchImages}