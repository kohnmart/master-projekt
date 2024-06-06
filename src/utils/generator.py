from fastai.vision.all import *

from config.paths import PATH_TO_PROCESSED_V1, PATH_TO_PROCESSED_V2, PATH_TO_EVAL

def generator_setup(min_zoom, max_zoom, max_rotate, path):
    # Define image augmentations
    aug_transforms_list = aug_transforms(size=224, 
                                        max_rotate=max_rotate, 
                                        do_flip=True,
                                        min_zoom=min_zoom,
                                        pad_mode='border',
                                        max_zoom=max_zoom
                                        )

    # Define data loading and preprocessing pipeline using DataBlock
    dblock = DataBlock(blocks=(ImageBlock, CategoryBlock),
                    get_items=get_image_files,
                    splitter=RandomSplitter(valid_pct=0.2, seed=42),
                    get_y=parent_label,
                    item_tfms=Resize(224), 
                    batch_tfms=aug_transforms_list)


    return dblock.dataloaders(path, bs=64, num_workers=0)


def generator_setup_eval(path, min_zoom, max_zoom, batch_size, max_rotate):
    # Define image augmentations
    aug_transforms_list = aug_transforms(size=224, 
                                        max_rotate=max_rotate, 
                                        do_flip=True,
                                        min_zoom=min_zoom,
                                        pad_mode='border',
                                        max_zoom=max_zoom
                                        )

    # Define data loading and preprocessing pipeline using DataBlock
    dblock = DataBlock(blocks=(ImageBlock, CategoryBlock),
                    get_items=get_image_files,
                    get_y=parent_label,
                    item_tfms=Resize(224), 
                    batch_tfms=aug_transforms_list)

        # Create DataLoaders
    # Create DataLoaders
    return dblock.dataloaders(path, bs=batch_size, num_workers=0)




def setup(model_name, props):

    path = os.path.join(PATH_TO_EVAL, model_name)
    os.makedirs(path)

    # Specify the file path where you want to save the YAML file
    file_path = 'props.yaml'

    # Save the props dictionary to the YAML file
    with open(file_path, 'w') as yaml_file:
        yaml.dump(props, yaml_file, default_flow_style=False)