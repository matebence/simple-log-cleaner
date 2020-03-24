from classes.utilities.Path import Path


class Http:
    __statuses: None
    __methods: None
    __requests: None

    def set_status_source(self, file_name):
        self.__statuses = open(Path.FILES.value + file_name, "r", encoding="utf8").readline().split(", ")

    def set_method_source(self, file_name):
        self.__methods = open(Path.FILES.value + file_name, "r", encoding="utf8").readline().split(", ")

    def set_request_srouce(self, file_name):
        self.__requests = open(Path.FILES.value + file_name, "r", encoding="utf8").read().split("\n")

    def remove_statuses(self, at_line):
        for status in self.__statuses:
            if int(at_line) < int(status):
                return False
        return True

    def remove_methods(self, at_line):
        for method in self.__methods:
            if method in at_line.lower():
                return True
        return False

    def remove_request(self, at_line):
        for request in self.__requests:
            if request == at_line.lower():
                return True
        return False
