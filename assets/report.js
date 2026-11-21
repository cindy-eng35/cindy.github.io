(() => {
'use strict';
const report=window.PROJECT_RESULTS;
if(!report||report.status!=='generated_from_real_data')return;
const $=id=>document.getElementById(id);
const put=(id,value)=>{const e=$(id);if(e&&value!==null&&value!==undefined)e.textContent=String(value);};
const stats=report.statistics||{};
const fmt=x=>Number.isFinite(Number(x))?Number(x).toLocaleString('en-US'):'—';
put('stat-machines',fmt(stats.machines));put('stat-records',fmt(stats.valid_records));
put('stat-cpu',Number.isFinite(stats.mean_cpu)?stats.mean_cpu.toFixed(1):'—');
put('stat-memory',Number.isFinite(stats.mean_memory)?stats.mean_memory.toFixed(1):'—');
put('selection-summary',`Input: ${report.input_filename||'documented file'}; scanned ${fmt(report.records_scanned)} rows; ${fmt(report.records_selected)} selected before validation. ${report.selection_description||''} Observed trace timestamps: ${stats.time_start??'—'}–${stats.time_end??'—'} seconds.`);
put('quality-summary',`Invalid selected records: ${fmt(report.invalid_selected_records)}. ${report.quality_note||''}`);
if(Number.isFinite(stats.cpu_memory_correlation))put('discussion-findings',`Selected sample: mean CPU ${stats.mean_cpu.toFixed(1)}%, memory ${stats.mean_memory.toFixed(1)}%, Pearson correlation ${stats.cpu_memory_correlation.toFixed(3)}. Review actual figures and add the study's OS interpretation. Correlation does not imply causation or application performance.`);
put('progress-label','Figures generated · review interpretation');
const figureIDs=['fig01_cpu_histogram','fig02_cpu_time_series','fig03_machine_comparison','fig04_memory_histogram','fig05_cpu_memory_scatter','fig06_imbalance_heatmap','fig07_utilization_categories'];
let ready=0;
document.querySelectorAll('[data-figure]').forEach(card=>{
 const key=card.dataset.figure,img=card.querySelector('img.figure-img'),meta=report.figures?.[key];
 if(!img||!meta)return;
 img.addEventListener('load',()=>{if(!card.classList.contains('ready')){card.classList.add('ready');ready++;put('figure-count',`${ready} / ${figureIDs.length} figures ready`);}if(meta.caption){const c=card.querySelector('.figure-caption');if(c)c.textContent=meta.caption;}});
 img.addEventListener('error',()=>card.classList.remove('ready'));
 img.src=`assets/results/${key}.png?v=${encodeURIComponent(report.generated_at||'1')}`;
});
})();