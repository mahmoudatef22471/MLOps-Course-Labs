"""
Model loading and prediction logic.

The model must be loaded ONCE at module level, NOT inside the predict function.
"""

import joblib
import pandas as pd

data_transformed = joblib.load("data/column_transformer.joblib")

model = joblib.load("data/model.pkl")


def predict_churn(features: list[float]) -> int:
    """
    Takes a list of feature values and returns a churn prediction (0 or 1).
    """

    column_names = [
        "CreditScore",
        "Geography",
        "Gender",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "EstimatedSalary",
    ]

    df = pd.DataFrame([features], columns=column_names)
    features_transformed = data_transformed.transform(df)
    prediction = model.predict(features_transformed)
    return int(prediction[0])


if __name__ == "__main__":
    # TODO 3: Replace with sample features that match your model

    sample = [619, "France", "Female", 42, 2, 0, 1, 1, 1, 101348.88]

    print(f"Input:      {sample}")
    print(f"Prediction: {predict_churn(sample)}")
