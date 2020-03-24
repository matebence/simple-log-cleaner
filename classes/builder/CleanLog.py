import os

from classes.builder.Clean import Clean
from classes.builder.options.Robots import Robots
from classes.builder.options.Files import Files
from classes.builder.options.Http import Http
from classes.builder.options.Identify import Identify
from classes.utilities.Path import Path
from classes.utilities.Columns import Columns


class CleanLog(Clean):
    __files = None
    __robots = None
    __http = None

    def __init__(self):
        self.__input_file_name = None
        self.__output_file_name = None
        self.__output_file = None
        self.__input_file = None
        self.__clean_up = False

    def from_file(self, input_file_name):
        self.__input_file_name = input_file_name
        return self

    def to_file(self, output_file_name):
        self.__output_file_name = output_file_name
        return self

    def remove_redundant_data_by(self, file_name):
        self.__files = Files(file_name)
        return self

    def remove_http_statuses_by(self, file_name):
        if self.__http is None:
            self.__http = Http()
        self.__http.set_status_source(file_name)
        return self

    def remove_http_methods_by(self, file_name):
        if self.__http is None:
            self.__http = Http()
        self.__http.set_method_source(file_name)
        return self

    def remove_http_requests_by(self, file_name):
        if self.__http is None:
            self.__http = Http()
        self.__http.set_request_srouce(file_name)
        return self

    def remove_robots_by(self, file_name):
        self.__robots = Robots(file_name)
        return self

    def __triger_final_cleanup(self):
        self.__clean_up = True
        self.__output_file = open(Path.OUTPUT.value + self.__output_file_name, "a", encoding="utf8")
        self.__input_file = open(Path.OUTPUT.value + "temp." + self.__output_file_name, "r", encoding="utf8")

    def __delete_temp_file(self, temp_file_name):
        os.remove(temp_file_name)

    def __write_to_file(self, datas, file):
        for data in datas:
            file.write(datas[data] + " ")
        file.write("\n")

    def build(self):
        self.__input_file = open(Path.INPUT.value + self.__input_file_name, "r", encoding="utf8")
        temp_file = open(Path.OUTPUT.value + "temp." + self.__output_file_name, "a", encoding="utf8")
        line = "empty"

        while line:
            line = self.__input_file.readline()
            items = Identify.items_from_log(line, self.__clean_up)

            if line == "" and self.__clean_up is False:
                temp_file.close()
                self.__input_file.close()
                self.__triger_final_cleanup()

                line = self.__input_file.readline()
                items = Identify.items_from_log(line, self.__clean_up)

            if items is not None:
                if self.__clean_up:
                    if self.__robots.remove_by_ip(items[Columns.IP_ADDRESS.value]):
                        continue
                    self.__write_to_file(items, self.__output_file)
                else:
                    if self.__files.remove(items[Columns.REQUEST_URL.value]):
                        continue
                    if self.__http.remove_statuses(items[Columns.HTTP_STATUS.value]):
                        continue
                    if self.__http.remove_methods(items[Columns.REQUEST_METHOD.value]):
                        continue
                    if self.__http.remove_request(items[Columns.REQUEST_URL.value]):
                        continue
                    if self.__robots.black_list_ip(items[Columns.REQUEST_URL.value], items[Columns.IP_ADDRESS.value]):
                        continue
                    if self.__robots.remove_by_user_agent(items[Columns.USER_AGENT.value]):
                        continue
                    self.__write_to_file(items, temp_file)

        self.__output_file.close()
        self.__input_file.close()
        self.__delete_temp_file(Path.OUTPUT.value + "temp." + self.__output_file_name)
