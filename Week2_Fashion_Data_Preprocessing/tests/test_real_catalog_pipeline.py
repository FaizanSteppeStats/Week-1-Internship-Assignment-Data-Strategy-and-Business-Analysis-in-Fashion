import json, tempfile, unittest
from pathlib import Path
from src.real_catalog_pipeline import run_case, strip_markup, fetch_pinned_snapshot

class RealCatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.source=Path(self.tmp.name)/'source';self.source.mkdir()
        self.output=Path(self.tmp.name)/'output'
        self.rows=[
            dict(id='A1',handle='dresses',title='Dresses',products_count=6, updated_at='2026-10-18T00:00:00Z',image_url=None,
                 description_html='<p>Soft &amp; washable cotton.</p>',seo={'description':''}),
            dict(id='A2',handle='tops',title='Tops',products_count=3, updated_at='2026-10-17T00:00:00Z', image_url='https://example.org/1.png',
                 description_html='<div>Tops for summer.</div>',seo={'description':'Well-cut tops'}),
            dict(id='A2',handle='tops',title='Duplicate',products_count=3, updated_at='2026-10-17T00:00:00Z',image_url=None,description_html='',seo={}),
            dict(id='A3',handle='bad',title='Bad Count',products_count=-2, updated_at='2026-10-17T00:00:00Z',image_url=None,description_html='',seo={}),
        ]
        self.stats={'total_collections':4,'total_products':5,'products_with_reviews':3,'last_synced':'2026-10-18T06:02:35Z',
        'products_by_category':{'Apparel & Accessories > Clothing > Dresses':3,'Apparel & Accessories > Clothing > Clothing Tops':2}}
        (self.source/'livostyle_collections.json').write_text(json.dumps(self.rows))
        (self.source/'livostyle_stats.json').write_text(json.dumps(self.stats))
    def tearDown(self):self.tmp.cleanup()
    def test_html_and_entity_cleanup(self):self.assertEqual(strip_markup('<p>Soft &amp; washable</p>'),'Soft & washable')
    def test_duplicate_quarantine(self):self.assertEqual(run_case(self.source,self.output)['duplicate_collection_ids'],1)
    def test_negative_count_quarantine(self):self.assertEqual(run_case(self.source,self.output)['invalid_count_or_timestamp'],1)
    def test_missing_optional_image_is_kept(self):self.assertEqual(run_case(self.source,self.output)['missing_collection_images'],3)
    def test_fallback_transparent(self):self.assertEqual(run_case(self.source,self.output)['seo_descriptions_derived_from_html'],1)
    def test_count_flags_not_deleted(self):self.assertEqual(run_case(self.source,self.output)['collections_count_exceeding_unique_skus'],1)
    def test_counts_reconcile(self):
        a=run_case(self.source,self.output);self.assertEqual(a['valid_collection_rows']+a['quarantined_rows'],4)
    def test_category_stats_unique(self):self.assertEqual(run_case(self.source,self.output)['product_category_totals_sum'],5)
    def test_output_has_source_provenance(self):self.assertIn('source_commit',run_case(self.source,self.output))
    def test_bad_category_total_fails(self):
        self.stats['total_products']=6
        (self.source/'livostyle_stats.json').write_text(json.dumps(self.stats))
        with self.assertRaises(ValueError):run_case(self.source,self.output)

if __name__=='__main__':unittest.main()
