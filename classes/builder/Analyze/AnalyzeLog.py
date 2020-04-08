import pandas
import pathlib

from classes.builder.Analyze.options.Time import Time
from classes.builder.Analyze.options.User import User
from classes.builder.Analyze.options.Length import Length
from classes.builder.Analyze.options.RLength import RLength
from classes.builder.Analyze.Analyze import Analyze
from classes.utilities.Columns import Columns
from classes.utilities.Path import Path


class AnalyzeLog(Analyze):
    __user = None
    __length = None
    __rlength = None
    __unix_time = None

    def __init__(self):
        self.__log = None
        self.__input_file_name = None
        self.__output_file_name = None

    def from_file(self, input_file_name):
        self.__input_file_name = input_file_name
        return self

    def analyze_to_file(self, output_file_name):
        self.__output_file_name = output_file_name
        return self

    def generate_unix_time(self):
        self.__unix_time = Time()
        return self

    def identify_user(self):
        self.__user = User()
        return self

    def generate_time_length(self):
        self.__length = Length()
        return self

    def generate_rlength(self):
        self.__rlength = RLength()
        return self

    def __does_output_file_exists(self):
        if pathlib.Path(Path.OUTPUT.value + self.__output_file_name).exists():
            self.__log = pandas.read_csv(Path.OUTPUT.value + self.__output_file_name, index_col=None)

    def analyze_and_build(self):
        self.__log = pandas.read_csv(Path.OUTPUT.value + self.__input_file_name, sep="#", engine="python")

        if self.__unix_time is not None:
            self.__does_output_file_exists()
            if Columns.UNIX_TIME.value not in self.__log:
                self.__log.insert(1, Columns.UNIX_TIME.value, '')
            self.__log[Columns.UNIX_TIME.value] = self.__unix_time.generate(
                self.__log[Columns.TIMESTAMP.value]).unix_seconds()
            self.__log.to_csv(Path.OUTPUT.value + self.__output_file_name, index=False)

        if self.__user is not None:
            self.__does_output_file_exists()
            self.__log.sort_values(by=[Columns.IP_ADDRESS.value, Columns.TIMESTAMP.value], inplace=True)
            if Columns.USER_ID.value not in self.__log:
                self.__log.insert(0, Columns.USER_ID.value, '')
            self.__log[Columns.USER_ID.value] = self.__user.generate_id(self.__log)
            self.__log.to_csv(Path.OUTPUT.value + self.__output_file_name, index=False)

        if self.__length is not None:
            self.__does_output_file_exists()
            if Columns.LENGTH.value not in self.__log and Columns.STT.value not in self.__log:
                self.__log.insert(3, Columns.LENGTH.value, '')
                self.__log.insert(4, Columns.STT.value, '')
            self.__length.generate(self.__log)
            self.__log.to_csv(Path.OUTPUT.value + self.__output_file_name, index=False)

        if self.__rlength is not None:
            self.__does_output_file_exists()
            if Columns.RL.value not in self.__log:
                self.__log.insert(5, Columns.RL.value, '')
            self.__rlength.generate(self.__log)
            self.__log.to_csv(Path.OUTPUT.value + self.__output_file_name, index=False)
