import joblib
import pandas as pd

model = joblib.load("scanner/ml/model.pkl")

def predict_network(data):
    df = pd.DataFrame([data])

    # Encode encryption same as training
    df['encryption'] = df['encryption'].astype('category').cat.codes

    X = df[['encryption', 'rssi', 'channel']]

    pred = model.predict(X)[0]

    mapping = {
        0: "Critical",
        1: "Risky",
        2: "Secure"
    }

    return mapping.get(pred, "Unknown")