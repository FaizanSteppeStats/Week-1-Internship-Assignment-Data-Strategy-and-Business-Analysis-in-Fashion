"""Create static, labelled audit figure."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def make_chart(processed:Path,target:Path):
    a=json.loads((Path(processed)/'quality_audit.json').read_text())
    categories=['Accepted sales','Separated returns','Quarantined']
    values=[a['clean_sales_rows'],a['clean_returns_rows'],a['quarantined_rows']]
    fig,ax=plt.subplots(figsize=(8.3,3.8))
    bars=ax.barh(categories[::-1],values[::-1],color=['#B86F55','#538E91','#173D60'][::-1])
    ax.set_xlim(0,max(values)*1.15)
    for b,v in zip(bars,values[::-1]):ax.text(b.get_width()+1,b.get_y()+b.get_height()/2,str(v),va='center',fontweight='bold')
    ax.set_title('Week 2 | Row-level data-quality outcomes',loc='left',fontsize=13,fontweight='bold')
    ax.set_xlabel('Rows | synthetic teaching dataset; no real business data')
    ax.spines[['top','right']].set_visible(False)
    fig.tight_layout();target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(target,dpi=180,bbox_inches='tight');plt.close(fig)
