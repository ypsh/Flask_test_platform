# -*- coding: UTF-8 -*-
import sys


# noinspection PyMethodMayBeStatic
class Path:
    def __init__(self):
        self.path = self.get_global_path('Flask_test_platform')

    def get_global_path(self, dir_name):
        """

        :type dir_name: object
        """
        global_path = sys.path[0]
        for item in sys.path:
            if item.endswith(dir_name):
                global_path = item
        return global_path

    def get_current_path(self):
        return self.path


if __name__ == '__main__':
    print(Path().get_global_path(""))
