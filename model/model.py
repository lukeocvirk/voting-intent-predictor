import joblib
import pandas as pd
import numpy as np

from sklearn.discriminant_analysis import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

DATA = "../refined_data/RefinedVoteIntentionsDatabase.csv"
MODEL = "baseline.joblib"

def main() -> None:
    df = pd.read_csv(DATA)

    y = df["vote_intention"].astype(int)
    X = df[[
        "year",
        "region",
        "province",
        "gender",
        "age_cats",
        "degree",
        "language",
    ]].copy()

    categorical = ["region", "province", "gender", "age_cats", "degree", "language"]
    numeric = ["year"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", StandardScaler(), numeric),
        ]
    )

    clf = LogisticRegression(
        solver="saga",
        max_iter=8000,
    )

    model = Pipeline(steps=[
        ("prep", preprocessor),
        ("clf", clf),
    ])

    train_df = df[df["year"].isin([2014, 2015, 2016, 2018, 2020, 2019, 2021, 2022])]
    test_df = df[df["year"].isin([2023])]

    X_train = train_df[X.columns]
    y_train = train_df["vote_intention"].astype(int)

    X_test = test_df[X.columns]
    y_test = test_df["vote_intention"].astype(int)

    print("Train years:", sorted(train_df["year"].unique())[-5:], "…")
    print("Test years:", sorted(test_df["year"].unique()))
    print("Train size:", len(train_df), "Test size:", len(test_df))

    # Train
    model.fit(X_train, y_train)

    # Save model
    priors = {}
    for col in ["region", "province", "gender", "age_cats", "degree", "language"]:
        priors[col] = train_df[col].value_counts(normalize=True)
    joblib.dump({"model": model, "priors": priors}, "baseline_bundle.joblib")

    # Evaluate
    proba = model.predict_proba(X_test)
    pred = model.predict(X_test)

    print("Accuracy:", round(accuracy_score(y_test, pred), 4))
    print("Log loss:", round(log_loss(y_test, proba), 4))
    print("\nClass counts in test:")
    print(y_test.value_counts().sort_index())
    print("\nClassification report:")
    print(classification_report(y_test, pred, digits=4))

    joblib.dump(model, MODEL)
    print(f"\nSaved model to {MODEL}")


if __name__ == "__main__":
    main()