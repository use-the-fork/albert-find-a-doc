import urllib.parse
from algoliasearch.search_client import SearchClient
import os
from albert import Action, Item, QueryHandler, openUrl, info, debug
import sys

sys.path.append(os.path.dirname(__file__))


class Bootstrap:
    client = SearchClient.create("BH4D9OD16A", "5990ad008512000bba2cf951ccf0332f")
    index = client.init_index("bootstrap")
    icon = "{}/images/bootstrap.png".format(os.path.dirname(__file__))
    docs = "https://getbootstrap.com/docs/5.0/"

    def __init__(self, md_name):
        self.md_name = md_name

    def getTitle(self, hierarchy):
        if hierarchy["lvl6"] is not None:
            return hierarchy["lvl6"]

        if hierarchy["lvl5"] is not None:
            return hierarchy["lvl5"]

        if hierarchy["lvl4"] is not None:
            return hierarchy["lvl4"]

        if hierarchy["lvl3"] is not None:
            return hierarchy["lvl3"]

        if hierarchy["lvl2"] is not None:
            return hierarchy["lvl2"]

        if hierarchy["lvl1"] is not None:
            return hierarchy["lvl1"]

        if hierarchy["lvl0"] is not None:
            return hierarchy["lvl0"]

        return None

    def getSubtitle(self, hierarchy):
        if hierarchy["lvl6"] is not None:
            return hierarchy["lvl5"]

        if hierarchy["lvl5"] is not None:
            return hierarchy["lvl4"]

        if hierarchy["lvl4"] is not None:
            return hierarchy["lvl3"]

        if hierarchy["lvl3"] is not None:
            return hierarchy["lvl2"]

        if hierarchy["lvl2"] is not None:
            return hierarchy["lvl1"]

        if hierarchy["lvl1"] is not None:
            return hierarchy["lvl0"]

        return None

    def handleQuery(self, search_item):
        items = []

        if search_item:

            search = self.index.search(
                search_item,
                {"facetFilters": "version:5.0", "hitsPerPage": 5, "highlightPreTag": "...", "highlightPostTag": "..."}
            )

            for hit in search["hits"]:

                title = self.getTitle(hit['hierarchy'])
                subtitle = self.getSubtitle(hit['hierarchy'])
                url = hit["url"]

                text = False
                try:
                    text = hit["_highlightResult"]["content"]["value"]
                except KeyError:
                    pass

                if text and subtitle:
                    title = "{} - {}".format(title, subtitle)
                    subtitle = text

                items.append(
                    Item(
                        id=f'{self.md_name}/{hit["objectID"]}',
                        icon=[self.icon],
                        text=title,
                        subtext=subtitle if subtitle is not None else "",
                        actions=[
                            Action(
                                "Open",
                                'Open the {} Documentation'.format(self.md_name),
                                lambda u=url: openUrl(u)
                            )
                        ],
                    )
                )

            if len(items) == 0:
                term = "bootstrap 5 {}".format(search_item)

                google = "https://www.google.com/search?q={}".format(
                    urllib.parse.quote(term)
                )

                items.append(
                    Item(
                        id=f'{self.md_name}/search_google',
                        icon=["{}/images/google.png".format(os.path.dirname(__file__))],
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
                    Item(
                        id=f'{self.md_name}/open_{self.md_name}_docs',
                        icon=[self.icon],
                        text='Open {} Docs'.format(self.md_name),
                        subtext="No match found. Open {}".format(self.docs),
                        actions=[
                            Action(
                                "Open",
                                'Open the {} Documentation'.format(self.md_name.replace("https://", "")),
                                lambda u=self.docs: openUrl(u)
                            )
                        ],
                    )
                )

        return items
