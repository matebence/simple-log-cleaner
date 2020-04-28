import os
import pathlib
import pandas

from classes.builder.Clean.Clean import Clean
from classes.builder.Clean.options.Robots import Robots
from classes.builder.Clean.options.Files import Files
from classes.builder.Clean.options.Http import Http
from classes.utilities.Identify import Identify
from classes.utilities.Path import Path
from classes.utilities.Columns import Columns


class CleanLog(Clean):

    def __init__(self):
        self.__files = self.__columns = self.__robots = self.__http = self.__url = None
        self.__input_file_name = self.__output_file_name = None
        self.__output_file = self.__input_file = None
        self.__clean_up = self.__headers = False

    def from_file(self, input_file_name):
        self.__input_file_name = input_file_name
        return self

    def to_file(self, output_file_name):
        self.__output_file_name = output_file_name
        return self

    def prepend_request_url(self, url):
        self.__url = url
        return self

    def define_redundant_columns(self, columns):
        self.__columns = columns
        return self

    def remove_redundant_data(self):
        self.__files = Files()
        self.__files.set_extensions_source("extensions.txt")
        return self

    def remove_http_statuses(self):
        if self.__http is None:
            self.__http = Http()
        self.__http.set_status_source("statuses.txt")
        return self

    def remove_http_methods(self):
        if self.__http is None:
            self.__http = Http()
        self.__http.set_method_source("methods.txt")
        return self

    def remove_http_requests(self):
        if self.__http is None:
            self.__http = Http()
        self.__http.set_request_source("requests.txt")
        return self

    def remove_robots(self):
        self.__robots = Robots()
        self.__robots.set_agents_source("agents.txt")
        return self

    def __is_writing_header_data(self):
        return (self.__headers is False) \
               and (self.__clean_up is True or self.__robots is None)

    def is_not_writing_to_temp_file(self):
        return self.__clean_up is True \
               or self.__robots is None

    def __is_generating_temp_file(self, line):
        return line == "" \
               and self.__clean_up is False \
               and self.__robots is not None

    def __is_about_to_finish_without_temp_file(self, line):
        return line == "" \
               and self.__clean_up is False \
               and self.__robots is None

    def __is_file_extension_removing_enabled(self, column_request_url):
        return self.__files is not None \
               and self.__files.get_extensions_source() is not None \
               and self.__files.remove(column_request_url)

    def __is_http_status_removing_enabled(self, column_http_status):
        return self.__http is not None \
               and self.__http.get_status_source() is not None \
               and self.__http.remove_statuses(column_http_status)

    def __is_http_method_removing_enabled(self, column_request_method):
        return self.__http is not None \
               and self.__http.get_method_source() is not None \
               and self.__http.remove_methods(column_request_method)

    def __is_http_request_removing_enabled(self, column_request_url):
        return self.__http is not None\
               and self.__http.get_request_source() is not None \
               and self.__http.remove_request(column_request_url)

    def __is_agent_removing_enabled(self, column_user_agent):
        return self.__robots is not None \
               and self.__robots.get_agents_source() is not None \
               and self.__robots.remove_by_user_agent(column_user_agent)

    def __is_robot_ip_blacklisting_enabled(self, column_request_url, column_ip_address):
        return self.__robots is not None \
               and self.__robots.black_list_ip(column_request_url, column_ip_address)

    def __is_column_allowed(self, data):
        return data.upper() not in self.__columns \
               and (self.__clean_up is True or self.__robots is None)

    def __is_about_to_finish_with_temp_file(self, line):
        return line == "" and self.__clean_up is True

    def __is_ip_removing_enabled(self, column_ip_address):
        return self.__robots.remove_by_ip(column_ip_address)

    def clean_and_build(self):
        temp_file = open(Path.OUTPUT.value + "temp.log", "w", encoding="utf8")
        self.__input_file = open(Path.INPUT.value + self.__input_file_name, "r", encoding="utf8")
        line = "empty"

        while line:
            line = self.__input_file.readline()
            items = Identify.items_from_log(line, self.__clean_up)

            if self.__is_generating_temp_file(line):
                temp_file.close()
                self.__input_file.close()
                self.__output_file = open(Path.OUTPUT.value + self.__output_file_name, "w", encoding="utf8")
                self.__input_file = open(Path.OUTPUT.value + "temp.log", "r", encoding="utf8")
                self.__clean_up = True
                self.__headers = False
                line = self.__input_file.readline()
                items = Identify.items_from_log(line, self.__clean_up)

            elif self.__is_about_to_finish_with_temp_file(line):
                self.__output_file.close()
                self.__input_file.close()
                os.remove(Path.OUTPUT.value + "temp.log") if pathlib.Path(Path.OUTPUT.value + "temp.log").exists() else None

            elif self.__is_about_to_finish_without_temp_file(line):
                self.__output_file = temp_file
                self.__output_file.close()
                self.__input_file.close()
                temp_file.close()
                os.rename(Path.OUTPUT.value + "temp.log", Path.OUTPUT.value + self.__output_file_name)

            if items is not None:
                if self.__clean_up:
                    if self.__is_ip_removing_enabled(items[Columns.IP_ADDRESS.value]):
                        continue
                    self.__write_to_file(items, self.__output_file)
                else:
                    items[Columns.REQUEST_URL.value] = self.__url + items[Columns.REQUEST_URL.value]

                    if self.__is_file_extension_removing_enabled(items[Columns.REQUEST_URL.value]):
                        continue
                    if self.__is_http_status_removing_enabled(items[Columns.HTTP_STATUS.value]):
                        continue
                    if self.__is_http_method_removing_enabled(items[Columns.REQUEST_METHOD.value]):
                        continue
                    if self.__is_http_request_removing_enabled(items[Columns.REQUEST_URL.value]):
                        continue
                    if self.__is_robot_ip_blacklisting_enabled(items[Columns.REQUEST_URL.value], items[Columns.IP_ADDRESS.value]):
                        continue
                    if self.__is_agent_removing_enabled(items[Columns.USER_AGENT.value]):
                        continue
                    self.__write_to_file(items, temp_file)

        return pandas.read_csv(Path.OUTPUT.value + self.__output_file_name, sep="#", engine="python")

    def __write_to_file(self, datas, file):
        if self.__is_writing_header_data():
            file.write('#'.join([data for data in datas if self.__is_column_allowed(data)])+"\n")
        if self.is_not_writing_to_temp_file():
            file.write('#'.join([datas[data] for data in datas if self.__is_column_allowed(data)])+"\n")
        else:
            file.write(' '.join([datas[data] for data in datas if not self.__is_column_allowed(data)])+"\n")
        self.__headers = True
