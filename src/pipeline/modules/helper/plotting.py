import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, precision_score, recall_score


def plot_images(images, filenames, foldername, cols=3):
    n_images = len(images)
    rows = (n_images // cols) + 1
    fig = plt.figure(figsize=(15, 5 * rows))
    
    for i, (img, filename) in enumerate(zip(images, filenames)):
        ax = fig.add_subplot(rows, cols, i + 1)
        ax.imshow(img)
        ax.set_title(filename, fontsize=10)
        ax.axis('off')  # Hide axes
    plt.tight_layout()
    save_file_name = foldername + '/all_plt.png'
    plt.savefig(save_file_name)


def generate_and_plot_conf(true_labels, predicted_labels, classes, full_path):
    # Calculate the confusion matrix
    cm = confusion_matrix(true_labels, predicted_labels, labels=classes)

    # Calculate accuracy, precision, and recall
    accuracy = accuracy_score(true_labels, predicted_labels)
    # precision = precision_score(true_labels, predicted_labels, average='macro')
    # recall = recall_score(true_labels, predicted_labels, average='macro')

    # Display the confusion matrix
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
    fig, ax = plt.subplots(figsize=(10, 10))
    disp.plot(cmap=plt.cm.Blues, xticks_rotation='vertical', ax=ax)

    # Add accuracy, precision, and recall to the plot
    ax.text(0.5, -0.2, f'Accuracy: {accuracy:.2f}', transform=ax.transAxes, fontsize=12, verticalalignment='top', horizontalalignment='center')

    plt.title("Confusion Matrix for Multi-Class Classification")
    plt.savefig(f"{full_path}/confusion_matrix.png")

    print("Conf matrix saved...")