from classes.utilities.Columns import Columns


class Route:

    def __init__(self, items):
        self.__ignored_items = items

    def insert_row(self, index, row):
        return row.append(row.iloc[index], ignore_index=False).sort_index().reset_index(drop=True)

    def generate(self, row):
        index = 1
        while index < row.shape[0]:
            prev_row = row.iloc[index - 1]
            if row[Columns.RL.value].iloc[index] == prev_row[Columns.RL.value] \
                    and prev_row[Columns.REQUEST_URL.value] != row[Columns.REFERER.value].iloc[index] \
                    and prev_row[Columns.REQUEST_URL.value] != row[Columns.REQUEST_URL.value].iloc[index] \
                    and False not in [str(x) not in row[Columns.REFERER.value].iloc[index] for x in self.__ignored_items]:
                row = self.insert_row(index, row)
                row.at[index, Columns.LENGTH.value] = 1
                row.at[index, Columns.REQUEST_URL.value] = prev_row[Columns.REFERER.value]
                row.at[index, Columns.REFERER.value] = None
                index += 1
            index += 1

        return row
