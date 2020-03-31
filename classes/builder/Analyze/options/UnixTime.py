import time

from datetime import datetime


class UnixTime:
    __date_time: None
    __time_zone: None

    def get_date_time(self):
        return self.__date_time

    def get_time_zone(self):
        return self.__time_zone

    def generate(self, timestamp):
        self.__date_time = timestamp.apply(lambda x: x.split(" ")[0])
        self.__time_zone = timestamp.apply(lambda x: x.split(" ")[1])
        return self

    def unix_seconds(self):
        return self.get_date_time().apply(lambda x: int(time.mktime(datetime.strptime(x, "%d/%b/%Y:%H:%M:%S").timetuple())))
