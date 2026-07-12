from fastapi import APIRouter
from ev_statistics.descriptive import EVStatistics

router = APIRouter()
stats = EVStatistics()

@router.get("/summary")
def summary():
    return stats.basic_summary()

@router.get("/top-makes")
def top_makes():
    return stats.top_makes()

@router.get("/ev-distribution")
def ev_distribution():
    return stats.ev_type_distribution()

@router.get("/cafv-distribution")
def cafv_distribution():
    return stats.cafv_distribution()

@router.get("/yearly-registrations")
def yearly_registrations():
    return stats.yearly_registrations()

@router.get("/top-cities")
def top_cities():
    return stats.top_cities()

@router.get("/correlation")
def correlation():
    return stats.correlation_matrix()

@router.get("/skewness-kurtosis")
def skewness():
    return stats.skewness_kurtosis()

@router.get("/outliers")
def outliers():
    return stats.outlier_analysis()

@router.get("/city/{city}")
def city_analysis(city: str):
    return stats.city_insights(city)

@router.get("/make/{make}")
def make_analysis(make: str):
    return stats.make_analysis(make)
