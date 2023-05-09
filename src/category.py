import json
import os


def check_category(category: str):
    """
    Check if the category already exists, otherwise create it
    Args:
        category: The category to check
    Returns:
    """
    if not os.path.exists("../categories/{}.json".format(category.lower())):
        # Create a file with the category name
        with open("../categories/{}.json".format(category.lower()), "w") as f:
            json.dump([], f, indent=4)

def add_category_entry:


def get_category():