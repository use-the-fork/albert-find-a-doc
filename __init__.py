"""
Search multiple Documentation sites
"""
import sys
from albert import Action, Item, QueryHandler, openUrl, info, debug
import os

sys.path.append(os.path.dirname(__file__))

from laravel import Laravel
from mui import Mui
from pest import Pest
from tailwind import Tailwind
from bootstrap import Bootstrap
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
            "lv": Laravel,
            "laravel": Laravel,
            "mui": Mui,
            "pest": Pest,
            "tw": Tailwind,
            "tailwind": Tailwind,
            "bs": Bootstrap,
            "bootstrap": Bootstrap,
            "ijs": Inertiajs,
            "inertiajs": Inertiajs,
            "react": React,
        }

        items = [
            Item(
                id=f'{md_name}/open_{md_name}_NA',
                icon=[ICON_PATH],
                text='Select a library from the list below:',
                subtext=", ".join(search_objects.keys()),
            )
        ]

        try:
            if the_query[1] and the_query[0] in search_objects:
                search_class = search_objects[the_query[0]]
                search = search_class(md_name)
                items = search.handleQuery(search_item=the_query[1])
            elif the_query[0] != "":
                items = [
                    Item(
                        id=f'{md_name}/open_{md_name}_Invalid_query',
                        icon=[ICON_PATH],
                        text='Invalid Query Value',
                        subtext="",
                    )
                ]
        except IndexError:
            pass

        query.add(items)

