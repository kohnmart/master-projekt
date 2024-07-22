
from modules.helper import rotation_image_proper
from transformers import CLIPProcessor, CLIPModel
import torch
import clip
from PIL import Image


# Reference : https://github.com/openai/CLIP

class ClipFast: 

    """
    model_name: ["RN50", "RN101", "RN50x4", "RN50x16", "ViT-B/14", "ViT-B/16", "ViT-B/32"]

    """

    def __init__(self, model_name):
        clip_model = model_name 
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(clip_model, device=self.device, jit=False)


    def process_on_rotation(self, image, rotation_amount=4):

        rot_accuracy = []

        for i in range(0, rotation_amount):
            rot_frame_rgb = rotation_image_proper(image, -90*i)
            res = self.process(rot_frame_rgb)
            for score in res:
                   rot_accuracy.append(score)
         

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

        return averages


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
        values, indices = similarity[0].topk(len(self.classes))


        # Print the result
        highest_value = -1
        highest_pair = None
        highest_index = -1

        paired_listing = []

        # Combine values and indices
        paired = list(zip(values, indices))

        # Sort pairs by the first element (value)
        sorted_paired = sorted(paired, key=lambda x: x[0], reverse=True)

        for value, index in sorted_paired:
            paired_listing.append([self.classes[index], value.item()])  
        return paired_listing

    

    def clip_decision_tree(self, keyed_frame, with_rotation):
        max_item_type = ''
        averages = ''
        self.classes = ['dress', 'shirt', 'pant']
        if with_rotation == True:
            averages = self.process_on_rotation(keyed_frame, rotation_amount=4)
            max_item_type = max(averages, key=averages.get)
        else:
            averages = self.process_on_rotation(keyed_frame, rotation_amount=1)
            max_item_type = max(averages, key=averages.get)

        res = self.subpath(averages, max_item_type, 'pant',['pant', 'skirt', 'short'], keyed_frame, with_rotation)

        res = self.subpath(res, max_item_type, 'shirt',['shirt', 'sweatshirt', 'sweatshirt', 't-shirt'], keyed_frame, with_rotation)

        return res, averages

    
    def clip_decision_plain(self, keyed_frame, with_rotation):
        self.classes = ['dress', 'skirt', 'sweatshirt', 'shirt', 'short', 'pant', 'jacket', 'poloshirt', 't-shirt']
        if with_rotation == True:
            return self.process_on_rotation(keyed_frame, rotation_amount=4)
        else:
            return self.process_on_rotation(keyed_frame, rotation_amount=1)



    
    def subpath(self, res, max_item_type, parentClass, childs, keyed_frame, with_rotation):
        if max_item_type == parentClass:
            self.classes = childs
            if with_rotation == True:
                return self.process_on_rotation(keyed_frame, rotation_amount=4)
            else:
                return self.process_on_rotation(keyed_frame, rotation_amount=1)

        else:
            return res

