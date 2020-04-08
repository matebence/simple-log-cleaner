from classes.builder.Clean.CleanLog import CleanLog
from classes.utilities.Columns import Columns


def main():
    clean_log = CleanLog() \
        .from_file("web.log") \
        .to_file("web.clean.csv") \
        .define_redundant_columns([Columns.USER.value, Columns.COOKIE_ID.value]) \
        .remove_redundant_data() \
        .remove_http_statuses() \
        .remove_http_methods() \
        .remove_http_requests() \
        .remove_robots() \
        .clean_and_build()

    clean_log.analyze_to_file("web.analyze.csv") \
        .generate_unix_time() \
        .identify_user() \
        .generate_time_length() \
        .generate_rlength() \
        .analyze_and_build()


if __name__ == "__main__":
    main()
