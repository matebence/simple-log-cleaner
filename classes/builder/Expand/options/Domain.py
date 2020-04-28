import requests
import random

from classes.utilities.Columns import Columns


class Domain:

    __request = None

    def __init__(self, domain):
        self.__domain = domain
        self.__servers = []

    def init_session(self):
        self.__request = requests.session()
        self.__request.proxies = {"http": self.get_proxy_servers()[self.change_ip()], "https":  self.get_proxy_servers()[self.change_ip()]}

    def change_ip(self):
        return random.randint(0, len(self.get_proxy_servers()) - 1)

    def set_proxy_servers(self, ip_addresses):
        self.__servers = ip_addresses

    def get_proxy_servers(self):
        return self.__servers

    def web_page_contains_url(self, row, index, request):
        return row[Columns.REQUEST_URL.value].iloc[index] in request.text and self.__domain + row[Columns.REQUEST_URL.value].iloc[index] in request.text

    def is_inserted(self, row, index):
        return row[Columns.REQUEST_URL.value].iloc[index] != row[Columns.REQUEST_URL.value].iloc[index - 2]

    def insert_row(self, index, data_frame, insert):
        first = data_frame.iloc[:index, ]
        second = data_frame.iloc[index:, ]

        data_frame = first.append(insert).append(second)
        data_frame.index = data_frame.index + 1
        data_frame = data_frame.sort_index()

        return data_frame

    def generate(self, row):
        index = 1
        while index < row.shape[0]:
            prev_row = row.iloc[index - 1]
            if row[Columns.RL.value].iloc[index] == prev_row[Columns.RL.value]:
                try:
                    self.init_session()
                    approval = self.__request.get(self.__domain + prev_row[Columns.REQUEST_URL.value])
                    if approval.ok and not self.web_page_contains_url(row, index, approval) and self.is_inserted(row, index):
                        row = self.insert_row(index - 1, row, row.iloc[index - 2])
                        row.at[index, Columns.LENGTH.value] = 1
                        index -= 1
                except:
                    index -= 1
            index += 1
