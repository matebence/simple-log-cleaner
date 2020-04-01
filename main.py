from classes.builder.Clean.CleanLog import CleanLog
from classes.builder.Analyze.AnalyzeLog import AnalyzeLog
from classes.utilities.Columns import Columns


def main():

    CleanLog() \
        .from_file("web.log") \
        .to_file("web.clean.csv") \
        .define_redundant_columns([Columns.USER.value, Columns.COOKIE_ID.value]) \
        .remove_redundant_data_by() \
        .remove_http_statuses_by() \
        .remove_http_methods_by() \
        .remove_http_requests_by() \
        .remove_robots_by()\
        .clean_and_build()

    AnalyzeLog() \
        .from_file("web.clean.csv") \
        .to_file("web.analyze.csv") \
        .generate_unix_time()\
        .identify_user()\
        .generate_time_length()\
        .analyze_and_build()


if __name__ == "__main__":
    main()
