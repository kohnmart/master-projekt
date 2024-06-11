import pymongo
import os
import uuid
from dotenv import load_dotenv

class MONGO:

    def __init__(self):
        load_dotenv()
        print(os.environ.get('MONGO_KEY'))
        mongo_key = 'mongodb+srv://mkohnle:Gni1Km1F0nWFXoNw@cluster0.t1akszl.mongodb.net/?retryWrites=true&w=majority'
        self.client = pymongo.MongoClient(mongo_key)
        self.db = self.client.detex_ai
        self.collection = self.db.boundingboxes
        self.collection.delete_many({})

    def mongo_insert(self, sample, label, mask):

        #check if sample already exists and if delete/update
        existing_docs = self.collection.find_one({'sample_id': sample[0]})

        if existing_docs:
            # delete docs
            result = self.collection.delete_many({'sample_id': sample})
            print(f"{result.deleted_count} documents deleted with ID: {sample}")

        result = self.collection.insert_one({
        '_id': str(uuid.uuid4()),
        'sample_id': sample,
        'type': 'rect',
        'left': mask['bbox'][0],
        'top': mask['bbox'][1],
        'width': mask['bbox'][2],
        'height': mask['bbox'][3],
        'label': label,
        'iou_score': mask['predicted_iou'],
    })
        if not result.acknowledged:
            print("Insertion failed")


