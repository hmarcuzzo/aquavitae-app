class DictionaryUtils:
    @staticmethod
    def remove_none_values(_dict: dict) -> dict:
        """
        Given a dictionary, dict, remove None values
        If a dictionary includes nested values, a recursive approach is required
        """
        return {
            key: value
            for key, value in _dict.items()
            if value is not None
        }
