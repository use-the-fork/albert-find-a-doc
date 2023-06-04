import urllib.parse
from algoliasearch.search_client import SearchClient
import os
from albert import Action, openUrl
import sys

sys.path.append(os.path.dirname(__file__))

from dto import ItemDTO


class BaseDocument:
    md_icon = "{}/images/{}".format(os.path.dirname(__file__), 'fad-icon.png')
    md_docs = ""
    md_search = ""

    def __init__(self, md_name: str):
        self.md_name = md_name

    def algolia_search_query(self, options=None):
        if options is None:
            options = {}
        return {**{"hitsPerPage": 5, "highlightPreTag": "...",
                   "highlightPostTag": "..."}, **options}

    def no_results(self, search_item):
        items = []
        term = "{} {}".format(self.md_search, search_item)
        google = "https://www.google.com/search?q={}".format(
            urllib.parse.quote(term)
        )

        items.append(
            ItemDTO(
                id=f'{self.md_name}/search_google',
                icon="{}/images/google.png".format(os.path.dirname(__file__)),
                text="Search Google",
                subtext='No match found. Search Google for: "{}"'.format(term),
                actions=[
                    Action(
                        "Open",
                        'No match found. Search Google',
                        lambda u=google: openUrl(u)
                    )
                ],
            )
        )

        items.append(
            ItemDTO(
                id=f'{self.md_name}/open_{self.md_name}_docs',
                icon=self.md_icon,
                text='Open {} Docs'.format(self.md_name),
                subtext="No match found. Open {}".format(self.md_docs),
                actions=[
                    Action(
                        "Open",
                        'Open the {} Documentation'.format(self.md_name.replace("https://", "")),
                        lambda u=self.md_docs: openUrl(u)
                    )
                ],
            )
        )
