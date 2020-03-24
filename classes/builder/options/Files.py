from classes.utilities.Path import Path


class Files:
    __extensions: None

    def __init__(self, file_name):
        self.__extensions = open(Path.FILES.value + file_name, "r", encoding="utf8").readline().split(", ")

    def remove(self, at_line):
        for extension in self.__extensions:
            if extension in at_line.lower():
                return True
        return False
