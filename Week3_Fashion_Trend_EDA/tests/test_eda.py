import unittest
from pathlib import Path
import sys,pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from eda import run
class TestEDA(unittest.TestCase):
 def test_time_series_has_no_gaps(self):
  d=pd.read_csv(ROOT/'data/fred_clothing_store_sales_2019_2026_08.csv',parse_dates=['date']);self.assertEqual(len(d),92);self.assertTrue(d.date.dt.to_period('M').diff().dropna().apply(lambda x:x.n==1).all())
 def test_reproduces_source_values(self):
  d=pd.read_csv(ROOT/'data/fred_clothing_store_sales_2019_2026_08.csv').set_index('date');self.assertEqual(d.loc['2020-04-01','clothing_stores_usd_million'],1642);self.assertEqual(d.loc['2025-12-01','clothing_stores_usd_million'],27542)
 def test_insights_and_charts(self):
  s=run(ROOT);self.assertEqual(s['missing_clothing'],0);self.assertGreater(s['dec_to_feb_multiple'],1.2);self.assertTrue((ROOT/'assets/01_sales_trend.png').exists())
if __name__=='__main__':unittest.main()
