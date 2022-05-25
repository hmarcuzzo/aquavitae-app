from typing import Dict


def remove_none_values(dict: Dict) -> Dict:
    """
    Given a dictionary, dict, remove None values
    If a dictionary includes nested values, a recursive approach is required
    """
    return {
        key: value
        for key, value in dict.items()
        if value is not None
    }
