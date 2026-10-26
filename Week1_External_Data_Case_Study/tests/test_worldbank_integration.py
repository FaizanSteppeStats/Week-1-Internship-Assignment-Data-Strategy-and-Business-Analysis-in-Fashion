import sys
import unittest
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from worldbank_market_integration import integrate, make_outputs

class ExternalCaseStudyTests(unittest.TestCase):
    def setUp(self):
        self.raw=pd.read_csv(ROOT/'data/external/worldbank_india_2020_2025.csv')

    def test_join_has_six_unique_years(self):
        result=integrate(self.raw)
        self.assertEqual(len(result),6)
        self.assertEqual(result.year.nunique(),6)
        self.assertEqual(len(result.columns),4)

    def test_value_ranges_and_sourcing(self):
        result=integrate(self.raw)
        for col in ['internet_users_pct','urban_population_pct']:
            self.assertTrue(result[col].between(0,100).all())
        self.assertEqual(set(self.raw.indicator_code),{'IT.NET.USER.ZS','SP.URB.TOTL.IN.ZS'})

    def test_fail_on_duplicate(self):
        with self.assertRaises(ValueError):
            integrate(pd.concat([self.raw,self.raw.iloc[[0]]],ignore_index=True))

    def test_fail_on_missing(self):
        bad=self.raw.copy();bad.loc[0,'value_pct']=None
        with self.assertRaises(ValueError):integrate(bad)

    def test_observed_separated_from_assumptions(self):
        obs,scenario=make_outputs(ROOT)
        self.assertEqual(obs['years_joined'],6)
        self.assertEqual(scenario['type'],'ILLUSTRATIVE ASSUMPTIONS - NOT MEASURED')
        self.assertEqual(scenario['roas'],3.0)

if __name__=='__main__':unittest.main()
