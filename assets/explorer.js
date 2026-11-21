(() => {
'use strict';
const $=id=>document.getElementById(id);
  // Local CSV explorer: deliberately limited, clearly separated from the final validated report.
  const input=$('csv-file'), clear=$('clear-preview'), machine=$('machine-select'), metric=$('metric-select'), canvas=$('preview-canvas');
  if(!input || !clear || !machine || !metric || !canvas)return;
  let rows=[];
  const number=s=>{if(s===undefined || s===null || String(s).trim()==='')return NaN;return Number(String(s).trim());};
  const draw=()=>{
    if(!rows.length)return;
    const choice=machine.value, field=metric.value;
    const subset=choice==='all'?rows:rows.filter(r=>r.m===choice);
    const bounds=subset.map(r=>r.t).filter(Number.isFinite);
    if(!bounds.length){$('preview-status').textContent='No records for this machine.';return;}
    let min=Infinity,max=-Infinity;for(const v of bounds){if(v<min)min=v;if(v>max)max=v;}
    const interval=Math.max(1,Math.ceil((max-min)/90));
    const buckets=new Map();
    subset.forEach(r=>{const k=Math.floor((r.t-min)/interval);const old=buckets.get(k)||{sum:0,n:0};old.sum+=r[field];old.n++;buckets.set(k,old);});
    const series=[...buckets.entries()].sort((a,b)=>a[0]-b[0]).map(([key,v])=>({x:min+key*interval,y:v.sum/v.n}));
    canvas.style.display='block';
    const size=canvas.getBoundingClientRect();if(size.width<20)return;
    const dpr=Math.min(window.devicePixelRatio||1,2), w=Math.floor(size.width),h=Math.floor(size.height);
    canvas.width=w*dpr;canvas.height=h*dpr;
    const ctx=canvas.getContext('2d');ctx.scale(dpr,dpr);ctx.clearRect(0,0,w,h);
    const l=48,r=17,t=17,b=36,pw=w-l-r,ph=h-t-b;
    ctx.font='11px Arial, sans-serif';ctx.textBaseline='middle';ctx.lineWidth=1;
    for(let j=0;j<=4;j++){const y=t+ph*(1-j/4);ctx.strokeStyle='#e1ecf9';ctx.beginPath();ctx.moveTo(l,y);ctx.lineTo(w-r,y);ctx.stroke();ctx.fillStyle='#8199ae';ctx.textAlign='right';ctx.fillText(String(j*25),l-9,y);}
    ctx.fillStyle='#8ca5bd';ctx.textAlign='center';ctx.fillText('Trace time (seconds)',l+pw/2,h-9);
    ctx.save();ctx.translate(13,t+ph/2);ctx.rotate(-Math.PI/2);ctx.fillText('Utilization (%)',0,0);ctx.restore();
    ctx.strokeStyle=field==='cpu'?'#69a4da':'#87b1cf';ctx.lineWidth=2.6;ctx.beginPath();
    series.forEach((pt,i)=>{const x=l+(series.length<=1?.5:i/(series.length-1))*pw;const y=t+ph*(1-Math.min(100,Math.max(0,pt.y))/100);i?ctx.lineTo(x,y):ctx.moveTo(x,y);});ctx.stroke();
    canvas.style.display='block';$('chart-empty').style.display='none';
    $('preview-status').textContent=`Local preview only: ${subset.length.toLocaleString()} valid rows across ${series.length} time bins. Time ${min}–${max} seconds. Figures from this browser are not formal report findings.`;
  };
  const reset=()=>{rows=[];input.value='';machine.innerHTML='<option value="all">All sample machines</option>';$('preview-metrics').innerHTML='<span>No sample loaded</span>';canvas.style.display='none';$('chart-empty').style.display='grid';$('preview-status').textContent='Preview cleared. Choose a small 2017 server_usage.csv sample to explore real measurements.';};
  clear.addEventListener('click',reset);
  input.addEventListener('change',async ()=>{
    const file=input.files?.[0];if(!file)return;
    if(file.size>6*1024*1024){$('preview-status').textContent='File exceeds 6 MB. Ask Team A to provide a small, documented sample.';input.value='';return;}
    try{
      const text=await file.text();const lines=text.split(/\r?\n/).filter(s=>s.trim());
      if(!lines.length)throw Error('CSV has no records.');
      const first=lines[0].split(',').map(s=>s.trim().toLowerCase());
      const header=!Number.isFinite(number(first[0]));
      const ix=header?{
        t:first.findIndex(s=>['timestamp','time_stamp','time'].includes(s)),
        m:first.findIndex(s=>['machineid','machine_id','machine id'].includes(s)),
        cpu:first.findIndex(s=>['util:cpu','cpu','cpu_util_percent','cpu_util'].includes(s)),
        memory:first.findIndex(s=>['util:memory','memory','mem_util_percent','mem_util','mem'].includes(s))
      }:{t:0,m:1,cpu:2,memory:3};
      if(Object.values(ix).some(v=>v<0))throw Error('The CSV header does not contain recognized timestamp, machine, CPU and memory fields.');
      let invalid=0;rows=[];
      const subset=lines.slice(header?1:0,(header?1:0)+30000);
      subset.forEach(line=>{const a=line.split(',');const r={t:number(a[ix.t]),m:String(a[ix.m]??'').trim(),cpu:number(a[ix.cpu]),memory:number(a[ix.memory])};
        if(!Number.isFinite(r.t)||!r.m||!Number.isFinite(r.cpu)||!Number.isFinite(r.memory)||r.cpu<0||r.cpu>100||r.memory<0||r.memory>100){invalid++;return;}rows.push(r);});
      if(!rows.length)throw Error('No valid CPU/memory records were detected. Verify that your CSV follows the 2017 schema.');
      const ids=[...new Set(rows.map(r=>r.m))].sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}));
      const mean=k=>(rows.reduce((sum,r)=>sum+r[k],0)/rows.length).toFixed(1);
      $('preview-metrics').innerHTML='';
      const fields=[`${rows.length.toLocaleString()} valid rows`,`${ids.length.toLocaleString()} machines`,`CPU avg ${mean('cpu')}%`,`Memory avg ${mean('memory')}%`,`${invalid.toLocaleString()} invalid rows skipped`];
      fields.forEach(val=>{const el=document.createElement('span');el.textContent=val;$('preview-metrics').append(el);});
      machine.innerHTML='<option value="all">All sample machines</option>';
      ids.slice(0,3000).forEach(id=>{const option=document.createElement('option');option.value=id;option.textContent=`Machine ${id}`;machine.add(option);});
      draw();
    }catch(err){reset();$('preview-status').textContent=`Could not read CSV: ${err.message}`;}
  });
  machine.addEventListener('change',draw);metric.addEventListener('change',draw);
  let resizeRequest=null;window.addEventListener('resize',()=>{if(resizeRequest)cancelAnimationFrame(resizeRequest);resizeRequest=requestAnimationFrame(()=>{if(rows.length)draw();});});

})();
