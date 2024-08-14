from fastai.vision.all import *
import matplotlib.pyplot as plt
import os
from sklearn.metrics import confusion_matrix
import seaborn as sns




def generator_setup_eval(path, min_zoom, max_zoom, batch_size):
    # Define image augmentations
    aug_transforms_list = aug_transforms(size=224)

    # Define data loading and preprocessing pipeline using DataBlock
    dblock = DataBlock(blocks=(ImageBlock, CategoryBlock),
                    get_items=get_image_files,
                    get_y=parent_label,
                    item_tfms=Resize(224), 
                    batch_tfms=aug_transforms_list)

        # Create DataLoaders
    # Create DataLoaders
    return dblock.dataloaders(path, bs=batch_size, num_workers=0)


def run_test_on_conf(dls, learn):
    true_labels = []
    predicted_labels = []   

    for batch in dls.train:

        images, labels = batch

        num_samples = min(dls.bs, len(images))

        for i in range(num_samples):
            img = images[i]
            img = img.cpu()
            # Make predictions on the image
            img = img[None]  # Add an extra dimension for batch size
            prediction = learn.get_preds(dl=[(img,)])[0][0]  # Predict for a single image
            predicted_class = prediction.argmax() 
            true_labels.append(labels[i])
            predicted_labels.append(predicted_class)

    return true_labels, predicted_labels


def create_test_conf(model_to_load, dls, class_names, save_plot, props):
    
    path_to_model = model_to_load

    # Collect true and predicted labels for all classes
    learn = load_learner(path_to_model)

    true_labels, predicted_labels = run_test_on_conf(dls, learn)

    # Convert lists of tensors to a single tensor
    true_labels = torch.stack(true_labels)
    predicted_labels = torch.stack(predicted_labels)

    # Move tensors to the CPU and convert to numpy arrays
    true_labels = true_labels.cpu().numpy()
    predicted_labels = predicted_labels.cpu().numpy()

    # Compute the overall confusion matrix
    overall_cm = confusion_matrix(true_labels, predicted_labels)

    # Sum of diagonal elements (correct predictions)
    correct_predictions = np.trace(overall_cm)

    # Sum of all elements in the confusion matrix (total predictions)
    total_predictions = np.sum(overall_cm)

    # Compute accuracy
    accuracy = correct_predictions / total_predictions

    # Display the overall confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(overall_cm, annot=False, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title(f'Confusion Matrix: Acc.: {accuracy * 100:.2f}%', pad=2.0)

    plt.subplots_adjust(hspace=1.0, wspace=0.7)
    plt.tight_layout(pad=1.0)

    save_path = './output'
    full_path = os.path.join(save_path, f"conf_test_{dls.bs}_{props['min_zoom']}_{props['max_zoom']}_{props['max_rotate']}.png")  # Updated filename
    if save_plot:
        plt.savefig(full_path)  # Save the figure as a PNG image
    return full_path