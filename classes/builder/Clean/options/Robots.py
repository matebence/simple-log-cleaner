from classes.utilities.Path import Path


class Robots:

    def __init__(self):
        self.__bot_ips = set()
        self.__ROBOT = "robots.txt"
        self.__agents: None

    def set_agents_source(self, file_name):
        self.__agents = open(Path.FILES.value + file_name, "r", encoding="utf8").readline().split(", ")

    def get_agents_source(self):
        return self.__agents

    def black_list_ip(self, requested_url, ip_address):
        if self.__ROBOT.lower() in requested_url.lower():
            self.__bot_ips.add(ip_address)
            return True
        return False

    def remove_by_user_agent(self, user_agent):
        for agent in self.__agents:
            if agent.lower() in user_agent.lower():
                return True
        return False

    def remove_by_ip(self, ip_address):
        for bot_ip in self.__bot_ips:
            if bot_ip == ip_address:
                return True
        return False
