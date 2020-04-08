import numpy

from classes.utilities.Columns import Columns


class Length:
    __STT = 3600

    def __init__(self):
        self.__stt_id = 0

    def increase_stt_id(self):
        self.__stt_id += 1

    def get_stt_id(self):
        return self.__stt_id

    def get_length(self, row, prev_row, index):
        diff = row[Columns.UNIX_TIME.value].iloc[index] - prev_row[Columns.UNIX_TIME.value]
        if self.__STT > diff >= 0:
            return float(diff)
        else:
            self.increase_stt_id()
            return float(numpy.nan)

    def generate(self, row):
        for index in range(1, row.shape[0]):
            prev_row = row.iloc[index - 1]
            if row[Columns.USER_ID.value].iloc[index] == prev_row[Columns.USER_ID.value]:
                row.at[index - 1, Columns.STT.value] = self.get_stt_id()
                row.at[index - 1, Columns.LENGTH.value] = self.get_length(row, prev_row, index)
            else:
                row.at[index - 1, Columns.STT.value] = self.get_stt_id()
                self.increase_stt_id()
