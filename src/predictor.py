
import joblib
import pandas as pd

from pathlib import Path

# Locate the saved model
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "crop_model.pkl"

FEATURES = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
]


def load_model():
    """Load the trained crop classification model."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}. "
            "Run src/train_model.py first."
        )

    return joblib.load(MODEL_PATH)


def predict_crop(soil_data):
    """
    Predict a crop from a dictionary containing all seven
    required model features.
    """
    missing = [name for name in FEATURES if name not in soil_data]

    if missing:
        raise ValueError(f"Missing required features: {missing}")

    input_df = pd.DataFrame(
        [[soil_data[name] for name in FEATURES]],
        columns=FEATURES,
    )

    model = load_model()
    prediction = model.predict(input_df)[0]

    return str(prediction)


if __name__ == "__main__":
    example_soil = {
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 25.0,
        "humidity": 80.0,
        "ph": 6.5,
        "rainfall": 200.0,
    }

    crop = predict_crop(example_soil)
    print("Predicted crop:", crop)
