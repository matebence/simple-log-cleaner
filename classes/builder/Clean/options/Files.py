from classes.utilities.Path import Path


class Files:
    __extensions: None

    def __init__(self):
        self.__extensions = ""

    def set_extensions_source(self, file_name):
        self.__extensions = open(Path.FILES.value + file_name, "r", encoding="utf8").readline().split(", ")

    def get_extensions_source(self):
        return self.__extensions

    def remove(self, at_line):
        for extension in self.__extensions:
            if extension.lower() in at_line.lower():
                return True
        return False
