"""
Search the Laravel Documentation
"""

from albert import Action, Item, QueryHandler, openUrl, info, debug
import os
from algoliasearch.search_client import SearchClient

md_iid = "0.5"
md_version = "0.4"
md_id = __name__
md_name = "Laravel"
md_docs = "https://laravel.com/docs/"
md_trigger = "lv"
md_description = "Albert extension for quickly and easily searching the Laravel documentation"
md_url = "https://github.com/use-the-fork/albert-laravel-docs/issues"
md_maintainers = "@use-the-fork"

client = SearchClient.create("E3MIRNPJH5", "1fa3a8fec06eb1858d6ca137211225c0")
index = client.init_index("laravel")

GOOGLE_ICON_PATH = "{}/images/google.png".format(os.path.dirname(__file__))
ICON_PATH = "{}/images/icon.png".format(os.path.dirname(__file__))


class Plugin(QueryHandler):
    def id(self):
        return md_id

    def name(self):
        return md_name

    def description(self):
        return md_description

    def defaultTrigger(self):
        return '{} '.format(md_trigger),

    def handleQuery(self, query):
            query.add(
                Item(
                    id=f'{md_name}/open_{md_name}_docs',
                    icon=[ICON_PATH],
                    text='Open {} Docs'.format(md_name),
                    subtext="No match found. Open {}".format(md_docs),
                    actions=[
                        Action(
                            "Open",
                            'Open the {} Documentation'.format(md_name.replace("https://", "")),
                            lambda u=md_docs: openUrl(u)
                        )

                    ],
                )
            )

