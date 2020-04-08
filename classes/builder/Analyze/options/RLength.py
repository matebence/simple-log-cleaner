import pandas
import math

from classes.utilities.Columns import Columns


class RLength:
    __P = 0.4
    __C = None

    def __init__(self):
        self.__rl = 0
        self.__total = 0

    def increase_rl(self):
        self.__rl += 1

    def get_rl(self):
        return self.__rl

    def increase_total(self, value):
        self.__total += value

    def get_total(self):
        return self.__total

    def set_total(self, value):
        self.__total = value

    def get_c(self, log):
        self.__C = -math.log(1 - self.__P) / (1 / log[Columns.LENGTH.value].mean())
        return self.__C

    def generate(self, row):
        self.get_c(row)
        for index in range(1, row.shape[0]):
            prev_row = row.iloc[index - 1]
            if row[Columns.USER_ID.value].iloc[index] == prev_row[Columns.USER_ID.value]:
                if not pandas.isna(row[Columns.LENGTH.value].astype(float).iloc[index - 1]):
                    self.increase_total(row[Columns.LENGTH.value].astype(float).iloc[index - 1])
                if self.get_total() <= self.__C:
                    row.at[index - 1, Columns.RL.value] = self.get_rl()
                else:
                    row.at[index - 1, Columns.RL.value] = self.get_rl()
                    self.set_total(0)
                    self.increase_rl()
            else:
                row.at[index - 1, Columns.RL.value] = self.get_rl()
                self.set_total(0)
                self.increase_rl()
