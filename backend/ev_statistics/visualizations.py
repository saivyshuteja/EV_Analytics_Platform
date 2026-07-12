import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = BACKEND_DIR / "data" / "raw" / "ev_data.csv"
CHARTS_DIR = BACKEND_DIR / "statistics" / "charts"


class EVVisualizations:

    def __init__(self):

        self.df = pd.read_csv(
            RAW_DATA_PATH
        )
        CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    def top_makes_chart(self):

        plt.figure(
            figsize=(12,6)
        )

        (
            self.df["Make"]
            .value_counts()
            .head(10)
            .plot(
                kind="bar"
            )
        )

        plt.title(
            "Top 10 EV Manufacturers"
        )

        plt.tight_layout()

        plt.savefig(
            CHARTS_DIR / "top_makes.png"
        )

    def ev_type_chart(self):

        plt.figure(
            figsize=(8,6)
        )

        (
            self.df[
                "Electric Vehicle Type"
            ]
            .value_counts()
            .plot(
                kind="pie",
                autopct="%1.1f%%"
            )
        )

        plt.ylabel("")

        plt.savefig(
            CHARTS_DIR / "ev_type_distribution.png"
        )

    def yearly_growth_chart(self):

        yearly = (

            self.df["Model Year"]
            .value_counts()
            .sort_index()
        )

        plt.figure(
            figsize=(12,6)
        )

        plt.plot(
            yearly.index,
            yearly.values
        )

        plt.title(
            "Year Wise EV Registrations"
        )

        plt.xlabel(
            "Model Year"
        )

        plt.ylabel(
            "Count"
        )

        plt.grid()

        plt.savefig(
            CHARTS_DIR / "yearly_growth.png"
        )

    def correlation_heatmap(self):

        numeric = self.df.select_dtypes(
            include="number"
        )

        plt.figure(
            figsize=(10,8)
        )

        sns.heatmap(

            numeric.corr(),

            annot=True,

            cmap="coolwarm"
        )

        plt.savefig(
            CHARTS_DIR / "correlation_heatmap.png"
        )


if __name__ == "__main__":

    viz = EVVisualizations()

    viz.top_makes_chart()

    viz.ev_type_chart()

    viz.yearly_growth_chart()

    viz.correlation_heatmap()
