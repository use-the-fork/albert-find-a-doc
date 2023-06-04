import os
import sys
from albert import Action

sys.path.append(os.path.dirname(__file__))


class ItemDTO:
    def __init__(self, id, icon: str = '', text: str = '', subtext: str = '', actions: list[Action] = []):
        if not id:
            raise ValueError("Id cannot be empty")

        self.id = id
        self.icon = icon
        self.text = text
        self.subtext = subtext
        self.actions = actions


class AlgoliaSearchDTO:
    def __init__(self, app_id=None, api_key=None, search_index=None, request_options=None):
        if not id:
            raise ValueError("Id cannot be empty")

        self.app_id = app_id
        self.api_key = api_key
        self.search_index = search_index
        self.request_options = request_options
