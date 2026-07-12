from fastapi import APIRouter
from pydantic import BaseModel
from ml.predictor import EVPredictor
from ml.evaluator import compare_models, get_best_model

router = APIRouter()
predictor = None

class PredictionRequest(BaseModel):
    model_year: int
    make: str
    ev_type: str
    electric_range: float

@router.get("/models")
def model_comparison():
    df = compare_models()
    return df.to_dict(orient="records")

@router.get("/best-model")
def best_model():
    return get_best_model().to_dict()

@router.post("/predict")
def predict(request: PredictionRequest):
    global predictor
    if predictor is None:
        predictor = EVPredictor()

    return predictor.predict(
        model_year=request.model_year,
        make=request.make,
        ev_type=request.ev_type,
        electric_range=request.electric_range,
    )
