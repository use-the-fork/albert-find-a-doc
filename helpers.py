import os
import sys

sys.path.append(os.path.dirname(__file__))


class Helpers:
    @staticmethod
    def is_in_array(string_to_check: str, md_possible_completions):

        partial_match = False
        for element in md_possible_completions:
            if string_to_check in element:
                partial_match = True
                break

        return partial_match
