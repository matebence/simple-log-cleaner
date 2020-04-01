import pandas


class User:

    def generate_id(self, log):
        return pandas.factorize(log.IP_ADDRESS + log.USER_AGENT)[0]
