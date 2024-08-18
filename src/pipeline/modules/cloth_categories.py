class ClothingCategories:
    """
    A class for managing and retrieving clothing classifications and their hierarchical structure.
    --> only semantic class.
    """

    @staticmethod
    def get_high_level_classes() -> list:
        """
        Retrieves the high-level clothing classes.
        ['dress', 'shirt', 'pant']
        """
        return ['dress', 'shirt', 'pant']

    @staticmethod
    def get_all_classes() -> list:
        """
        Retrieves all possible clothing classes.
        ['dress', 'skirt', 'sweatshirt', 'shirt', 'short', 'pant', 'jacket', 'poloshirt', 't-shirt']
        """
        return ['dress', 'skirt', 'sweatshirt', 'shirt', 'short', 'pant', 'jacket', 'poloshirt', 't-shirt']

    @staticmethod
    def get_upperwear_tree() -> list:
        """
        Retrieves the upperwear clothing classes.
        ['shirt', 'sweatshirt', 'poloshirt', 't-shirt']
        """
        return ['shirt', 'sweatshirt', 'poloshirt', 't-shirt']

    @staticmethod
    def get_underwear_tree() -> list:
        """
        Retrieves the underwear clothing classes.
        ['long pant', 'short pant', 'skirt']
        """
        return ['long pant', 'short pant', 'skirt']
