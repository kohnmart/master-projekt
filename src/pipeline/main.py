from sam import SAM
from clip import ClipClassifier

print('Launching...')

sam_instance = SAM()
clip_instance = ClipClassifier()

print('Instance are setup...')

files = ['mixed_0016.png', 'mixed_0019.png']


for sample in files:

    print(f"Processing: {sample}")

    masks, image = sam_instance.image_processor(sample)

    print('Image processed...')

    cleaned_masks = sam_instance.clean_masks(masks)


    print('Masks cleaned...')
    print(len(cleaned_masks))

    cloth_objects = sam_instance.separate_by_bbox(cleaned_masks, image)

    sam_instance.show_sample_with_bboxes(cleaned_masks, image, sample)

    print('Image classifying...')


    for cloth in cloth_objects:
        clip_instance.image = cloth
        print(cloth.shape)
        res = clip_instance.classifier()
        print(res)



