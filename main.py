"""
Churn Prediction API

Run with:
    litestar --app main:app run --reload
Then open:
    http://localhost:8000/schema/swagger
"""

from litestar import Litestar, get, post
from pydantic import BaseModel

from app.logger_setup import setup_logging
from app.model_utils import predict_churn

logger = setup_logging()


# ---------------------------------------------------------------------------
# Request Schema
# ---------------------------------------------------------------------------
class ChurnRequest(BaseModel):
    CreditScore: int
    geography: str
    gender: str
    age: int
    tenure: int
    balance: float
    num_of_products: int
    has_cr_card: int
    is_active_member: int
    estimated_salary: float


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@get("/")
def home() -> dict:
    logger.info("Home endpoint accessed")
    return {"message": "Welcome to the Churn Prediction API"}


@get("/health")
def health() -> dict:
    return {"status": "healthy"}


@post("/predict")
def predict(data: ChurnRequest) -> dict:
    features = [
        data.CreditScore,
        data.geography,
        data.gender,
        data.age,
        data.tenure,
        data.balance,
        data.num_of_products,
        data.has_cr_card,
        data.is_active_member,
        data.estimated_salary,
    ]
    prediction = predict_churn(features)
    logger.info("Predict called with features=%s, prediction=%s", features, prediction)
    return {"prediction": prediction}


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = Litestar(
    route_handlers=[home, health, predict],
)
