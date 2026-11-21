#!/usr/bin/env python3
"""Reproducible, evidence-only analysis of Alibaba 2017 server_usage.csv.

Input: 2017 headerless CSV columns in official order:
  timestamp,machineID,util:CPU,util:memory,util:disk,load1,load5,load15

The script never fabricates measurements or silently substitutes demo data.
Selected records are a reproducible random sample (independent Bernoulli
selection with probability 1/N); selection settings and quality counters
are documented in exported metadata.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COLS = ['timestamp', 'machineID', 'cpu', 'memory', 'disk', 'load1', 'load5', 'load15']
BLUE, LIGHT, DARK, GREY = '#649cd3', '#add3f4', '#335c87', '#71849a'


def save_figure(fig, path: Path) -> None:
    fig.tight_layout(pad=1.8)
    fig.savefig(path, dpi=170, facecolor='white', bbox_inches='tight')
    plt.close(fig)


def clean_ax(ax):
    ax.grid(axis='y', color='#e5eff8', linewidth=.8)
    ax.set_axisbelow(True)
    for k in ('top', 'right'):
        ax.spines[k].set_visible(False)
    ax.spines['left'].set_color('#dbe8f4')
    ax.spines['bottom'].set_color('#dbe8f4')
    ax.tick_params(colors=GREY, labelsize=9)


def classify(series: pd.Series, low: float, high: float) -> pd.Series:
    return pd.cut(series, bins=[-1e-6, low, high, 100 + 1e-6],
                  labels=['Low', 'Medium', 'High'], include_lowest=True, right=True)


def analyze(args) -> None:
    if not args.input.is_file():
        raise FileNotFoundError(f'Input CSV not found: {args.input}')
    if args.every < 1 or not 0 < args.low < args.high < 100:
        raise ValueError('Require --every >= 1 and 0 < --low < --high < 100')
    args.output.mkdir(parents=True, exist_ok=True)
    chunks = []
    scanned, selected, invalid = 0, 0, 0
    load_non_null = 0
    rng_sample = np.random.default_rng(args.seed)
    reader = pd.read_csv(args.input, names=COLS, header=None, dtype='string',
                         chunksize=100_000, keep_default_na=True)
    for frame in reader:
        selected_mask = rng_sample.random(len(frame)) < (1.0 / args.every)
        chosen = frame.loc[selected_mask, ['timestamp', 'machineID', 'cpu', 'memory', 'load1']].copy()
        scanned += len(frame)
        selected += len(chosen)
        if selected > args.max_selected:
            raise ValueError(f'Selected rows exceeded --max-selected={args.max_selected:,}. '
                             f'Increase --every (current {args.every}) to keep a time-spanning sample.')
        for col in ['timestamp','cpu','memory','load1']:
            chosen[col] = pd.to_numeric(chosen[col], errors='coerce')
        valid = (chosen.timestamp.notna() & (chosen.timestamp >= 0) &
                 chosen.machineID.notna() & chosen.machineID.str.strip().ne('') &
                 chosen.cpu.between(0, 100) & chosen.memory.between(0, 100))
        invalid += int((~valid).sum())
        load_non_null += int(chosen['load1'].notna().sum())
        if valid.any():
            chunks.append(chosen.loc[valid])
    if not chunks:
        raise ValueError('No valid records found in selected rows. Verify the v2017 headerless schema.')
    df = pd.concat(chunks, ignore_index=True)
    df['machineID'] = df['machineID'].astype(str)
    df['timestamp'] = df['timestamp'].astype('int64')
    duplicates = int(df.duplicated(subset=['timestamp','machineID']).sum())
    df = df.drop_duplicates(subset=['timestamp','machineID'], keep='first').copy()
    if not len(df):
        raise ValueError('All sampled measurements were duplicates.')

    tmin, tmax = int(df.timestamp.min()), int(df.timestamp.max())
    df['hours'] = (df.timestamp - tmin) / 3600
    df['time_bin'] = ((df.timestamp - tmin)//300).astype('int64')
    group = df.groupby('machineID').agg(mean_cpu=('cpu','mean'),
              sd_cpu=('cpu','std'), mean_memory=('memory','mean'), records=('cpu','size'))
    group.sort_values('mean_cpu', ascending=False).to_csv(args.output / 'machine_summary.csv',
          float_format='%.5f', index_label='machineID')
    series = df.groupby('time_bin').agg(mean_cpu=('cpu','mean'), mean_memory=('memory','mean'),
                                      n=('cpu','size')).reset_index()
    times = (series['time_bin']*300)/3600

    figures = {}
    def register(key, caption):
        figures[key] = {'caption': caption}

    fig,ax=plt.subplots(figsize=(8,3.65))
    ax.hist(df.cpu, bins=np.arange(0,105,5), color=BLUE, edgecolor='white',linewidth=.65)
    ax.set(xlabel='CPU utilization (%)',ylabel='Sampled observations',title='CPU utilization distribution')
    clean_ax(ax);save_figure(fig,args.output/'fig01_cpu_histogram.png')
    register('fig01_cpu_histogram', f'Histogram of {len(df):,} valid sampled CPU observations; 5-percentage-point bins. Distribution is descriptive, not evidence of latency.')

    fig,ax=plt.subplots(figsize=(8,3.65))
    ax.plot(times,series.mean_cpu,color=BLUE,lw=2.0)
    ax.set(xlabel='Hours since first valid sampled observation',ylabel='Mean CPU utilization (%)',
           title='CPU utilization across the trace period',ylim=(0,100))
    clean_ax(ax);save_figure(fig,args.output/'fig02_cpu_time_series.png')
    register('fig02_cpu_time_series', 'Mean sampled CPU utilization per 5-minute trace-time bin; different numbers of records may contribute to each interval.')

    eligible=group[group.records >= args.min_machine_records]
    if eligible.empty:eligible=group.copy()
    lows=eligible.nsmallest(min(6,len(eligible)),'mean_cpu')
    highs=eligible.nlargest(min(6,len(eligible)),'mean_cpu')
    ranked=pd.concat([lows,highs]).loc[lambda x:~x.index.duplicated(keep='first')]
    fig,ax=plt.subplots(figsize=(8,4))
    labels=[f'Machine {m}' for m in ranked.index]
    positions=np.arange(len(ranked))
    bars=ax.barh(positions,ranked.mean_cpu.values,color=[LIGHT]*len(lows)+[BLUE]*max(0,len(ranked)-len(lows)))
    ax.set_yticks(positions,labels=labels)
    ax.invert_yaxis();ax.set(xlabel='Mean CPU utilization (%)',title='Selected low- and high-CPU machines',xlim=(0,100))
    clean_ax(ax);ax.grid(axis='x',color='#e5eff8');ax.grid(axis='y',visible=False)
    save_figure(fig,args.output/'fig03_machine_comparison.png')
    register('fig03_machine_comparison', f'Machines with lowest and highest mean sampled CPU utilization (minimum {args.min_machine_records} observations where available); not a randomized selection.')

    fig,ax=plt.subplots(figsize=(8,3.65))
    ax.hist(df.memory,bins=np.arange(0,105,5),color='#91bce1',edgecolor='white',linewidth=.65)
    ax.set(xlabel='Memory utilization (%)',ylabel='Sampled observations',title='Memory utilization distribution')
    clean_ax(ax);save_figure(fig,args.output/'fig04_memory_histogram.png')
    register('fig04_memory_histogram', f'Histogram of {len(df):,} valid sampled memory observations; 5-percentage-point bins.')

    rng=np.random.default_rng(args.seed)
    selected_idx=rng.choice(len(df),size=min(5000,len(df)),replace=False)
    small=df.iloc[selected_idx]
    corr=float(df[['cpu','memory']].corr().iloc[0,1]) if df.cpu.nunique()>1 and df.memory.nunique()>1 else None
    fig,ax=plt.subplots(figsize=(8,3.65))
    ax.scatter(small.cpu,small.memory,c=BLUE,alpha=.18,s=13,edgecolors='none')
    ax.set(xlabel='CPU utilization (%)',ylabel='Memory utilization (%)',
           title='CPU vs. memory usage (paired samples)',xlim=(0,100),ylim=(0,100))
    clean_ax(ax);save_figure(fig,args.output/'fig05_cpu_memory_scatter.png')
    corr_text = f'; Pearson r = {corr:.3f}' if corr is not None else '; Pearson correlation undefined (constant variable)'
    register('fig05_cpu_memory_scatter', f'Scatter of up to 5,000 randomly selected paired observations (seed {args.seed}) from the valid sample{corr_text}. Correlation does not demonstrate causation.')

    select_ids=group.sort_values(['records','sd_cpu'],ascending=False).head(14).index
    pivot=df[df.machineID.isin(select_ids)].pivot_table(index='machineID',columns='time_bin',values='cpu',aggfunc='mean')
    fig,ax=plt.subplots(figsize=(8,4.1))
    image=ax.imshow(pivot.to_numpy(dtype=float),aspect='auto',interpolation='nearest',origin='upper',vmin=0,vmax=100,cmap='Blues')
    ax.set_yticks(np.arange(len(pivot.index)), labels=[str(s) for s in pivot.index])
    ncols=len(pivot.columns);ticks=np.unique(np.linspace(0,max(0,ncols-1),min(7,ncols),dtype=int))
    ax.set_xticks(ticks,labels=[f'{pivot.columns[t]*300/3600:.1f}' for t in ticks]);ax.set(xlabel='Hours since first sampled observation',ylabel='Machine ID',title='CPU utilization heatmap: selected machines')
    fig.colorbar(image,ax=ax,fraction=.027,pad=.02,label='CPU utilization (%)')
    save_figure(fig,args.output/'fig06_imbalance_heatmap.png')
    register('fig06_imbalance_heatmap', 'Machine-time heatmap of CPU utilization (%), showing up to 14 machines selected by record count and variability. Gaps indicate missing sampled intervals; color alone cannot establish application performance.')

    cpu_cat=classify(df.cpu,args.low,args.high)
    mem_cat=classify(df.memory,args.low,args.high)
    order=['Low','Medium','High']
    counts=pd.DataFrame({'CPU':cpu_cat.value_counts(normalize=True).reindex(order,fill_value=0)*100,
                          'Memory':mem_cat.value_counts(normalize=True).reindex(order,fill_value=0)*100})
    fig,ax=plt.subplots(figsize=(8,3.65))
    bottom=np.zeros(2)
    for idx,(label,color) in enumerate(zip(order,['#c3e2f9','#83b9e6','#477eaf'])):
        values=counts.loc[label,['CPU','Memory']].to_numpy(dtype=float)
        ax.bar(['CPU','Memory'],values,bottom=bottom,label=label,color=color,width=.48)
        bottom+=values
    ax.set(xlabel='Resource type',ylabel='Share of sampled observations (%)',title='Low / medium / high utilization',ylim=(0,100))
    ax.legend(ncol=3,loc='upper center',bbox_to_anchor=(.5,-.15),frameon=False)
    clean_ax(ax);save_figure(fig,args.output/'fig07_utilization_categories.png')
    register('fig07_utilization_categories', f'Sampled observation shares by utilization category. Low ≤{args.low:g}%, medium >{args.low:g}–≤{args.high:g}%, high >{args.high:g}%; thresholds are project-defined, not official standards.')

    sorted_df=df.sort_values(['machineID','timestamp'])[['machineID','timestamp','cpu','memory']].copy()
    trans=[]
    for key in ('cpu','memory'):
        sorted_df[key+'_category'] = classify(sorted_df[key],args.low,args.high).astype(str)
        previous = sorted_df.groupby('machineID')[key+'_category'].shift(1)
        found=previous.notna()
        changes=found & sorted_df[key+'_category'].ne(previous)
        trans.append({'resource':key,'adjacent_pairs':int(found.sum()),'category_transitions':int(changes.sum()),
                      'transition_share_percent':round(100*changes.sum()/found.sum(),2) if found.sum()>0 else None})
    pd.DataFrame(trans).to_csv(args.output/'category_transitions.csv',index=False)

    results={
      'status':'generated_from_real_data',
      'generated_at':datetime.now(timezone.utc).isoformat(),
      'input_filename':args.input.name,
      'records_scanned':int(scanned),'records_selected':int(selected),
      'invalid_selected_records':int(invalid),
      'duplicate_timestamp_machine_records_removed':duplicates,
      'selection_description':f'Seeded Bernoulli sampling of source rows with inclusion probability 1/{args.every}, using seed {args.seed}; scanning the complete input file. Maximum selected rows {args.max_selected:,}.',
      'quality_note':f'{duplicates:,} duplicate (timestamp,machineID) observations removed after validation. Non-missing load1 values among selected rows: {load_non_null:,}.',
      'dataset':'Alibaba Cluster Trace v2017, server_usage.csv; relative timestamps (seconds)',
      'statistics':{
        'machines':int(df.machineID.nunique()),'valid_records':int(len(df)),
        'mean_cpu':round(float(df.cpu.mean()),4),'mean_memory':round(float(df.memory.mean()),4),
        'cpu_memory_correlation':round(corr,5) if corr is not None else None,
        'time_start':tmin,'time_end':tmax,
        'low_threshold_percent':args.low,'high_threshold_percent':args.high,
      },
      'transitions':trans,
      'figures':figures,
      'disclaimer':'Sample-dependent descriptive analysis. Findings need team verification and OS interpretation.'
    }
    (args.output/'analysis_summary.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
    (args.output/'results.js').write_text('window.PROJECT_RESULTS = '+json.dumps(results,ensure_ascii=False,allow_nan=False)+';\n',encoding='utf-8')
    print(f'Processed {scanned:,} source rows; selected {selected:,}; valid {len(df):,}; machines {df.machineID.nunique():,}.')
    print(f'Created {len(figures)} figures and metadata at: {args.output.resolve()}')
    print('Review findings, figure captions and limitations before publishing.')


def main() -> None:
    parser=argparse.ArgumentParser(description='Analyze Alibaba 2017 server_usage.csv with transparent systematic sampling.')
    parser.add_argument('--input',type=Path,required=True,help='Official headerless server_usage.csv path')
    parser.add_argument('--output',type=Path,default=Path('assets/results'),help='Output folder under website project (default assets/results)')
    parser.add_argument('--every',type=int,default=5,help='Select rows with probability 1/N (default 5, i.e. 20%; raise for huge data)')
    parser.add_argument('--max-selected',type=int,default=250000,help='Stop instead of silently truncating if selected rows exceed this cap')
    parser.add_argument('--low',type=float,default=30,help='Low utilization cutoff in percent')
    parser.add_argument('--high',type=float,default=70,help='Medium utilization upper cutoff in percent')
    parser.add_argument('--seed',type=int,default=42,help='Random seed for scatter-plot subsampling')
    parser.add_argument('--min-machine-records',type=int,default=10,help='Minimum machine sample size for comparison when available')
    args=parser.parse_args()
    analyze(args)

if __name__ == '__main__':
    main()
