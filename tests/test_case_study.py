import unittest
from pathlib import Path
import sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from case_study_analysis import calculate_case_study

class CaseStudyTest(unittest.TestCase):
    def test_category_totals_and_holdout(self):
        s=calculate_case_study(ROOT)
        cat=pd.read_csv(ROOT/'outputs/case_category_kpis.csv')
        self.assertEqual(int(cat.units_sold.sum()),s['units_sold'])
        self.assertEqual(int(cat.stockout_sku_weeks.sum()),s['total_stockout_sku_weeks'])
        self.assertEqual(s['holdout_sku_weeks_used']+s['holdout_sku_weeks_excluded_due_to_stockout'],16*12)
        self.assertIn('SYNTHETIC',s['data_type'])
        self.assertEqual(s['sku_count'],16)

if __name__=='__main__':
    unittest.main()
