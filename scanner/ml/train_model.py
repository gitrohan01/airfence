import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

from scanner.models import NetworkObservation


def fetch_data():
    data = NetworkObservation.objects.all().values(
        'encryption', 'rssi', 'channel', 'classification'
    )
    return pd.DataFrame(data)


def preprocess(df):
    # Encode encryption
    df['encryption'] = df['encryption'].astype('category').cat.codes

    # Encode target
    df['classification'] = df['classification'].astype('category').cat.codes

    X = df[['encryption', 'rssi', 'channel']]
    y = df['classification']

    return X, y


def train():
    df = fetch_data()

    X, y = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2
    )

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    acc = model.score(X_test, y_test)

    print(f"Accuracy: {acc}")

    joblib.dump(model, "scanner/ml/model.pkl")


if __name__ == "__main__":
    train()