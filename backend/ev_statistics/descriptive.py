import pandas as pd
import numpy as np
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = BACKEND_DIR / "data" / "raw" / "ev_data.csv"


class EVStatistics:

    def __init__(self):

        self.df = pd.read_csv(
            RAW_DATA_PATH
        )

    def basic_summary(self):

        columns = [
            "Model Year",
            "Electric Range",
            "Base MSRP"
        ]
        columns = [col for col in columns if col in self.df.columns]

        return (
            self.df[columns]
            .describe()
            .to_dict()
        )

    def top_makes(self, top_n=10):

        return (
            self.df["Make"]
            .value_counts()
            .head(top_n)
            .to_dict()
        )

    def ev_type_distribution(self):

        counts = (
            self.df[
                "Electric Vehicle Type"
            ]
            .value_counts()
        )

        percentages = (
            counts /
            counts.sum()
        ) * 100

        return {

            "counts":
            counts.to_dict(),

            "percentages":
            percentages.round(2).to_dict()
        }

    def cafv_distribution(self):

        counts = (
            self.df[
                "Clean Alternative Fuel Vehicle (CAFV) Eligibility"
            ]
            .value_counts()
        )

        percentages = (
            counts /
            counts.sum()
        ) * 100

        return {

            "counts":
            counts.to_dict(),

            "percentages":
            percentages.round(2).to_dict()
        }

    def yearly_registrations(self):

        return (
            self.df["Model Year"]
            .value_counts()
            .sort_index()
            .to_dict()
        )

    def top_cities(self):

        return (
            self.df["City"]
            .value_counts()
            .head(15)
            .to_dict()
        )

    def correlation_matrix(self):

        numeric_cols = self.df.select_dtypes(
            include=np.number
        )

        return (
            numeric_cols
            .corr()
            .round(3)
            .to_dict()
        )

    def skewness_kurtosis(self):

        return {

            "Electric Range": {

                "skewness":
                float(
                    self.df[
                        "Electric Range"
                    ].skew()
                ),

                "kurtosis":
                float(
                    self.df[
                        "Electric Range"
                    ].kurtosis()
                )
            },

            "Model Year": {

                "skewness":
                float(
                    self.df[
                        "Model Year"
                    ].skew()
                ),

                "kurtosis":
                float(
                    self.df[
                        "Model Year"
                    ].kurtosis()
                )
            }
        }

    def outlier_analysis(self):

        result = {}

        numeric_cols = [
            "Model Year",
            "Electric Range",
            "Base MSRP"
        ]
        numeric_cols = [col for col in numeric_cols if col in self.df.columns]

        for col in numeric_cols:

            q1 = self.df[col].quantile(0.25)

            q3 = self.df[col].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - (1.5 * iqr)

            upper = q3 + (1.5 * iqr)

            result[col] = {

                "Q1": float(q1),

                "Q3": float(q3),

                "IQR": float(iqr),

                "Lower Bound": float(lower),

                "Upper Bound": float(upper)
            }

        return result

    def cafv_vs_evtype(self):

        table = pd.crosstab(

            self.df[
                "Clean Alternative Fuel Vehicle (CAFV) Eligibility"
            ],

            self.df[
                "Electric Vehicle Type"
            ]
        )

        return table.to_dict()

    def make_vs_evtype(self):

        top_makes = (
            self.df["Make"]
            .value_counts()
            .head(10)
            .index
        )

        filtered = self.df[
            self.df["Make"]
            .isin(top_makes)
        ]

        table = pd.crosstab(

            filtered["Make"],

            filtered[
                "Electric Vehicle Type"
            ]
        )

        return table.to_dict()

    def yoy_growth(self):

        yearly = (

            self.df["Model Year"]
            .value_counts()
            .sort_index()
        )

        growth = (
            yearly.pct_change() * 100
        )

        return (
            growth
            .fillna(0)
            .round(2)
            .to_dict()
        )

    def cumulative_count(self):

        yearly = (

            self.df["Model Year"]
            .value_counts()
            .sort_index()
        )

        cumulative = yearly.cumsum()

        return cumulative.to_dict()

    def city_insights(self, city):

        city_df = self.df[
            self.df["City"].str.upper()
            ==
            city.upper()
        ]

        return {

            "city":
            city,

            "vehicle_count":
            len(city_df),

            "top_makes":
            city_df["Make"]
            .value_counts()
            .head(5)
            .to_dict(),

            "ev_types":
            city_df[
                "Electric Vehicle Type"
            ]
            .value_counts()
            .to_dict()
        }

    def make_analysis(self, make):

        make_df = self.df[
            self.df["Make"].str.upper()
            ==
            make.upper()
        ]

        return {

            "make":
            make,

            "count":
            len(make_df),

            "year_distribution":
            make_df["Model Year"]
            .value_counts()
            .sort_index()
            .to_dict(),

            "ev_type_distribution":
            make_df[
                "Electric Vehicle Type"
            ]
            .value_counts()
            .to_dict()
        }


if __name__ == "__main__":

    stats = EVStatistics()

    print(
        stats.top_makes()
    )

    print(
        stats.ev_type_distribution()
    )

    print(
        stats.correlation_matrix()
    )
