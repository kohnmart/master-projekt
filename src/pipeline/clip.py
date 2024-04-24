
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
   

    def classifier(self):
        
        probs = self.predictor(['a photo a upper body cloth', 'a photo of a lower body cloth'])

        if probs[0][0] < probs[0][1]:
            probs = self.predictor(['a photo of a short pants', 'a photo of a long pants'])
            res = f"Short: {probs[0][0]:.2f}% ___ Pant: {probs[0][1]:.2f}%"

        else: 
            probs = self.predictor(['a photo of a short sleeve top', 'a photo of a long-sleeve top'])
            res = f"Short Sleeve: {probs[0][0]:.2f}% ___ Long Sleeve: {probs[0][1]:.2f}%"

            if probs[0][0] > probs[0][1]:
                probs = self.predictor(['a photo of a t-shirt', 'a photo of a polo shirt'])
                res = f"T-Shirt: {probs[0][0]:.2f}% ___ Polo Shirt: {probs[0][1]:.2f}%"

            else:
                probs = self.predictor(['a photo of a sweatshirt', 'a photo of a jacket'])
                res = f"Shirt: {probs[0][0]:.2f}% ___ Jacket: {probs[0][1]:.2f}%"


        return res