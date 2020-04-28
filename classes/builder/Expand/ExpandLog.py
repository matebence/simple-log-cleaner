import pandas

from classes.builder.Expand.Expand import Expand
from classes.builder.Expand.options.Domain import Domain
from classes.builder.Expand.options.Route import Route
from classes.utilities.Path import Path


class ExpandLog(Expand):
    __append_routes_by_domain = None
    __append_routes_by_referer = None

    def __init__(self):
        self.__input_file_name = None
        self.__domain = None
        self.__output_file_name = None

    def from_file(self, input_file_name):
        self.__input_file_name = input_file_name
        return self

    def by_domain(self, domain):
        self.__domain = domain
        return self

    def to_file(self, output_file_name):
        self.__output_file_name = output_file_name
        return self

    def generate_routes_by_domain(self):
        self.__append_routes_by_domain = Domain(self.__domain)
        return self

    def generate_routes_by_referer(self):
        self.__append_routes_by_referer = Route()
        return self

    def append_routes_and_build(self):
        log = pandas.read_csv(Path.OUTPUT.value + self.__input_file_name, engine="python")

        if self.__append_routes_by_domain is not None:
            self.__append_routes_by_domain.generate(log)
            log.to_csv(Path.OUTPUT.value + self.__output_file_name, index=False)

        if self.__append_routes_by_referer is not None:
            self.__append_routes_by_referer.generate(log)
            log.to_csv(Path.OUTPUT.value + self.__output_file_name, index=False)

        return log
