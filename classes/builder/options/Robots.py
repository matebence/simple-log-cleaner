from classes.utilities.Path import Path


class Robots:
    __ROBOT = "robots.txt"
    __bot_ips: None
    __bots: None

    def __init__(self, file_name):
        self.__bots = open(Path.FILES.value + file_name, "r", encoding="utf8").readline().split(", ")
        self.__bot_ips = set()

    def black_list_ip(self, requested_url, ip_address):
        if self.__ROBOT in requested_url.lower():
            self.__bot_ips.add(ip_address)
            return True
        return False

    def remove_by_user_agent(self, user_agent):
        for bot in self.__bots:
            if bot in user_agent.lower():
                return True
        return False

    def remove_by_ip(self, ip_address):
        for bot_ip in self.__bot_ips:
            if bot_ip == ip_address:
                return True
        return False
