import unittest
from pathlib import Path
import sys,pandas as pd,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from forecast import train_predict,wape,run
class TestForecast(unittest.TestCase):
 def setUp(self):
  self.y=pd.read_csv(ROOT/'data/fred_clothing_store_sales_2019_2026_08.csv',parse_dates=['date']).set_index('date').clothing_stores_usd_million
 def test_leakage_rejected(self):
  with self.assertRaises(AssertionError):train_predict(self.y.loc[:'2024-12-01'],[pd.Timestamp('2024-12-01')],'seasonal_naive')
 def test_seasonal_naive_uses_last_year(self):
  p=train_predict(self.y.loc[:'2025-12-01'],[pd.Timestamp('2026-01-01')],'seasonal_naive');self.assertEqual(p.iloc[0],13533)
 def test_holdout_not_in_selection(self):
  x=run(ROOT);self.assertIn(x['chosen_model'],['seasonal_naive','seasonal_trend','ridge_fourier']);self.assertTrue((ROOT/'outputs/untouched_2026_holdout.csv').exists())
 def test_wape(self):self.assertAlmostEqual(wape([100,100],[90,120]),15)
if __name__=='__main__':unittest.main()
