#!/usr/bin/env python3
"""Data cleaning script for the Hotel Booking dataset.

Author: Nwaeke Calixtus, Esq

Usage:
    python scripts/clean_data.py --input ../hotels.csv --output ../data/cleaned_hotels.csv
"""
import argparse
import os
import sys
from typing import Tuple

import pandas as pd


def summarize(df: pd.DataFrame) -> None:
    print(f"Rows: {len(df)}")
    nulls = df.isna().sum()
    print("Top nulls:")
    print(nulls[nulls > 0].sort_values(ascending=False).head(10))


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.replace("NULL", pd.NA)

    # Parse dates
    if "reservation_status_date" in df.columns:
        df["reservation_status_date"] = pd.to_datetime(
            df["reservation_status_date"], errors="coerce"
        )

    # Numeric conversions (best-effort)
    numeric_cols = [
        "lead_time",
        "arrival_date_year",
        "arrival_date_week_number",
        "arrival_date_day_of_month",
        "stays_in_weekend_nights",
        "stays_in_week_nights",
        "adults",
        "children",
        "babies",
        "previous_cancellations",
        "previous_bookings_not_canceled",
        "booking_changes",
        "days_in_waiting_list",
        "adr",
        "required_car_parking_spaces",
        "total_of_special_requests",
    ]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Replace missing guests with 0 and coerce to int where appropriate
    for c in ("adults", "children", "babies"):
        if c in df.columns:
            df[c] = df[c].fillna(0)
            try:
                df[c] = df[c].astype(int)
            except Exception:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

    # Drop rows with zero total guests (likely bad records)
    if set(("adults", "children", "babies")).issubset(df.columns):
        df["total_guests"] = df["adults"] + df["children"] + df["babies"]
        df = df[df["total_guests"] > 0].copy()
        df.drop(columns=["total_guests"], inplace=True)

    # Trim whitespace for object columns and normalize explicit strings
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace("nan", pd.NA)

    # Drop exact duplicates
    df = df.drop_duplicates()

    return df


def main(argv: Tuple[str] = None) -> int:
    p = argparse.ArgumentParser(description="Clean hotel booking CSV into reproducible CSV")
    p.add_argument("--input", "-i", required=True, help="Input CSV path")
    p.add_argument("--output", "-o", required=True, help="Output cleaned CSV path")
    args = p.parse_args(argv)

    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}")
        return 2

    df = pd.read_csv(args.input, low_memory=False)
    print("Input summary:")
    summarize(df)

    cleaned = clean(df)
    print("After cleaning summary:")
    summarize(cleaned)

    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    cleaned.to_csv(args.output, index=False)
    print(f"Wrote cleaned CSV to: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
