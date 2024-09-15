import numpy as np

class ClothingSimilarity:

    # Define the class similarity matrices as class variables (static)
    all_classes_matrix = np.array([
        [1.0, 0.8, 0.2, 0.3, 0.1, 0.1, 0.3, 0.2, 0.2],  # Dress
        [0.8, 1.0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.1, 0.1],  # Skirt
        [0.2, 0.1, 1.0, 0.5, 0.2, 0.3, 0.7, 0.5, 0.4],  # Sweatshirt
        [0.3, 0.2, 0.5, 1.0, 0.2, 0.2, 0.4, 0.8, 0.7],  # Shirt
        [0.1, 0.1, 0.2, 0.2, 1.0, 0.7, 0.2, 0.2, 0.2],  # Short
        [0.1, 0.1, 0.3, 0.2, 0.7, 1.0, 0.3, 0.2, 0.2],  # Pant
        [0.3, 0.2, 0.7, 0.4, 0.2, 0.3, 1.0, 0.4, 0.3],  # Jacket
        [0.2, 0.1, 0.5, 0.8, 0.2, 0.2, 0.4, 1.0, 0.7],  # Poloshirt
        [0.2, 0.1, 0.4, 0.7, 0.2, 0.2, 0.3, 0.7, 1.0]   # T-shirt
    ])

    high_level_matrix = np.array([
        [1.0, 0.3, 0.2, 0.2],  # Dress
        [0.5, 1.0, 0.4, 0.6],  # Shirt
        [0.4, 0.4, 1.0, 0.3],  # Pant
        [0.1, 0.5, 0.1, 1.0]   # Jacket
    ])

    upperwear_matrix = np.array([
        [1.0, 0.5, 0.8, 0.4],  # Shirt
        [0.5, 1.0, 0.6, 0.4],  # Sweatshirt
        [0.8, 0.6, 1.0, 0.7],  # Poloshirt
        [0.4, 0.4, 0.7, 1.0]   # T-shirt
    ])

    underwear_matrix = np.array([
        [1.0, 0.7, 0.2],  # Pant
        [0.2, 1.0, 0.7],  # Short
        [0.2, 0.7, 1.0]   # Skirt
    ])

    @staticmethod
    def get_weighted_accuracy(true_class_index, classes, result, similarity_matrix) -> list:

        predicted_probs = np.zeros(len(classes))

        for prediction in result:
            class_name, probability = prediction
            class_index = classes.index(class_name)  # Find the index of the class in the classes list
            predicted_probs[class_index] = probability

        temp_weights = []

        for i in range(0, len(classes)):
            # Retrieve the similarity scores for the true class
            similarity_scores = similarity_matrix[i]

            # Calculate the weighted accuracy
            weighted_accuracy = np.dot(predicted_probs, similarity_scores)

            temp_weights.append([classes[i], weighted_accuracy])
        
        # Sort the results by weighted accuracy in descending order
        sorted_paired = sorted(temp_weights, key=lambda x: x[1], reverse=True)

        return sorted_paired
