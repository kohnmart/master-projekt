
from transformers import CLIPProcessor, CLIPModel

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