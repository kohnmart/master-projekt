from sam import SAM
from clip import ClipClassifier

print('Launching...')

sam_instance = SAM()
clip_instance = ClipClassifier()

print('Instance are setup...')

file_names = []
indexes = [f'{i:04}' for i in range(4,21)]  # Generate index strings from '0000' to '0020'
for index in indexes:
    file_names.append(f"mixed_{index}.png")


for sample in file_names:

    print(f"Processing: {sample}")

    masks, image = sam_instance.image_processor(sample)

    print('Image processed...')

    cleaned_masks = sam_instance.clean_masks(masks)


    print('Masks cleaned...')

    cloth_objects = sam_instance.separate_by_bbox(cleaned_masks, image)


    print('Image classifying...')


    probs =[]
    for cloth in cloth_objects:
        clip_instance.image = cloth

        res = clip_instance.classifier()
        probs.append(res)


    sam_instance.show_sample_with_bboxes(cleaned_masks, image, sample, probs)

