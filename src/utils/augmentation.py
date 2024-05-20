from PIL import Image, ImageDraw
import numpy as np
import random 
def generate_random_aspect_ratio(min_ratio, max_ratio, original_area):
    # Calculate the minimum and maximum widths and heights based on the aspect ratio range
    min_width = ((min_ratio * original_area) ** 0.5)  # square root to get width from area
    max_width = ((max_ratio * original_area) ** 0.5)
    
    # Generate random width within the calculated range
    width = random.uniform(min_width, max_width)
    
    # Calculate height based on the aspect ratio
    height = width / random.uniform(min_ratio, max_ratio)
    
    aspect_ratio = width / height
    return aspect_ratio, width * height, width, height  # return aspect ratio, area, width, and height

def erase_pixels(image, x, y, width, height, noise_factor):
    draw = ImageDraw.Draw(image)
    noise_x = np.random.normal(scale=noise_factor, size=4)
    noise_y = np.random.normal(scale=noise_factor, size=4)
    draw.polygon([(x + noise_x[0], y + noise_y[0]),
                  (x + width + noise_x[1], y + noise_y[1]),
                  (x + width + noise_x[2], y + height + noise_y[2]),
                  (x + noise_x[3], y + height + noise_y[3])],
                 fill="white")

    return image

def erase_generator(path=None, image=None):
    # Example usage
    image = None
    if path:
        image = Image.open(path)  # Load your image here

    else: 
        image = image
    
    sub_area = image.width * image.height
    sub_area = sub_area * 0.2  # Calculate the original image area

    min_ratio = 0.5  # Example min aspect ratio
    max_ratio = 2.0  # Example max aspect ratio

    aspect_ratio, area, width, height = generate_random_aspect_ratio(min_ratio, max_ratio, sub_area)

    # Random position within the image bounds
    x = random.randint(0, image.width - int(width))
    y = random.randint(0, image.height - int(height))

    # Erase pixels within the generated rectangle
    return erase_pixels(image, x, y, int(width), int(height), noise_factor=50)