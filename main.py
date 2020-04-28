from classes.builder.Clean.CleanLog import CleanLog
from classes.builder.Analyze.AnalyzeLog import AnalyzeLog
from classes.builder.Expand.ExpandLog import ExpandLog
from classes.utilities.Columns import Columns
from classes.gui.Table import Table


def main():
    clean_log = CleanLog() \
        .from_file("web.log") \
        .to_file("web.clean.csv") \
        .prepend_request_url("https://www.ukf.sk") \
        .define_redundant_columns([Columns.USER.value, Columns.COOKIE_ID.value]) \
        .remove_redundant_data() \
        .remove_http_statuses() \
        .remove_http_methods() \
        .remove_http_requests() \
        .remove_robots() \
        .clean_and_build()

    analyze_log = AnalyzeLog() \
        .from_file("web.clean.csv") \
        .to_file("web.analyze.csv") \
        .generate_unix_time() \
        .identify_user() \
        .generate_time_length() \
        .generate_rlength() \
        .analyze_and_build()

    route_log = ExpandLog() \
        .from_file("web.analyze.csv") \
        .to_file("web.route.csv") \
        .ignore(["google", "bing", "facebook", "foto", "webmail", "finder/search?", "-", None]) \
        .generate_routes_by_referer() \
        .append_routes_and_build()

    table_log = Table()\
        .set_data_frame(route_log) \
        .start_gui()


if __name__ == "__main__":
    main()
