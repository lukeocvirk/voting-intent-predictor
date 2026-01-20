import argparse
import joblib
import numpy as np
import pandas as pd

BUNDLE_PATH_DEFAULT = "baseline_bundle.joblib"

FEATURE_COLS = ["year", "region", "province", "gender", "age_cats", "degree", "language"]
CAT_COLS = ["region", "province", "gender", "age_cats", "degree", "language"]

PARTY_LABELS = {
    1: "LPC",
    2: "CPC",
    3: "NDP",
    6: "GPC",
    10: "Other",
}

def sample_from_prior(prior_series: pd.Series, rng: np.random.Generator):
    vals = prior_series.index.to_numpy()
    probs = prior_series.to_numpy()
    return rng.choice(vals, p=probs)

def build_samples(user_fixed: dict, priors: dict, n: int, seed: int):
    rng = np.random.default_rng(seed)
    rows = []

    for _ in range(n):
        row = {}
        row["year"] = int(user_fixed.get("year", 2023))

        for col in CAT_COLS:
            if col in user_fixed and user_fixed[col] is not None:
                row[col] = user_fixed[col]
            else:
                row[col] = sample_from_prior(priors[col], rng)

        rows.append(row)

    return pd.DataFrame(rows, columns=FEATURE_COLS)

def main():
    parser = argparse.ArgumentParser(
        description="Sample synthetic voters and predict vote intention probabilities."
    )
    parser.add_argument("--bundle", default=BUNDLE_PATH_DEFAULT, help="Path to baseline_bundle.joblib")
    parser.add_argument("--n", type=int, default=100, help="Number of synthetic voters to sample")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--show-samples", action="store_true", help="Print sampled voter rows")

    # Optional
    parser.add_argument("--year", type=int, help="Year (e.g., 2023)")
    parser.add_argument("--region", type=int, help="Region code")
    parser.add_argument("--province", type=int, help="Province code")
    parser.add_argument("--gender", type=int, help="Gender code")
    parser.add_argument("--age_cats", type=int, help="Age category code")
    parser.add_argument("--degree", type=int, help="Degree code")
    parser.add_argument("--language", type=int, help="Language code")

    args = parser.parse_args()

    bundle = joblib.load(args.bundle)
    model = bundle["model"]
    priors = bundle["priors"]

    user_fixed = {}
    for k in ["year", "region", "province", "gender", "age_cats", "degree", "language"]:
        v = getattr(args, k)
        if v is not None:
            user_fixed[k] = v

    samples = build_samples(user_fixed, priors, n=args.n, seed=args.seed)

    if args.show_samples:
        print("\nSampled voters (first 20 shown):")
        print(samples.head(20).to_string(index=False))

    proba = model.predict_proba(samples)
    classes = model.named_steps["clf"].classes_

    mean_proba = proba.mean(axis=0)
    ranked = sorted(zip(classes, mean_proba), key=lambda x: x[1], reverse=True)

    print("\nAverage predicted party probabilities over sampled voters:")
    for cls, p in ranked:
        party = PARTY_LABELS.get(cls, f"Unknown ({cls})")
        print(f"  {party}: {p:.3f}")

    rng = np.random.default_rng(args.seed)

    # Simulate votes for synthetic voters
    sim_votes = [rng.choice(classes, p=proba[i]) for i in range(proba.shape[0])]

    vote_counts = pd.Series(sim_votes).value_counts()

    print("\nSimulated vote counts (stochastic draws):")
    for cls in classes:
        party = PARTY_LABELS.get(cls, f"Unknown ({cls})")
        print(f"  {party}: {int(vote_counts.get(cls, 0))}")

    print("\nSimulated vote percentages:")
    for cls in classes:
        party = PARTY_LABELS.get(cls, f"Unknown ({cls})")
        pct = 100.0 * vote_counts.get(cls, 0) / len(sim_votes)
        print(f"  {party}: {pct:.1f}%")
        
if __name__ == "__main__":
    main()
