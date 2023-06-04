"""
Search multiple Documentation sites
"""
import sys
from albert import Action, Item, QueryHandler, openUrl, info, debug
import os

sys.path.append(os.path.dirname(__file__))

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

        items = [
            Item(
                id=f'{md_name}/open_{md_name}_NA',
                icon=[ICON_PATH],
                text='Select a library from the list below:'
            ),
            Bootstrap.completion,
            Inertiajs.completion,
            Laravel.completion,
            Mui.completion,
            Pest.completion,
            React.completion,
            Tailwind.completion
        ]

        try:
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
            pass

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
                    actions=result.actions,
                )
            )

        return items
