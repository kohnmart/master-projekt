
from modules.helper import rotation_image_proper
from transformers import CLIPProcessor, CLIPModel
import torch
import clip
from PIL import Image
class ClipClassifier: 

    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.image = None

    def predictor(self, text_prompt):
        inputs = self.processor(text=text_prompt, images=self.image, return_tensors="pt", padding=True)
        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image 
        return logits_per_image.softmax(dim=1) 
   
    def get_label(self, probs, classes):
        res_list = []
        for i, prob in enumerate(probs[0]):
            res_list.append([classes[i], prob.item()])
        res_list.sort(key=lambda x: x[1], reverse=True)
        print("RES: " + str(res_list[0]))
        return res_list[0]

    def classifier(self):
        
        probs = self.predictor(['a photo a upper body cloth type', 'a photo of a lower body cloth type'])
        if probs[0][0].item() < probs[0][1].item():
            probs = self.predictor(['a photo of a short pants', 'a photo of a long pants', 'a photo of a skirt'])
            res = self.get_label(probs, ['short', 'pant', 'skirt'])

        else: 
            probs = self.predictor(['a photo of a short-sleeve top', 'a photo of a long-sleeve top'])
            if probs[0][0].item() > probs[0][1].item():
                probs = self.predictor(['a photo of a t-shirt', 'a photo of a polo-shirt', 'a photo of a dress'])
                res = self.get_label(probs, ['t-shirt', 'polo', 'dress'])

            else:
                probs = self.predictor(['a photo of a sweatshirt', 'a photo of a jacket'])
                res = self.get_label(probs, ['shirt', 'jacket'])
        return res



# Reference : https://github.com/openai/CLIP

class ClipFast: 

    """
    model_name: ["RN50", "RN101", "RN50x4", "RN50x16", "ViT-B/14", "ViT-B/16", "ViT-B/32"]

    """

    def __init__(self, model_name):
        clip_model = model_name 
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(clip_model, device=self.device, jit=False)
        self.classes =  ['dress', 'skirt', 'jacket', 'shirt', 'tshirt', 'pant', 'short']
        self.classes_prompt = [f'a photo of a {cl}' for cl in self.classes]

    def rotate_wise(self, image):
        rot_accuracy = []

        for i in range(0,4):
            rot_frame_rgb = rotation_image_proper(image, -90*i)
            res = self.process(rot_frame_rgb)
            rot_accuracy.append(res)

        # Initialize an empty list to store unique items
        unique_items = []

        # Initialize an empty set to track items that have already been added
        seen_items = set()

        # Loop through each item and add it to the list if it's not a duplicate
        for item in rot_accuracy:
            if item[0] not in seen_items:
                unique_items.append(item[0])
                seen_items.add(item[0])

        # Print the resulting list of unique items
        item_list = []
        for u_item in unique_items:
            ls = [item for item in rot_accuracy if u_item in item]
            item_list.append(ls)

        # Initialize a dictionary to store sums and counts for each type
        sums_counts = {}

        # Iterate through the nested list to update sums and counts
        for sublist in item_list:
            for item in sublist:
                item_type = item[0]
                value = item[1]
                
                if item_type not in sums_counts:
                    sums_counts[item_type] = {'sum': 0, 'count': 0}
                
                sums_counts[item_type]['sum'] += value
                sums_counts[item_type]['count'] += 1

        # Calculate the averages
        averages = {}
        for item_type, values in sums_counts.items():
            averages[item_type] = values['sum'] / values['count']

        # Print the resulting averages
        #print(averages)
        max_item_type = max(averages, key=averages.get)
        return max_item_type


    def process(self, image):
        
        image = Image.fromarray(image)

        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        self.classes_prompt = [f'a photo of a {cl}' for cl in self.classes]
        text = clip.tokenize(self.classes_prompt).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            text_features = self.model.encode_text(text)

        
        # Pick the top 5 most similar labels for the image
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        values, indices = similarity[0].topk(2)


        # Print the result
        #print("\nTop predictions:\n")
        highest_value = -1
        highest_pair = None
        highest_index = -1

        paired_listing = []

        # Combine values and indices
        paired = list(zip(values, indices))

        # Sort pairs by the first element (value)
        sorted_paired = sorted(paired, key=lambda x: x[0], reverse=True)

        # Iterate through the sorted pairs
        for value, index in sorted_paired:
            print(f"Value: {value}, Index: {self.classes[index]}")
            paired_listing.append([self.classes[index], value.item()])

        highest_pair = paired_listing[0]

        print("Highest Pair")
        print(highest_pair)

        # Return the highest value pair
        return highest_pair

                