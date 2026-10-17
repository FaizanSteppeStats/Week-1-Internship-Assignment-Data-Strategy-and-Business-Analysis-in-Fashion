"""Unit tests: run python -m unittest discover -s tests -v."""
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from fashion_strategy_demo import (wape, customer_rfm, evaluate_forecasts,
                                  generate_synthetic_data, reorder_suggestions)


class Tests(unittest.TestCase):
    def test_wape(self):
        self.assertAlmostEqual(wape([10, 20], [10, 15]), 100 * 5 / 30)
        self.assertTrue(np.isnan(wape([0, 0], [0, 0])))
        with self.assertRaises(ValueError):
            wape([-2], [1])

    def test_end_to_end(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            generate_synthetic_data(folder)
            sales = pd.read_csv(folder / 'synthetic_weekly_sales.csv')
            orders = pd.read_csv(folder / 'synthetic_orders.csv')
            preds, scores = evaluate_forecasts(sales)
            self.assertTrue((scores['wape_pct'] >= 0).all())
            self.assertEqual(len(scores), 2)
            self.assertGreater(len(preds), 0)
            inventory = reorder_suggestions(sales)
            self.assertTrue((inventory['illustrative_replenishment_units'] >= 0).all())
            rfm, summary = customer_rfm(orders)
            self.assertEqual(rfm['customer_id'].nunique(), 520)
            self.assertEqual(int(summary['customers'].sum()), 520)


if __name__ == '__main__':
    unittest.main()
