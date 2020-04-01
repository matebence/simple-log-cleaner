import pandas

from classes.builder.Analyze.options.Time import Time
from classes.builder.Analyze.options.User import User
from classes.builder.Analyze.options.Length import Length
from classes.builder.Analyze.Analyze import Analyze
from classes.utilities.Columns import Columns
from classes.utilities.Path import Path


class AnalyzeLog(Analyze):
    __user = None
    __length = None
    __unix_time = None

    def __init__(self):
        self.__log = None
        self.__input_file_name = None
        self.__output_file_name = None

    def from_file(self, input_file_name):
        self.__input_file_name = input_file_name
        return self

    def to_file(self, output_file_name):
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

    def analyze_and_build(self):
        self.__log = pandas.read_csv(Path.OUTPUT.value + self.__input_file_name, sep="#", engine="python")
        self.__log.sort_values(by=[Columns.IP_ADDRESS.value, Columns.TIMESTAMP.value], inplace=True)

        if self.__unix_time is not None:
            self.__log.insert(1, Columns.UNIX_TIME.value, self.__unix_time.generate(self.__log[Columns.TIMESTAMP.value]).unix_seconds())

        if self.__user is not None:
            self.__log.insert(0, Columns.USER_ID.value, self.__user.generate_id(self.__log))

        if self.__length is not None:
            self.__log.insert(0, Columns.INDEX_COLUMN.value, self.__log.index)
            self.__log.insert(3, Columns.LENGTH.value, '')
            self.__log.insert(4, Columns.STT.value, '')
            self.__length.generate(self.__log)

        self.__log.to_csv(Path.OUTPUT.value + self.__output_file_name, index=False)
