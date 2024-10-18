class ClothingCategories:
    """
    A class for managing and retrieving clothing classifications and their hierarchical structure.
    """

    @staticmethod
    def get_all_classes() -> list:
        """
        Retrieves all possible clothing classes.
        ['dress', 'skirt', 'sweatshirt', 'shirt', 'short', 'pant', 'jacket', 'poloshirt', 't-shirt']
        """
        return ['dress', 'skirt', 'short', 'pant', 'jacket', 'sweatshirt', 'shirt', 'poloshirt', 't-shirt']

    @staticmethod
    def get_high_level_classes() -> list:
        """
        Retrieves the high-level clothing classes.
        ['dress', 'skirt', 'shirt', 'pant', 'jacket']
        """
        return ['dress', 'skirt', 'shirt', 'pant', 'jacket']
    
    @staticmethod 
    def get_high_level_questioning() -> list:
        """
        Retrieves possible high-level decision questions for clothing classification.
        """
        return ['dress or skirt', 'tshirt or shirt or jacket', 'pant or short']

    @staticmethod
    def get_shirt_classes() -> list:
        """
        Retrieves detailed shirt-related classifications.
        """
        return [
            "T-Shirt", "Polo Shirt", "Baseball Shirt", "Button-Down Shirt",
            "Chambray Shirt", "Oxford Shirt", "Camp Shirt", "Tank Top",
            "Hoodie", "Crewneck Sweatshirt", "Zip-Up Sweatshirt", "Pullover Sweatshirt"
        ]

    @staticmethod
    def reverse_shirt_classes(item: str) -> str:
        """
        Maps a detailed shirt classification to a general class.
        """
        shirt_mappings = {
            "Dress Shirt": "shirt", "Henley Shirt": "shirt", "Flannel Shirt": "shirt",
            "Button-Down Shirt": "shirt", "Chambray Shirt": "shirt", "Oxford Shirt": "shirt",
            "Camp Shirt": "shirt", "Hoodie": "sweatshirt", "Baseball Shirt": "sweatshirt",
            "Crewneck Sweatshirt": "sweatshirt", "Zip-Up Sweatshirt": "sweatshirt",
            "Pullover Sweatshirt": "sweatshirt", "Polo Shirt": "poloshirt",
            "T-Shirt": "t-shirt", "Tank Top": "t-shirt"
        }
        return shirt_mappings.get(item, item)

    @staticmethod
    def decide_on_upperwear(item: str) -> str:
        """
        Decides on a general upperwear classification based on the detailed item provided.
        """
        if item in ["Baseball Shirt"]:
            return "sweatshirt"
        elif item in [
            "Dress Shirt", "Henley Shirt", "Flannel Shirt", "Button-Down Shirt",
            "Chambray Shirt", "Oxford Shirt", "Camp Shirt"
        ]:
            return "shirt"
        return item

    @staticmethod
    def get_upperwear_long_sleeve() -> list:
        """
        Retrieves upperwear classes with long sleeves.
        ['shirt', 'sweatshirt']
        """
        return ['shirt', 'sweatshirt']

    @staticmethod
    def get_upperwear_short_sleeve() -> list:
        """
        Retrieves upperwear classes with short sleeves.
        ['poloshirt', 't-shirt']
        """
        return ['poloshirt', 't-shirt']

    @staticmethod
    def get_upperwear_tree() -> list:
        """
        Retrieves general upperwear classes.
        ['t-shirt', 'shirt', 'sweatshirt']
        """
        return ['t-shirt', 'shirt', 'sweatshirt']

    @staticmethod
    def get_sleeve_length_options() -> list:
        """
        Retrieves sleeve length options for upperwear.
        ['shirt', 't-shirt']
        """
        return ['shirt', 't-shirt']

    @staticmethod
    def get_lowerwear_classes() -> list:
        """
        Retrieves lowerwear classes, including pants and skirts.
        ['jeans', 'trouser', 'sweatpant', 'pant', 'hot pant', 'training short', 'training pant', 'skirt']
        """
        return ['jeans', 'trouser', 'sweatpant', 'pant', 'hot pant', 'training short', 'training pant', 'skirt']

    @staticmethod
    def decide_on_lowerwear(item: str) -> str:
        """
        Decides on a general lowerwear classification based on the item provided.
        """
        if item in ['hot pant', 'training short']:
            return 'short'
        elif item in ['jeans', 'trouser', 'sweatpant', 'training pant']:
            return 'pant'
        return item

    @staticmethod
    def swap_temp_categories(
        main_obj: dict, sub_obj: dict, current_type: list, type_to_insert: str, type_to_pop: str
    ) -> dict:
        """
        Swaps out temporary categories in the main object based on the highest scoring sub-object category.
        """
        max_type = max(sub_obj, key=sub_obj.get)
        if max_type in current_type:
            main_obj[type_to_insert] = main_obj.pop(type_to_pop, 0)
        return main_obj

    @staticmethod
    def get_semantic_skirt_classes() -> list:
        """
        Retrieves semantic skirt classes.
        """
        return ["Pencil Skirt", "A-Line Skirt", "Pleated Skirt", "Maxi Skirt", "Wrap Skirt"]

    @staticmethod
    def get_semantic_dress_classes() -> list:
        """
        Retrieves semantic dress classes.
        """
        return ["A-Line Dress", "Sheath Dress", "Wrap Dress", "Maxi Dress", "Shift Dress"]

    @staticmethod
    def get_semantics(cloth_type: str) -> list:
        """
        Retrieves semantic classes for a given clothing type (e.g., 'skirt' or 'dress').
        """
        if cloth_type == 'skirt':
            return ClothingCategories.get_semantic_skirt_classes()
        elif cloth_type == 'dress':
            return ClothingCategories.get_semantic_dress_classes()
        return []
