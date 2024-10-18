class ClothingCategories:
    """
    A class for managing and retrieving clothing classifications and their hierarchical structure.
    --> only semantic class.
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
        ['dress', 'shirt', 'pant']
        """
        return ['dress', 'skirt', 'shirt', 'pant', 'jacket']
    
    @staticmethod 
    def get_high_level_questioning() -> list:
        return ['dress or skirt', 'jacket or shirt', 'pant or short']

    @staticmethod
    def get_shirt_classes() -> list:
        return ["T-Shirt", "Polo Shirt", "Henley Shirt",  "Baseball Shirt",
                "Button-Down Shirt",
                "Chambray Shirt",
                "Oxford Shirt",
                "Camp Shirt",
                "Tank Top",
                "Hoodie",
                "Crewneck Sweatshirt",
                "Zip-Up Sweatshirt",
                "Pullover Sweatshirt"
                ]

    @staticmethod
    def reverse_shirt_classes(item: str) -> str:

        if item in ["Dress Shirt", "Henley Shirt", "Flannel Shirt", "Button-Down Shirt", "Chambray Shirt", "Oxford Shirt", "Camp Shirt"]:
            return "shirt"
        elif item in ["Hoodie", "Baseball Shirt",
                      "Crewneck Sweatshirt",
                      "Zip-Up Sweatshirt",
                      "Pullover Sweatshirt"]:
            return "sweatshirt"
        
        elif item == "Polo Shirt":
            return "poloshirt"
        
        elif item == "T-Shirt" or item == "Tank Top": 
            return "t-shirt"


    @staticmethod
    def decide_on_upperwear_tree(item) -> str:
        if item in [
                "baseballshirt"]:
            return "sweatshirt"

        elif item in ["Dress Shirt", "Henley Shirt", "Flannel Shirt",
                      "Button-Down Shirt",
                      "Chambray Shirt",
                      "Oxford Shirt",
                      "Camp Shirt"]:
            return "shirt"

        else:
            return item

    @staticmethod
    def get_upperwear_tree_long_sleeve() -> list:
        """
        Retrieves the upperwear clothing classes.
        ['shirt', 'sweatshirt']
        """
        return ['shirt', 'sweatshirt']

    @staticmethod
    def get_upperwear_tree_short_sleeve() -> list:
        """
        Retrieves the upperwear clothing classes.
        ['poloshirt', 't-shirt']
        """
        return ['poloshirt', 't-shirt']

    def get_upperwear_tree() -> list:
        return ['t-shirt', 'shirt', 'sweatshirt']

    @staticmethod
    def get_long_or_short_sleeve_decision() -> list:
        """
        Retrieves the upperwear clothing classes.
        ['long-sleeve', 'short-sleeve']
        """
        return ['shirt', 't-shirt']

    @staticmethod
    def get_underwear_tree() -> list:
        """
        Retrieves the underwear clothing classes.
        ['long pant', 'short pant', 'skirt']
        """
        return ['jeans', 'trouser', 'sweatpant', 'pant', 'hot pant', 'training short', 'training pant', 'skirt']

    @staticmethod
    def decide_on_underwear_tree(item) -> str:
        if item in ['hot pant', 'training short']:
            return 'short'

        elif item in ['jeans', 'trouser', 'sweatpant', 'training pant']:
            return 'pant'
        else:
            return item

    @staticmethod
    def swap_out_temp_categories(cloth_obj_main: dict, cloth_obj_sub: dict, current_type: dict, type_to_insert: str, type_to_pop: str) -> dict:
        max_type = max(cloth_obj_sub, key=cloth_obj_sub.get)

        if max_type in current_type:
            # Transfer the value from type_to_pop to type_to_insert
            cloth_obj_main[type_to_insert] = cloth_obj_main.pop(type_to_pop, 0)

        return cloth_obj_main

    @staticmethod
    def get_semantic_skirt_classes():
        return

    def get_semantics(cloth_type: str):
        if cloth_type == 'skirt':
            return ["Pencil Skirt", "A-Line Skirt", "Pleated Skirt", "Maxi Skirt", "Wrap Skirt"]

        elif cloth_type == 'dress':
            return ["A-Line Dress", "Sheath Dress", "Wrap Dress", "Maxi Dress", "Shift Dress"]
