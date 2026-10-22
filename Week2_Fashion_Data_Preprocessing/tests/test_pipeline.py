import tempfile
import unittest
from pathlib import Path
import sys
import json
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.create_demo_data import make_demo
from src.preprocess import process_csv,parse_amount,parse_discount

class TestPreprocessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.root=Path(cls.tmp.name);cls.raw=cls.root/'orders.csv';cls.out=cls.root/'out'
        make_demo(cls.raw)
        cls.audit=process_csv(cls.raw,cls.out)
        cls.clean=pd.read_csv(cls.out/'clean_sales.csv')
        cls.reject=pd.read_csv(cls.out/'quarantine.csv')
        cls.ret=pd.read_csv(cls.out/'returns.csv')
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_row_reconciliation(self):
        a=self.audit;self.assertEqual(a['raw_rows'],a['clean_sales_rows']+a['clean_returns_rows']+a['quarantined_rows'])
    def test_dedup_exact(self):self.assertEqual(self.audit['exact_duplicate_rows'],2)
    def test_conflict_quarantine(self):self.assertIn('CONFLICTING_LINE_ID', '|'.join(self.reject.rejection_reason))
    def test_positive_sales(self):
        self.assertTrue((self.clean.quantity>0).all());self.assertTrue((self.clean.unit_price_inr>0).all())
    def test_return_routing(self):self.assertTrue((self.ret.quantity<0).all());self.assertFalse(self.clean.return_flag.any())
    def test_money_and_discount(self):
        self.assertEqual(parse_amount('₹1,899.00'),1899)
        self.assertAlmostEqual(parse_discount('15%'),.15)
        self.assertAlmostEqual(parse_discount('0.15'),.15)
        self.assertAlmostEqual(parse_discount('15'),.15)
    def test_dates_utc(self):self.assertTrue(self.clean.order_timestamp.str.contains('2026').all())
    def test_no_leakage(self):
        w=pd.read_csv(self.out/'weekly_features.csv')
        for _,g in w.groupby('category'):
            g=g.sort_values('year_week')
            self.assertTrue(g.lag_1_week_units.iloc[0]!=g.lag_1_week_units.iloc[0]) # nan
            if len(g)>1:self.assertEqual(g.lag_1_week_units.iloc[1],g.units_sold.iloc[0])
    def test_protect_customer_ids(self):
        customers=pd.read_csv(self.out/'customer_features.csv');self.assertFalse(customers.customer_id.astype(str).str.contains('GUEST').any())
    def test_reproducible(self):
        duplicate=self.root/'again.csv';make_demo(duplicate)
        self.assertEqual(self.raw.read_bytes(),duplicate.read_bytes())
    def test_missing_schema_raises(self):
        p=self.root/'bad.csv';p.write_text('x,y\n1,2\n')
        with self.assertRaises(ValueError): process_csv(p,self.root/'bad_out')

if __name__=='__main__':unittest.main()
