import json
from pathlib import Path

try:
    from statistics.descriptive import EVStatistics
except ModuleNotFoundError:
    from descriptive import EVStatistics


BACKEND_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = BACKEND_DIR / "statistics" / "statistical_report.json"


class StatisticalReport:

    def __init__(self):

        self.stats = EVStatistics()

    def generate_report(self):

        report = {

            "summary":
            self.stats.basic_summary(),

            "top_makes":
            self.stats.top_makes(),

            "ev_distribution":
            self.stats.ev_type_distribution(),

            "cafv_distribution":
            self.stats.cafv_distribution(),

            "yearly_registrations":
            self.stats.yearly_registrations(),

            "top_cities":
            self.stats.top_cities(),

            "correlation_matrix":
            self.stats.correlation_matrix(),

            "skewness_kurtosis":
            self.stats.skewness_kurtosis(),

            "outlier_analysis":
            self.stats.outlier_analysis(),

            "cafv_vs_evtype":
            self.stats.cafv_vs_evtype(),

            "make_vs_evtype":
            self.stats.make_vs_evtype(),

            "yoy_growth":
            self.stats.yoy_growth(),

            "cumulative_count":
            self.stats.cumulative_count()
        }

        with open(REPORT_PATH, "w", encoding="utf-8") as f:

            json.dump(

                report,

                f,

                indent=4
            )

        return report


if __name__ == "__main__":

    report = StatisticalReport()

    report.generate_report()

    print(
        "Statistical Report Generated"
    )
