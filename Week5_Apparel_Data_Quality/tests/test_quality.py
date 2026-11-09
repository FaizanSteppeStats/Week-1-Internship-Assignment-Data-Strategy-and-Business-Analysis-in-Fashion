import tempfile
import unittest
from pathlib import Path
import pandas as pd
from src.quality_assessment import inspect_fred, run_quality
from src.retail_cleaner import parse_discount, parse_amount, process_csv
ROOT=Path(__file__).resolve().parents[1]

class QualityTests(unittest.TestCase):
    def test_all_rows_reconcile(self):
        result=run_quality(ROOT)['synthetic_case'];self.assertEqual(result['raw_rows'],result['accepted_sales']+result['accepted_returns']+result['quarantined_rows'])
    def test_retail_pipeline_reproduces_known_fixture(self):
        with tempfile.TemporaryDirectory() as d:
            a=process_csv(ROOT/'data/raw/synthetic_fashion_orders.csv',Path(d))
            self.assertEqual((a['raw_rows'],a['clean_sales_rows'],a['clean_returns_rows'],a['quarantined_rows']),(163,147,2,14))
    def test_discount_normalization(self):
        for s in ['10%','10',0.10]:self.assertAlmostEqual(parse_discount(s),0.1)
    def test_invalid_discount_preserved(self):
        self.assertGreater(parse_discount('120%'),1)
    def test_currency_normalization(self):
        self.assertEqual(parse_amount('INR 1,299'),1299)
    def test_real_months_complete(self):
        a,_=inspect_fred(ROOT/'data/external/fred_clothing_store_sales_2019_2026_08.csv');self.assertTrue(a['passed_structural_gates']);self.assertEqual(a['monthly_rows'],92)
    def test_real_yoy_event_is_flag_not_removal(self):
        a,df=inspect_fred(ROOT/'data/external/fred_clothing_store_sales_2019_2026_08.csv');self.assertEqual(len(df),92);self.assertTrue(df.loc[df.date.eq(pd.Timestamp('2020-04-01')),'review_outlier_yoy'].all())
    def test_detect_missing_month(self):
        with tempfile.TemporaryDirectory() as d:
            df=pd.read_csv(ROOT/'data/external/fred_clothing_store_sales_2019_2026_08.csv');df=df[df.date!='2021-05-01'];p=Path(d)/'case.csv';df.to_csv(p,index=False)
            m,_=inspect_fred(p);self.assertEqual(m['missing_target_months'],1);self.assertFalse(m['passed_structural_gates'])
    def test_detect_duplicate_month(self):
        with tempfile.TemporaryDirectory() as d:
            df=pd.read_csv(ROOT/'data/external/fred_clothing_store_sales_2019_2026_08.csv');df=pd.concat([df,df.iloc[[0]]]);p=Path(d)/'case.csv';df.to_csv(p,index=False)
            m,_=inspect_fred(p);self.assertEqual(m['duplicate_months'],1)
    def test_blank_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            df=pd.read_csv(ROOT/'data/external/fred_clothing_store_sales_2019_2026_08.csv');df.loc[0,'clothing_stores_usd_million']=None;p=Path(d)/'case.csv';df.to_csv(p,index=False)
            m,_=inspect_fred(p);self.assertEqual(m['invalid_target_values'],1)

if __name__=='__main__':unittest.main()
