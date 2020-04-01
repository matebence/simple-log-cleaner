from classes.utilities.Columns import Columns


class Length:
    __STT = 3600

    def __init__(self):
        self.__stt_id = 0

    def increase_stt_id(self):
        self.__stt_id += 1

    def get_stt_id(self):
        return self.__stt_id

    def get_length(self, current_row, last_row, index):
        diff = current_row[Columns.UNIX_TIME.value].iloc[index] - last_row[Columns.UNIX_TIME.value]
        if self.__STT > diff > 0:
            return diff
        else:
            self.increase_stt_id()
            return ""

    def generate(self, current_row):
        last_row = current_row.iloc[0]
        for index in range(1, current_row.shape[0]):
            if current_row[Columns.USER_ID.value].iloc[index] == last_row[Columns.USER_ID.value]:
                current_row.at[last_row[Columns.INDEX_COLUMN.value], Columns.STT.value] = self.get_stt_id()
                current_row.at[last_row[Columns.INDEX_COLUMN.value], Columns.LENGTH.value] = str(self.get_length(current_row, last_row, index))
            else:
                current_row.at[last_row[Columns.INDEX_COLUMN.value], Columns.STT.value] = self.get_stt_id()
                self.increase_stt_id()
            last_row = current_row.iloc[index]
