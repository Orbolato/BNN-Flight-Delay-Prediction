"""Lightweight integrity checks for the public reproducibility package."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "final_data_sbrf_sbgr.csv"
CITATION = ROOT / "CITATION.cff"
EXPECTED_SHA256 = "02990049e1307b352b369c0074719ce89d21fbc6aa6156bcd0dd32059819a0eb"
EXPECTED_ROWS = 14956
EXPECTED_COLUMNS = 28
CANONICAL_REPOSITORY = "https://github.com/Orbolato/BNN-Flight-Delay-Prediction"


class IntegrityTests(unittest.TestCase):
    def test_exact_route_dataset_checksum(self) -> None:
        digest = hashlib.sha256(DATASET.read_bytes()).hexdigest()
        self.assertEqual(digest, EXPECTED_SHA256)

    def test_exact_route_dataset_shape(self) -> None:
        with DATASET.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader)
            row_count = sum(1 for _ in reader)
        self.assertEqual(len(header), EXPECTED_COLUMNS)
        self.assertEqual(row_count, EXPECTED_ROWS)

    def test_citation_uses_canonical_repository_url(self) -> None:
        text = CITATION.read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count(CANONICAL_REPOSITORY), 2)
        self.assertNotIn("BNN-Flight-Delay-Reproducibility", text)
        self.assertIn("10.1109/ACCESS.2026.3709713", text)


if __name__ == "__main__":
    unittest.main()
