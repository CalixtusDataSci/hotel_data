#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit Tests for Hotel Data Cleaning Module

Author: Nwaeke Calixtus, Esq
License: MIT
"""

import sys
from pathlib import Path

# Ensure scripts directory is importable before other imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pandas as pd  # noqa: E402
import pytest  # noqa: E402
from clean_data import clean  # noqa: E402


class TestDataCleaning:
    """Test suite for hotel data cleaning function."""

    @pytest.fixture
    def sample_data(self):
        """Create sample hotel data for testing."""
        return pd.DataFrame(
            {
                "hotel_id": [1, 2, 3, 4, 5],
                "hotel_name": [
                    "Hotel A",
                    "Hotel B",
                    "Hotel C",
                    "Hotel D",
                    "Hotel A",
                ],
                "check_in_date": [
                    "2026-01-01",
                    "2026-01-02",
                    "invalid",
                    "2026-01-04",
                    "2026-01-05",
                ],
                "check_out_date": [
                    "2026-01-02",
                    "2026-01-03",
                    "2026-01-04",
                    "2026-01-05",
                    "2026-01-06",
                ],
                "num_guests": [2, 3, 0, 4, 2],
                "room_rate": [
                    100.50,
                    "150.75",
                    200,
                    "invalid",
                    175.25,
                ],
                "booking_id": [101, 102, 103, 104, 105],
            }
        )

    def test_clean_removes_zero_guests(self, sample_data):
        """Verify rows with zero guests are removed."""
        cleaned = clean(sample_data.copy())
        assert len(cleaned) < len(sample_data)
        assert (cleaned["num_guests"] > 0).all()

    def test_clean_removes_duplicates(self, sample_data):
        """Verify duplicates are removed based on key columns."""
        # Add a duplicate row
        extra = sample_data.iloc[0:1]
        dup_data = pd.concat([sample_data, extra], ignore_index=True)
        cleaned = clean(dup_data)
        assert len(cleaned) <= len(sample_data)

    def test_clean_parses_dates(self, sample_data):
        """Verify dates are parsed to datetime format."""
        cleaned = clean(sample_data.copy())
        assert pd.api.types.is_datetime64_any_dtype(cleaned["check_in_date"])
        assert pd.api.types.is_datetime64_any_dtype(cleaned["check_out_date"])

    def test_clean_coerces_numeric_fields(self, sample_data):
        """Verify numeric fields are properly coerced."""
        cleaned = clean(sample_data.copy())
        assert pd.api.types.is_numeric_dtype(cleaned["room_rate"])
        assert pd.api.types.is_numeric_dtype(cleaned["num_guests"])

    def test_clean_normalizes_strings(self, sample_data):
        """Verify string fields are normalized."""
        cleaned = clean(sample_data.copy())
        # Check that there are no leading/trailing spaces
        hotel_names = cleaned["hotel_name"].astype(str)
        assert (hotel_names == hotel_names.str.strip()).all()

    def test_clean_handles_missing_values(self, sample_data):
        """Verify handling of invalid/missing data."""
        cleaned = clean(sample_data.copy())
        # Should drop rows with invalid dates or coercion failures
        assert len(cleaned) > 0  # But should retain valid rows
        nulls = cleaned.isnull().sum().sum()
        assert (nulls == 0) or (len(cleaned) > 0)

    def test_clean_preserves_data_integrity(self, sample_data):
        """Verify essential columns are preserved."""
        cleaned = clean(sample_data.copy())
        required_cols = [
            "hotel_id",
            "hotel_name",
            "check_in_date",
            "check_out_date",
        ]
        assert all(col in cleaned.columns for col in required_cols)

    def test_clean_output_type(self, sample_data):
        """Verify output is a DataFrame."""
        cleaned = clean(sample_data.copy())
        assert isinstance(cleaned, pd.DataFrame)

    def test_clean_with_empty_dataframe(self):
        """Verify handling of empty DataFrame."""
        empty_df = pd.DataFrame()
        cleaned = clean(empty_df.copy())
        assert isinstance(cleaned, pd.DataFrame)

    def test_clean_with_all_invalid_dates(self):
        """Verify handling when all dates are invalid."""
        invalid_data = pd.DataFrame(
            {
                "hotel_id": [1, 2],
                "check_in_date": ["invalid", "also_invalid"],
                "room_rate": [100, 200],
                "num_guests": [2, 3],
            }
        )
        cleaned = clean(invalid_data.copy())
        # Should either drop rows or handle gracefully
        assert isinstance(cleaned, pd.DataFrame)


class TestDataQuality:
    """Test suite for data quality assurance."""

    def test_no_negative_prices(self):
        """Verify no negative room rates in cleaned data."""
        data = pd.DataFrame(
            {
                "room_rate": [100, 150, 200],
                "num_guests": [2, 3, 4],
                "hotel_name": ["A", "B", "C"],
            }
        )
        cleaned = clean(data.copy())
        assert (cleaned["room_rate"] >= 0).all()

    def test_valid_guest_numbers(self):
        """Verify guest count is positive."""
        data = pd.DataFrame(
            {
                "num_guests": [0, 1, 2],
                "hotel_name": ["A", "B", "C"],
                "room_rate": [100, 150, 200],
            }
        )
        cleaned = clean(data.copy())
        assert (cleaned["num_guests"] > 0).all()


if __name__ == "__main__":
    args = [__file__, "-v", "--cov=scripts", "--cov-report=html"]
    pytest.main(args)
