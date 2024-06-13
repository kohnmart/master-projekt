
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
class ClipClassifierUpdate: 

    def __init__(self):
        clip_model = "ViT-B/16" #@param ["RN50", "RN101", "RN50x4", "RN50x16", "ViT-B/14", "ViT-B/16", "ViT-B/32"]
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(clip_model, device=self.device, jit=False)
        self.classes =  ['dress', 'skirt', 'jacket', 'shirt', 'tshirt', 'pant', 'short']
        self.classes_prompt = [f'a photo of a {cl}' for cl in self.classes]

    def process(self, image):
        
        image = Image.fromarray(image)

        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        text = clip.tokenize(self.classes_prompt).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            text_features = self.model.encode_text(text)

        
        # Pick the top 5 most similar labels for the image
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        values, indices = similarity[0].topk(3)


        # Print the result
        #print("\nTop predictions:\n")
        highest_value = -1
        highest_pair = None

        for value, index in zip(values, indices):
            #print(f"{self.classes[index]:>16s}: {100 * value.item():.2f}%")
            if value.item() > highest_value:
                highest_value = value.item()
                highest_pair = (self.classes[index], 100 * value.item())

        # Return the highest value pair
        return highest_pair

                