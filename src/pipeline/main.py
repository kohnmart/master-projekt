from sam import SAM
from clip import ClipClassifier
import numpy as np
import time
import pymongo
import uuid

print ('Connect to database...')

client = pymongo.MongoClient('mongodb+srv://mkohnle:Gni1Km1F0nWFXoNw@cluster0.t1akszl.mongodb.net/?retryWrites=true&w=majority')

# Access a database
db = client.detex_ai

# Access a collection
collection = db.boundingboxes

print ('Connected succesfully to database...')

print('Launching...')

sam_instance = SAM()
clip_instance = ClipClassifier()


print('Instance are setup...')

start_time = time.time()

file_names = []
indexes = [f'{i:04}' for i in range(17,22)]  # Generate index strings from '0000' to '0020'
for index in indexes:
    file_names.append(f"mixed_{index}.png")


for sample in file_names:

    print(f"Processing: {sample}")

    masks, image = sam_instance.image_processor(sample)
    cleaned_masks = sam_instance.clean_masks(masks, range=[10000, 200000])

    cloth_objects, cleaned_compared_masks = sam_instance.separate_by_bbox(cleaned_masks, image, True, True)
    

    probs = []
    
    for cloth in cloth_objects:
        clip_instance.image = cloth

        res = clip_instance.classifier()
        probs.append(res)


    for mask in cleaned_masks:
        result = collection.insert_one({
            '_id': str(uuid.uuid4()),
            'sample_id': sample,
            'type': 'rect',
            'left': mask['bbox'][0],
            'top': mask['bbox'][1],
            'width': mask['bbox'][2],
            'height': mask['bbox'][3],
            'label': res,
            'iou_score': mask['predicted_iou'],
        })

        if result.acknowledged:
            print("Insertion successful")
            print("Inserted document ID:", result.inserted_id)
        else:
            print("Insertion failed")

    sam_instance.save_sample_with_bboxes(cleaned_compared_masks, image, sample, probs)


end_time = time.time()

elapsed_time = end_time - start_time
formatted_elapsed_time = "{:.2f}".format(elapsed_time)

print("Elapsed time:", formatted_elapsed_time, "seconds")