"""Minimal loader and sanity check for the scholarly contribution error-detection release.

Usage:
    pip install pandas pyarrow
    python load.py
"""
import pathlib
import pandas as pd

DATA = pathlib.Path(__file__).parent / "data"


def load():
    graph = pd.read_parquet(DATA / "contribution_graph.parquet")
    validation = pd.read_csv(DATA / "human_validation.csv")
    second = pd.read_csv(DATA / "second_annotator_overlap.csv")
    return graph, validation, second


def main():
    graph, validation, second = load()
    in_gold = graph["in_gold"].astype(str).str.lower().eq("true").sum()
    print(f"contribution graph : {len(graph):,} facts, {in_gold:,} in-gold (with leaderboard labels)")
    hl = validation["human_label"].str.strip().str.lower()
    print(f"human validation   : {len(validation)} facts, {(hl == 'genuinely-wrong').sum()} genuine errors")
    print(f"second-annotator   : {len(second)} overlap facts (for inter-annotator agreement)")

    print("\nHighest-error-score facts (candidates a curator would review first):")
    top = graph.sort_values("error_score", ascending=False).head(5)
    print(top[["method", "dataset", "metric", "value", "error_score", "violated_constraints"]].to_string(index=False))


if __name__ == "__main__":
    main()
