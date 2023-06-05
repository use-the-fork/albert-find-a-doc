from algoliasearch.search_client import SearchClient
import os
import sys

sys.path.append(os.path.dirname(__file__))

from dto import ItemDTO, AlgoliaSearchDTO, ActionDTO
from base_document import BaseDocument

algolia_search_dto = AlgoliaSearchDTO(app_id='KNPXZI5B0M', api_key='5fc87cef58bb80203d2207578309fab6',
                                      search_index='tailwindcss', request_options={"facetFilters": "version:v3"})


class Tailwind(BaseDocument):
    client = SearchClient.create(algolia_search_dto.app_id, algolia_search_dto.api_key)
    index = client.init_index(algolia_search_dto.search_index)
    md_name = "Tailwind"
    md_icon = "{}/images/{}".format(os.path.dirname(__file__), 'tailwind.png')
    md_docs = 'https://tailwindcss.com/docs/'
    md_search = 'tailwindcss'
    md_completion = 'fad tailwind '

    completion = ItemDTO(
        id='fad/{}_completion'.format(md_name),
        icon=md_icon,
        text=md_name,
        completion=md_completion
    )

    def __init__(self, md_name):
        super().__init__(md_name)

    def get_title(self, hierarchy):
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

    def get_subtitle(self, hierarchy):
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

    def handle_query(self, search_item):
        items = []

        if search_item:
            search = self.index.search(
                search_item, self.algolia_search_query(algolia_search_dto.request_options)
            )

            for hit in search["hits"]:

                title = self.get_title(hit['hierarchy'])
                subtitle = self.get_subtitle(hit['hierarchy'])
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
                    ItemDTO(
                        id=f'{self.md_name}/{hit["objectID"]}',
                        icon=self.md_icon,
                        text=title,
                        subtext=subtitle if subtitle is not None else "",
                        action=
                        ActionDTO(
                            text="Open",
                            subtext='Open the {} Documentation'.format(self.md_name),
                            url_to_open=url
                        )
                    )
                )

            if len(items) == 0:
                items = self.no_results(search_item)

        return items
