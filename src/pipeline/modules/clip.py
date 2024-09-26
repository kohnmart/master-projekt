import clip
import torch

from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# # from cloth_matrix import all_classes_matrix, high_level_matrix, upperwear_matrix, underwear_matrix
from src.pipeline.modules.cloth_categories import ClothingCategories
from src.pipeline.modules.helper.vision import rotation_image_proper


class ClipFast: 

    """
    model_options: ["RN50", "RN101", "RN50x4", "RN50x16", "ViT-L/14", "ViT-B/16", "ViT-B/32"]
    source: https://github.com/openai/CLIP
    """

    def __init__(self, model_name):
        torch.cuda.empty_cache()
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

        avg_encoding = False
        image_features = []
        text_features = []
        if avg_encoding:
            encoded_images = []
            rotations = [0, 90, 180, 270]
            for rotation in rotations:
                rotated_image = torch.rot90(image_input, k=rotation//90, dims=(2, 3))
                encoded_image = self.model.encode_image(rotated_image)
                encoded_images.append(encoded_image)
        
            image_features = torch.mean(torch.stack(encoded_images), dim=0)
            text_features = self.model.encode_text(text)

        else:
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
        #sorted_paired = sorted(paired, key=lambda x: x[0], reverse=True)


        for value, index in paired:
            paired_listing.append([self.classes[index], value.item()])  

        sorted_paired = []
        for category in self.classes:
            for pair in paired_listing:
                if category == pair[0]:
                    sorted_paired.append(pair)

        return sorted_paired

    

    def clip_decision_tree(self, keyed_frame, with_rotation):
    
        ## HIGH LEVEL CLASSES ##
        main_item_type, main_scores = self.main_path(keyed_frame, with_rotation)

        ## SHIRT CLASSES ## 
        shirt_res = self.sub_branch_shirt(main_item_type, keyed_frame, with_rotation)
        if shirt_res != False: 
            return shirt_res, main_scores

        ## DRESS CLASSES
        dress_res = self.sub_branch_dress(main_item_type, keyed_frame, with_rotation)
        if dress_res != False: 
            return dress_res, main_scores

        ## JACKET CLASSES
        jacket_res = self.sub_branch_jacket(main_item_type, keyed_frame, with_rotation)
        if jacket_res != False: 
            return jacket_res, main_scores

        ## PANT CLASSES 
        return self.sub_branch_pant(main_item_type, keyed_frame, with_rotation), main_scores




    def clip_decision_plain(self, keyed_frame, with_rotation):
        self.classes = ClothingCategories.get_all_classes()
        if with_rotation == True:
            return self.process_on_rotation(keyed_frame, rotation_amount=4)
        else:
            return self.process_on_rotation(keyed_frame, rotation_amount=1)



    def subpath(self, max_item_type, parentClass, childs, keyed_frame, with_rotation):
        if max_item_type == parentClass:
            self.classes = childs
            if with_rotation == True:
                return self.process_on_rotation(keyed_frame, rotation_amount=4)
            else:
                return self.process_on_rotation(keyed_frame, rotation_amount=1)

    

    def main_path(self, keyed_frame, with_rotation):
        self.classes = ClothingCategories.get_high_level_classes()
        if with_rotation == True:
            main_path_score = self.process_on_rotation(keyed_frame, rotation_amount=4)
            main_item_type = max(main_path_score, key=main_path_score.get)
        else:
            main_path_score = self.process_on_rotation(keyed_frame, rotation_amount=1)
            main_item_type = max(main_path_score, key=main_path_score.get)

        return main_item_type, main_path_score

    
    def sub_branch_shirt(self, max_item_type, keyed_frame, with_rotation):
        if max_item_type == 'shirt':
            classes = ClothingCategories.get_shirt_classes()
            res = self.subpath(max_item_type, 'shirt', classes, keyed_frame, with_rotation)
            max_item_type = max(res, key=res.get)

            ## CHECK ON POLOSHIRTS 
            if max_item_type == 'poloshirt':
                classes = ['longsleeve', 'shortsleeve']
                sub_res_poloshirt = self.subpath(max_item_type, 'poloshirt', classes, keyed_frame, with_rotation)
                # Fix: Use correct parameters and pass sub_res_poloshirt only as a dict
                res = ClothingCategories.swap_out_temp_categories(res, sub_res_poloshirt, current_type='longsleeve', type_to_insert='sweatshirt', type_to_pop='poloshirt')

            return res

        else:
            return False



    def sub_branch_dress(self, max_item_type, keyed_frame, with_rotation):
        if max_item_type == 'dress':
            skirts = ClothingCategories.get_semantics('skirt')
            dresses = ClothingCategories.get_semantics('dress')
            combined = skirts + dresses 
            res = self.subpath(max_item_type, 'dress', combined, keyed_frame, with_rotation)  

            max_type = max(res, key=res.get)

            if max_type in skirts:
                res['skirt'] = res.pop(max_type, 0)

            else:
                res['dress'] = res.pop(max_type, 0)

            return res

        else:
            return False


    def sub_branch_jacket(self, max_item_type, keyed_frame, with_rotation):
        if max_item_type == 'jacket':
            classes = ['sweatshirt', 'jacket']
            res = self.subpath(max_item_type, 'jacket', classes , keyed_frame, with_rotation)
            return res

        else: 
            return False

    
    def sub_branch_pant(self, max_item_type, keyed_frame, with_rotation):
        if max_item_type == 'pant':
            res = self.subpath(max_item_type, 'pant', ClothingCategories.get_underwear_tree(), keyed_frame, with_rotation)
            max_type = max(res, key=res.get)

            ## CHECK ON SHORTS
            if max_type in ['hot pant', 'training short']:
                if max_type == 'hot pant':
                    res = ClothingCategories.swap_out_temp_categories(res, res, current_type='hot pant', type_to_insert='short', type_to_pop='hot pant')
                else:
                    res = ClothingCategories.swap_out_temp_categories(res, res, current_type='training short', type_to_insert='short', type_to_pop='training short')
                max_type = 'short'

                sub_res_short = self.subpath(max_type, 'short', ['short', 'skirt'], keyed_frame, with_rotation)
                res = ClothingCategories.swap_out_temp_categories(res, sub_res_short, current_type='skirt', type_to_insert='skirt', type_to_pop='short')

            return res

        else: 
            return False