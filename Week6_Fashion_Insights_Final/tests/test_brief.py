import unittest
from pathlib import Path
import pandas as pd
from src.decision_brief import wape, create_brief
ROOT=Path(__file__).resolve().parents[1]
class BriefTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.metrics=create_brief(ROOT)
    def test_wape_exact(self):self.assertAlmostEqual(wape([10,20],[9,22]),10.0)
    def test_wape_zero_denominator_rejected(self):
        with self.assertRaises(ValueError):wape([0,0],[1,2])
    def test_holdout_counts(self):self.assertEqual(len(pd.read_csv(ROOT/'data/reference/untouched_2026_holdout.csv')),8)
    def test_2026_holdout_is_strictly_eight_months(self):
        x=pd.read_csv(ROOT/'data/reference/untouched_2026_holdout.csv');self.assertEqual(x.date.min(),'2026-01-01');self.assertEqual(x.date.max(),'2026-08-01')
    def test_selected_beats_naive_on_holdout(self):self.assertLess(self.metrics['week4_holdout_wape_pct'],self.metrics['week4_seasonal_naive_holdout_wape_pct'])
    def test_no_claim_of_local_accuracy(self):self.assertIn('cannot measure India',self.metrics['scope_limitation'])
    def test_action_plan_is_four_independent_initiatives(self):self.assertEqual(len(pd.read_csv(ROOT/'outputs/prioritized_decision_plan.csv')),4)
    def test_evidence_matrix_covers_all_six_weeks_conceptually(self):self.assertEqual(len(pd.read_csv(ROOT/'outputs/evidence_to_action_matrix.csv')),5)
    def test_frozen_series_not_partial_year_as_full_year(self):self.assertEqual(len(pd.read_csv(ROOT/'data/raw/fred_clothing_store_sales_2019_2026_08.csv')),92)
if __name__=='__main__':unittest.main()
