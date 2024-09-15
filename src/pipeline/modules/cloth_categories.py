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
        return ['dress', 'skirt', 'sweatshirt', 'shirt', 'short', 'pant', 'jacket', 'poloshirt', 't-shirt']

    @staticmethod
    def get_high_level_classes() -> list:
        """
        Retrieves the high-level clothing classes.
        ['dress', 'shirt', 'pant']
        """
        return ['dress', 'shirt', 'pant', 'jacket']


    @staticmethod
    def get_upperwear_tree_long_sleeve() -> list:
        """
        Retrieves the upperwear clothing classes.
        ['shirt', 'sweatshirt','jacket']
        """
        return ['shirt', 'sweatshirt']

    @staticmethod
    def get_upperwear_tree_short_sleeve() -> list:
        """
        Retrieves the upperwear clothing classes.
        ['poloshirt', 't-shirt']
        """
        return ['poloshirt', 't-shirt']


    @staticmethod
    def get_long_or_short_sleeve_decision() -> list:
        """
        Retrieves the upperwear clothing classes.
        ['long-sleeve', 'short-sleeve']
        """
        return ['long-sleeve', 'short-sleeve']

    @staticmethod
    def get_underwear_tree() -> list:
        """
        Retrieves the underwear clothing classes.
        ['long pant', 'short pant', 'skirt']
        """
        return ['jeans', 'trouser', 'sweatpant', 'pant', 'hot pant', 'bermuda short', 'training short', 'skirt']


    @staticmethod
    def decide_on_underwear_tree(item) -> str:
        if item in ['hot pant', 'bermuda short', 'training short']:
            return 'short'
        
        elif item in ['jeans', 'trouser', 'sweatpant']:
            return 'pant'
        else: 
            return item