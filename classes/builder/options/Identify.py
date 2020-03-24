import re

from classes.utilities.Columns import Columns


class Identify:

    @staticmethod
    def items_from_log(line, clean_up):
        if line != "":
            regex = re.search(
                '^(\S+) (\S+) (\S+) ([\w:/]+\s[+\-]\d{4}) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)'
                if clean_up else
                '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S+)?\s*" (\d{3}) (\d+) "(\S+)" "(\S.*)"',
                line)
            return {
                Columns.IP_ADDRESS.value: regex.group(1),
                Columns.COOKIE_ID.value: regex.group(2),
                Columns.USER_ID.value: regex.group(3),
                Columns.TIMESTAMP.value: regex.group(4),
                Columns.REQUEST_METHOD.value: regex.group(5),
                Columns.REQUEST_URL.value: regex.group(6),
                Columns.HTTP_VERSION.value: regex.group(7),
                Columns.HTTP_STATUS.value: regex.group(8),
                Columns.FILE_SIZE.value: regex.group(9),
                Columns.REFERER.value: regex.group(10),
                Columns.USER_AGENT.value: regex.group(11),
            }
        else:
            return None
