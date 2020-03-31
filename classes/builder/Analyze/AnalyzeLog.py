import pandas

from classes.builder.Analyze.options.UnixTime import UnixTime
from classes.builder.Analyze.Analyze import Analyze
from classes.utilities.Columns import Columns
from classes.utilities.Path import Path


class AnalyzeLog(Analyze):
    __unix_time = None

    def __init__(self):
        self.__input_file_name = None
        self.__output_file_name = None

    def from_file(self, input_file_name):
        self.__input_file_name = input_file_name
        return self

    def to_file(self, output_file_name):
        self.__output_file_name = output_file_name
        return self

    def generate_unix_time(self):
        self.__unix_time = UnixTime()
        return self

    def identify_user(self): pass

    def generate_time_length(self): pass

    def analise_and_build(self):
        data = pandas.read_csv(Path.OUTPUT.value + self.__input_file_name, sep="#", engine="python", index_col=None)
        data[Columns.UNIX_TIME.value] = self.__unix_time.generate(data[Columns.TIMESTAMP.value]).unix_seconds()
        print(data[[Columns.UNIX_TIME.value, Columns.TIMESTAMP.value]])
