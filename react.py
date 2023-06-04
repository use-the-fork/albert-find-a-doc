from algoliasearch.search_client import SearchClient
import os
from albert import Action, Item, openUrl
import sys

sys.path.append(os.path.dirname(__file__))

from dto import ItemDTO, AlgoliaSearchDTO
from base_document import BaseDocument

algolia_search_dto = AlgoliaSearchDTO(app_id='1FCF9AYYAT', api_key='e8451218980a351815563de007648b00',
                                      search_index='beta-react', request_options={})


class React(BaseDocument):
    client = SearchClient.create(algolia_search_dto.app_id, algolia_search_dto.api_key)
    index = client.init_index(algolia_search_dto.search_index)
    md_name = "React"
    md_icon = "{}/images/{}".format(os.path.dirname(__file__), 'react.png')
    md_docs = 'https://react.dev/reference/react/'
    md_search = 'react'
    md_completion = 'fad react '

    completion = Item(
                id='fad/{}_completion'.format(md_name),
                icon=[md_icon],
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
                items = self.no_results(search_item)

        return items
