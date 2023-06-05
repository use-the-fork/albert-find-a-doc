# encoding=utf8

import sys
import webbrowser
from wox import Wox, WoxAPI
import os

sys.path.append(os.path.dirname(__file__))

from dto import ItemDTO
from bootstrap import Bootstrap
from laravel import Laravel
from mui import Mui
from pest import Pest
from tailwind import Tailwind
from inertiajs import Inertiajs
from react import React

ICON_PATH = "{}/images/fad-icon.png".format(os.path.dirname(__file__))

md_iid = "0.5"
md_version = "0.4"
md_id = __name__
md_name = "Find a Doc"
md_description = "Albert extension for quickly and easily searching documentation sites"
md_url = "https://github.com/use-the-fork/albert-find-a-doc/issues"
md_maintainers = "@use-the-fork"
md_lib_dependencies = ["algoliasearch"]
md_trigger = "fad "


class FindADoc(Wox):

    def query(self, key):

        the_query = key.strip().split(" ", 1)

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
            {
                "Title": "Select a library from the list below:",
                "IcoPath": ICON_PATH,

            },
            self.convert_completion(Bootstrap.completion),
            self.convert_completion(Inertiajs.completion),
            self.convert_completion(Laravel.completion),
            self.convert_completion(Mui.completion),
            self.convert_completion(Pest.completion),
            self.convert_completion(React.completion),
            self.convert_completion(Tailwind.completion)
        ]

        try:
            if the_query[1] and the_query[0] in search_objects:
                search_instance = search_objects[the_query[0]](md_name)
                items = self.getResults(search_instance=search_instance, the_query=the_query[1])
            elif the_query[0] != "":
                items = [
                    {
                        "Title": "Invalid Query Value",
                        "IcoPath": ICON_PATH,
                    }
                ]
        except IndexError:
            pass

        return items

    def getResults(self, search_instance, the_query):
        items = []
        results = search_instance.handle_query(search_item=the_query)
        for result in results:
            items.append(
                {
                    "Title": result.text,
                    "SubTitle": result.subtext if result.subtext is not None else "",
                    "IcoPath": result.icon,
                    "JsonRPCAction":
                        {
                            "method": "openUrl",
                            "parameters": [result.action.url_to_open],
                            "dontHideAfterAction": False
                        }
                }
            )

        return items

    def convert_completion(self, the_item: ItemDTO = None):
        return {
            "Title": the_item.text,
            "SubTitle": the_item.subtext if the_item.subtext is not None else "",
            "IcoPath": the_item.icon,
            "JsonRPCAction":
                {
                    "method": "change_completion",
                    "parameters": [the_item.completion],
                    "dontHideAfterAction": True
                }
        }

    def change_completion(self, completion):
        WoxAPI.change_query(completion)

    def openUrl(self, url):
        webbrowser.open(url)
        # todo:doesn't work when move this line up
        WoxAPI.change_query(url)


if __name__ == "__main__":
    FindADoc()
