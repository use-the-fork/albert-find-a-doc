
from algoliasearch.search_client import SearchClient
import os
import sys

sys.path.append(os.path.dirname(__file__))

from dto import ItemDTO, AlgoliaSearchDTO, ActionDTO
from base_document import BaseDocument
from typing import List

algolia_search_dto = AlgoliaSearchDTO(app_id='1JFXODBVDH', api_key='dd63fbb022012f3144613ee088b8645b',
                                      search_index='pestphp', request_options={})


class Pest(BaseDocument):
    client = SearchClient.create(algolia_search_dto.app_id, algolia_search_dto.api_key)
    index = client.init_index(algolia_search_dto.search_index)
    md_name = "PEST"
    md_icon = "{}/images/{}".format(os.path.dirname(__file__), 'pest.png')
    md_docs = 'https://pestphp.com/docs/'
    md_search = 'pest php'
    md_completion = 'fad pest '

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

    def handle_query(self, search_item) -> List[ItemDTO]:
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
