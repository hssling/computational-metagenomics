from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
ROOT=Path(r'D:\Computational Metagenomics\Manuscript_Package_Genomics_Transcriptomics')
FIG_DIR=ROOT/'figures'; FIG_DIR.mkdir(parents=True,exist_ok=True)
TITLES=['Genomics and transcriptomics analytical workflow', 'Illustrative variant evidence integration map', 'Illustrative RNA-seq differential expression output', 'Clinical interpretation and reporting pathway']
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'figure.dpi':240,'savefig.dpi':240,'savefig.bbox':'tight','font.family':'DejaVu Sans','axes.titlesize':14,'axes.labelsize':12})
def save(p): plt.savefig(p,facecolor='white'); plt.close()
fig,ax=plt.subplots(figsize=(13.4,6.8)); ax.set_xlim(0,16); ax.set_ylim(0,10); ax.axis('off')
for x,y,w,h,t,c in [(0.8,6.6,2.7,1.3,'Question','#355070'),(4.1,6.6,2.8,1.3,'Assay design','#6d597a'),(7.5,6.6,3.0,1.3,'Computation','#b56576'),(11.1,7.4,2.7,1.3,'Interpretation','#2a9d8f'),(11.1,5.8,2.7,1.3,'Reporting','#e76f51')]:
 p=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.04,rounding_size=0.12',edgecolor=c,facecolor=c,linewidth=1.6,alpha=0.94); ax.add_patch(p); ax.text(x+w/2,y+h/2,t,ha='center',va='center',color='white',weight='bold')
for s,e in [((3.55,7.25),(4.05,7.25)),((6.95,7.25),(7.45,7.25)),((10.55,7.25),(11.0,8.05)),((10.55,7.05),(11.0,6.45))]:
 ax.add_patch(FancyArrowPatch(s,e,arrowstyle='-|>',mutation_scale=18,linewidth=2,color='#333333'))
ax.set_title(TITLES[0],weight='bold'); save(FIG_DIR/'fig1_workflow.png')
rng=np.random.default_rng(42); data=rng.normal(size=(10,10))
fig,ax=plt.subplots(figsize=(8.2,6.2)); im=ax.imshow(data,cmap='coolwarm',aspect='auto'); fig.colorbar(im, ax=ax, shrink=0.8); ax.set_title(TITLES[1],weight='bold'); save(FIG_DIR/'fig2_matrix.png')
rng=np.random.default_rng(2026); x1=rng.normal(-0.25,0.14,36); y1=rng.normal(0.12,0.12,36); x2=rng.normal(0.24,0.14,36); y2=rng.normal(-0.08,0.12,36)
fig,ax=plt.subplots(figsize=(8.1,6.1)); ax.scatter(x1,y1,s=70,c='#2a9d8f',edgecolors='black',linewidths=0.6,label='Group A'); ax.scatter(x2,y2,s=70,c='#e76f51',edgecolors='black',linewidths=0.6,label='Group B')
ax.axhline(0,color='#888',linestyle='--',linewidth=0.9); ax.axvline(0,color='#888',linestyle='--',linewidth=0.9); ax.legend(frameon=True); ax.set_title(TITLES[2],weight='bold'); save(FIG_DIR/'fig3_projection.png')
fig,ax=plt.subplots(figsize=(8.4,6.0)); cats=['Design','QC','Modeling','Interpretation','Reporting']; vals=[4,5,4,5,4]
ax.bar(cats,vals,color=['#355070','#6d597a','#b56576','#2a9d8f','#e76f51']); ax.set_ylim(0,6); ax.set_ylabel('Relative emphasis'); ax.set_title(TITLES[3],weight='bold'); save(FIG_DIR/'fig4_strategy.png')
print('Figures generated successfully.')
