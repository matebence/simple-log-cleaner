from classes.builder.CleanLog import CleanLog


def main():
    CleanLog() \
        .from_file("web.log") \
        .to_file("web.clean.log") \
        .remove_redundant_data_by("extensions.txt") \
        .remove_http_statuses_by("statuses.txt") \
        .remove_http_methods_by("methods.txt") \
        .remove_http_requests_by("requests.txt") \
        .remove_robots_by("bots.txt").build()


if __name__ == "__main__":
    main()
