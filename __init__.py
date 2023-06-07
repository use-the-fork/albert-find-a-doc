"""
Search multiple Documentation sites
"""
import sys
from albert import Action, Item, QueryHandler, openUrl, info, debug
import os

sys.path.append(os.path.dirname(__file__))

from dto import ItemDTO
from helpers import Helpers

from bootstrap import Bootstrap
from laravel import Laravel
from mui import Mui
from pest import Pest
from tailwind import Tailwind
from inertiajs import Inertiajs
from react import React

md_iid = "0.5"
md_version = "0.4"
md_id = __name__
md_name = "Find a Doc"
md_description = "Albert extension for quickly and easily searching documentation sites"
md_url = "https://github.com/use-the-fork/albert-find-a-doc/issues"
md_maintainers = "@use-the-fork"
md_lib_dependencies = ["algoliasearch"]
md_trigger = "fad "

ICON_PATH = "{}/images/fad-icon.png".format(os.path.dirname(__file__))


class Plugin(QueryHandler):
    def id(self):
        return md_id

    def name(self):
        return md_name

    def description(self):
        return md_description

    def defaultTrigger(self):
        return md_trigger

    def handleQuery(self, query):
        if not query.isValid:
            return

        the_query = query.string.strip().split(" ", 1)

        search_objects = {
            "laravel": Laravel,
            "mui": Mui,
            "pest": Pest,
            "tailwind": Tailwind,
            "bootstrap": Bootstrap,
            "inertiajs": Inertiajs,
            "react": React,
        }

        items = []

        try:
            if Helpers.is_in_array(the_query[0], Laravel.md_possible_completions):
                items.append(self.convert_completion(Laravel.completion))

            if Helpers.is_in_array(the_query[0], Bootstrap.md_possible_completions):
                items.append(self.convert_completion(Bootstrap.completion))

            if Helpers.is_in_array(the_query[0], Inertiajs.md_possible_completions):
                items.append(self.convert_completion(Inertiajs.completion))

            if Helpers.is_in_array(the_query[0], Mui.md_possible_completions):
                items.append(self.convert_completion(Mui.completion))

            if Helpers.is_in_array(the_query[0], Pest.md_possible_completions):
                items.append(self.convert_completion(Pest.completion))

            if Helpers.is_in_array(the_query[0], React.md_possible_completions):
                items.append(self.convert_completion(React.completion))

            if Helpers.is_in_array(the_query[0], Tailwind.md_possible_completions):
                items.append(self.convert_completion(Tailwind.completion))

                if the_query[1] and the_query[0] in search_objects:
                    search_instance = search_objects[the_query[0]](md_name)
                    items = self.getResults(search_instance=search_instance, the_query=the_query[1])
                elif the_query[0] != "":
                    items = [
                        Item(
                            id=f'{md_name}/open_invalid_query',
                            icon=[ICON_PATH],
                            text='Invalid Query Value',
                            subtext="",
                        )
                    ]
        except IndexError:
            items = [
                Item(
                    id=f'{md_name}/open_invalid_query',
                    icon=[ICON_PATH],
                    text='The following libraries are valid:',
                    subtext=", ".join(search_objects.keys()),
                )
            ]

        query.add(items)

    def getResults(self, search_instance, the_query):
        items = []
        results = search_instance.handle_query(search_item=the_query)
        for result in results:
            items.append(
                Item(
                    id=result.id,
                    icon=[result.icon],
                    text=result.text,
                    subtext=result.subtext if result.subtext is not None else "",
                    actions=[
                        Action(
                            result.action.text,
                            result.action.subtext,
                            lambda u=result.action.url_to_open: openUrl(u)
                        )
                    ]
                )
            )

        return items

    def convert_completion(self, the_item: ItemDTO = None):
        return Item(
                    id="{}/completion".format(the_item.id),
                    icon=[the_item.icon],
                    text=the_item.text,
                    subtext=the_item.subtext if the_item.subtext is not None else "",
                    completion=the_item.completion
                )
