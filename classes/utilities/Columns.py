from enum import Enum


class Columns(Enum):
    IP_ADDRESS = "ip_address"
    COOKIE_ID = "cookie_id"
    USER_ID = "user_id"
    TIMESTAMP = "timestamp"
    REQUEST_METHOD = "request_method"
    REQUEST_URL = "requested_url"
    HTTP_VERSION = "http_version"
    HTTP_STATUS = "http_status"
    FILE_SIZE = "file_size"
    REFERER = "referer"
    USER_AGENT = "user_agent"
