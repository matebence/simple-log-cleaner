import pandas
import pathlib

from classes.builder.Expand.Expand import Expand
from classes.builder.Expand.options.Route import Route
from classes.utilities.Columns import Columns
from classes.utilities.Path import Path


class ExpandLog(Expand):

    __append_routes = None

    def __init__(self):
        self.__input_file_name = None
        self.__web_map_file_name = None
        self.__output_file_name = None

    def from_file(self, input_file_name):
        self.__input_file_name = input_file_name
        return self

    def by_file(self, web_map_file_name):
        self.__web_map_file_name = web_map_file_name
        return self

    def to_file(self, output_file_name):
        self.__output_file_name = output_file_name
        return self

    def generate_routes(self):
        self.__append_routes = Route()
        return self

    def append_routes_and_build(self):
        pass
