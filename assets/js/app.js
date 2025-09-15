// Main UI logic: bindings, rendering, and interactions
(function(){
  const { state, setActiveTab, setMockMode, setSettings, setAnswer, setBrief, setJournal, addJournal, setUploads, setLastQuestion, setJournalPrefill } = window.__UI_STATE__;
  const { getSettings, postAnswer, getBrief, getJournal, postJournal, postUpload } = window.__API__;

  function mountIcons(){
    if (window.lucide?.createIcons) window.lucide.createIcons({ attrs: { 'stroke-width': 1.5 } });
  }

  // Elements
  const tabButtons = Array.from(document.querySelectorAll('.tab-btn'));
  const questionInput = document.getElementById('questionInput');
  const qaForm = document.getElementById('qaForm');
  const retryAsk = document.getElementById('retryAsk');

  const answerSkeleton = document.getElementById('answerSkeleton');
  const answerError = document.getElementById('answerError');
  const answerInsufficient = document.getElementById('answerInsufficient');
  const answerCard = document.getElementById('answerCard');
  const thesisEl = document.getElementById('thesis');
  const setupEl = document.getElementById('setup');
  const invalidationEl = document.getElementById('invalidation');
  const levelsEl = document.getElementById('levels');
  const sourcesList = document.getElementById('sourcesList');
  const answerStrategy = document.getElementById('answerStrategy');
  const toJournalBtn = document.getElementById('toJournal');

  const chipK = document.getElementById('chipK');
  const chipN = document.getElementById('chipN');
  const chipTau = document.getElementById('chipTau');
  const chipReranker = document.getElementById('chipReranker');
  const chipMMR = document.getElementById('chipMMR');
  const chipRecency = document.getElementById('chipRecency');

  const btnMenu = document.getElementById('btnMenu');
  const mobileActions = document.getElementById('mobileActions');

  const btnBrief = document.getElementById('btnBrief');
  const mBtnBrief = document.getElementById('mBtnBrief');
  const briefModal = document.getElementById('briefModal');
  const refreshBrief = document.getElementById('refreshBrief');
  const macroStance = document.getElementById('macroStance');
  const macroNotes = document.getElementById('macroNotes');
  const ideasWrap = document.getElementById('ideasWrap');
  const calendarWrap = document.getElementById('calendarWrap');

  const btnJournal = document.getElementById('btnJournal');
  const mBtnJournal = document.getElementById('mBtnJournal');
  const journalModal = document.getElementById('journalModal');
  const journalList = document.getElementById('journalList');
  const journalForm = document.getElementById('journalForm');
  const jf_timestamp = document.getElementById('jf_timestamp');
  const jf_strategy = document.getElementById('jf_strategy');
  const jf_symbol = document.getElementById('jf_symbol');
  const jf_direction = document.getElementById('jf_direction');
  const jf_entry = document.getElementById('jf_entry');
  const jf_size = document.getElementById('jf_size');
  const jf_stop = document.getElementById('jf_stop');
  const jf_tp = document.getElementById('jf_tp');
  const jf_rationale = document.getElementById('jf_rationale');
  const jf_reset = document.getElementById('jf_reset');
  const exportCSVBtn = document.getElementById('exportCSV');
  const riskHint = document.getElementById('riskHint');
  const softWarn = document.getElementById('softWarn');

  const btnUpload = document.getElementById('btnUpload');
  const mBtnUpload = document.getElementById('mBtnUpload');
  const uploadModal = document.getElementById('uploadModal');
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('fileInput');
  const uploadList = document.getElementById('uploadList');
  const uploadStrategy = document.getElementById('uploadStrategy');
  const btnStartUpload = document.getElementById('btnStartUpload');

  const btnSettings = document.getElementById('btnSettings');
  const mBtnSettings = document.getElementById('mBtnSettings');
  const settingsModal = document.getElementById('settingsModal');
  const s_K = document.getElementById('s_K');
  const s_N = document.getElementById('s_N');
  const s_tau = document.getElementById('s_tau');
  const s_reranker = document.getElementById('s_reranker');
  const s_mmr = document.getElementById('s_mmr');
  const s_recency = document.getElementById('s_recency');

  const toggleMock = document.getElementById('toggleMock');
  const toggleMockLabel = document.getElementById('toggleMockLabel');
  const toggleMockKnob = document.getElementById('toggleMockKnob');
  const mToggleMock = document.getElementById('mToggleMock');
  const mToggleMockLabel = document.getElementById('mToggleMockLabel');
  const mToggleMockKnob = document.getElementById('mToggleMockKnob');
  // Tooltips: make titles available on hover
  document.querySelectorAll('.tab-btn').forEach(b => b.setAttribute('title', `Tab: ${b.textContent}`));
  document.getElementById('chipK')?.parentElement?.setAttribute('title', 'K = număr pasaje retrieve per query');
  document.getElementById('chipN')?.parentElement?.setAttribute('title', 'N = număr pasaje finale după reranker');
  document.getElementById('chipTau')?.parentElement?.setAttribute('title', 'τ = prag relevanță (tau)');
  document.getElementById('chipReranker')?.parentElement?.setAttribute('title', 'Reranker = ON/OFF');
  document.getElementById('chipMMR')?.parentElement?.setAttribute('title', 'MMR = diversitate rezultate');
  document.getElementById('chipRecency')?.parentElement?.setAttribute('title', 'Recency boost = folosire știri recente');

  function setActiveTabUI(tab){
    setActiveTab(tab);
    tabButtons.forEach(b => {
      const on = b.getAttribute('data-tab') === tab;
      b.setAttribute('aria-selected', on ? 'true' : 'false');
      b.classList.toggle('bg-gray-900', on);
      b.classList.toggle('text-white', on);
      b.classList.toggle('border', on);
      b.classList.toggle('border-gray-900', on);
    });
    answerCard.classList.add('hidden');
    answerInsufficient.classList.add('hidden');
    answerError.classList.add('hidden');
  }

  function uniqCitations(cits){ return (cits||[]).map((c, idx) => idx + 1); }
  function inlineWithCitations(text, cits){ const nums = uniqCitations(cits); if (!nums.length) return text||''; return `${text||''} ${nums.map(n=>`[${n}]`).join('')}`; }
  function truncate(str, n){ if (!str) return ''; return str.length > n ? str.slice(0, n-1) + '…' : str; }
  function stanceBadge(stance){
    const base = 'text-xs px-2 py-1 rounded-md border';
    if (!stance) return `<span class="${base} bg-white text-gray-700">—</span>`;
    const s = String(stance).toLowerCase();
    if (s.includes('favorabil')) return `<span class="${base} bg-emerald-50 border-emerald-200 text-emerald-700">favorabil</span>`;
    if (s.includes('nefavorabil')) return `<span class="${base} bg-rose-50 border-rose-200 text-rose-700">nefavorabil</span>`;
    return `<span class="${base} bg-amber-50 border-amber-200 text-amber-700">neutru</span>`;
  }
  function riskChip(label, type='risk'){
    const base = 'text-xs px-2 py-1 rounded-md border bg-gray-50 text-gray-700';
    if (!label) return `<span class="${base}">${type==='risk' ? 'Risc' : 'Incertitudine'}: —</span>`;
    const l = String(label).toLowerCase();
    if (l.includes('low')) return `<span class="${base} border-emerald-200 bg-emerald-50 text-emerald-700">${type==='risk' ? 'Risc' : 'Incertitudine'}: low</span>`;
    if (l.includes('high')) return `<span class="${base} border-rose-200 bg-rose-50 text-rose-700">${type==='risk' ? 'Risc' : 'Incertitudine'}: high</span>`;
    return `<span class="${base} border-amber-200 bg-amber-50 text-amber-700">${type==='risk' ? 'Risc' : 'Incertitudine'}: med</span>`;
  }

  async function loadSettings(){
    try{
      const data = await getSettings();
      setSettings(data);
      chipK.textContent = `K=${data?.K ?? '—'}`;
      chipN.textContent = `N=${data?.N ?? '—'}`;
      chipTau.textContent = `τ=${data?.tau ?? '—'}`;
      s_K.textContent = data?.K ?? '—';
      s_N.textContent = data?.N ?? '—';
      s_tau.textContent = data?.tau ?? '—';
      s_reranker.textContent = data?.reranker ? 'ON' : 'OFF';
      s_mmr.textContent = data?.mmr ? 'ON' : 'OFF';
      s_recency.textContent = data?.recency_boost ?? '—';
    }catch(e){ /* silent */ }
  }

  let lastAnswerPayload = null;
  async function askAnswer(question){
    setLastQuestion(question);
    answerCard.classList.add('hidden');
    answerError.classList.add('hidden');
    answerInsufficient.classList.add('hidden');
    answerSkeleton.classList.remove('hidden');
    try{
      const data = await postAnswer({ question, collection: state.activeTab });
      lastAnswerPayload = data;
      setAnswer(data);
      const cits = Array.isArray(data?.citations) ? data.citations : [];
      if (cits.length < 3){
        answerSkeleton.classList.add('hidden');
        answerInsufficient.classList.remove('hidden');
        return;
      }

      thesisEl.innerText = inlineWithCitations(data?.answer?.thesis || '', cits);
      setupEl.innerText = inlineWithCitations(data?.answer?.setup || '', cits);
      invalidationEl.innerText = inlineWithCitations(data?.answer?.invalidation || '', cits);
      const lv = (data?.answer?.levels || '').toString();
      levelsEl.innerHTML = '';
      if (lv){
        const parts = lv.split(/[,;]+/).map(s => s.trim()).filter(Boolean);
        const ul = document.createElement('ul'); ul.className = 'list-disc pl-5 space-y-1';
        parts.forEach(p => { const li = document.createElement('li'); li.textContent = p; ul.appendChild(li); });
        levelsEl.appendChild(ul);
        const refs = document.createElement('div'); refs.className = 'text-xs text-gray-500 mt-1'; refs.textContent = uniqCitations(cits).map(n => `[${n}]`).join('');
        levelsEl.appendChild(refs);
      } else { levelsEl.textContent = '—'; }

      // Risk chips
      const riskBadge = document.getElementById('riskBadge');
      const uncertaintyBadge = document.getElementById('uncertaintyBadge');
      riskBadge.outerHTML = riskChip(data?.answer?.risk || '—', 'risk');
      uncertaintyBadge.outerHTML = riskChip(data?.answer?.uncertainty || '—', 'uncertainty');

      // Strategy chip
      answerStrategy.textContent = state.activeTab.replace('_', '-');

      // Sources
      sourcesList.innerHTML = '';
      cits.forEach((c, idx) => {
        const li = document.createElement('li'); li.className = 'text-sm';
        li.innerHTML = `
          <div class="flex items-start gap-2 rounded-lg border bg-gray-50 px-2 py-2">
            <span class="text-xs font-medium text-gray-700">[${idx+1}]</span>
            <div class="flex-1 min-w-0">
              <div class="flex flex-wrap items-center gap-2">
                <span class="text-xs text-gray-700">${c?.doc_id ?? 'doc'}</span>
                <span class="text-xs text-gray-500">•</span>
                <span class="text-xs text-gray-500">p.${c?.page ?? '—'}</span>
              </div>
              <div class="text-xs text-gray-600 truncate">${truncate(c?.preview || '', 240)}</div>
            </div>
            <a class="ml-2 inline-flex items-center gap-1 text-xs px-2 py-1 rounded-md border bg-white hover:bg-gray-50" href="${c?.url || '#'}" target="_blank" rel="noopener noreferrer">
              <i data-lucide="external-link" class="w-3.5 h-3.5"></i> Deschide pasaj
            </a>
          </div>`;
        sourcesList.appendChild(li);
      });

      answerSkeleton.classList.add('hidden');
      answerCard.classList.remove('hidden');
      mountIcons();
    }catch(e){
      answerSkeleton.classList.add('hidden');
      answerError.classList.remove('hidden');
    }
  }

  // Tab events
  tabButtons.forEach(btn => btn.addEventListener('click', () => { setActiveTabUI(btn.getAttribute('data-tab')); questionInput.focus(); }));
  setActiveTabUI('EQ_INV');

  // Ask handlers
  qaForm.addEventListener('submit', (e) => { e.preventDefault(); const q = questionInput.value.trim(); if (!q) return; askAnswer(q); });
  retryAsk.addEventListener('click', () => { if (state.lastQuestion) askAnswer(state.lastQuestion); });

  // Mobile menu
  btnMenu?.addEventListener('click', () => { mobileActions.classList.toggle('hidden'); });

  // Brief modal
  function openBrief(){ briefModal.classList.remove('hidden'); loadBrief(); }
  function closeBrief(){ briefModal.classList.add('hidden'); }
  document.querySelectorAll('[data-close-brief]').forEach(b => b.addEventListener('click', closeBrief));
  btnBrief?.addEventListener('click', openBrief); mBtnBrief?.addEventListener('click', openBrief);

  async function loadBrief(){
    try{
      const data = await getBrief(); setBrief(data);
      macroStance.outerHTML = stanceBadge(data?.macro?.stance || '—');
      macroNotes.innerHTML = '';
      (data?.macro?.notes || []).forEach((n, idx) => {
        const row = document.createElement('div'); row.className = 'flex items-start gap-2 rounded-lg border bg-white px-2 py-2 mb-2';
        row.innerHTML = `
          <span class="text-xs text-gray-500">[${idx+1}]</span>
          <div class="flex-1 text-sm">${n?.text || ''}</div>
          <a href="${n?.citation?.url || '#'}" target="_blank" rel="noopener" class="ml-2 text-xs inline-flex items-center gap-1 px-2 py-1 rounded-md border bg-gray-50 hover:bg-gray-100">
            <i data-lucide="external-link" class="w-3.5 h-3.5"></i> Deschide pasaj
          </a>`;
        macroNotes.appendChild(row);
      });

      ideasWrap.innerHTML = '';
      const groups = [ { key:'EQ_INV', title:'EQ-INV' }, { key:'EQ_MOM', title:'EQ-MOM/PEAD' }, { key:'OPT_INCOME', title:'OPT-INCOME' } ];
      groups.forEach(g => {
        const arr = data?.ideas?.[g.key] || [];
        const box = document.createElement('div'); box.className = 'rounded-xl border bg-white p-3';
        box.innerHTML = `
          <div class="flex items-center justify-between mb-2">
            <div class="text-sm font-semibold">${g.title}</div>
            <span class="text-xs text-gray-500">${Math.min(3, arr.length)} idei</span>
          </div>
          <div class="space-y-2" id="ideas_${g.key}"></div>`;
        ideasWrap.appendChild(box);
        const wrap = box.querySelector(`#ideas_${g.key}`);
        arr.slice(0,3).forEach((idea, idx) => {
          const cits = idea?.citations || [];
          const row = document.createElement('div'); row.className = 'rounded-lg border bg-gray-50 px-2 py-2';
          const score = idea?.score != null ? Number(idea.score).toFixed(2) : '—';
          const unc = idea?.uncertainty || '—';
          row.innerHTML = `
            <div class="flex items-start gap-2">
              <span class="text-xs text-gray-500">[${idx+1}]</span>
              <div class="flex-1 min-w-0">
                <div class="text-sm">${inlineWithCitations(idea?.text || '', cits)}</div>
                <div class="mt-1 flex items-center gap-2 text-xs text-gray-500">
                  <span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded border bg-white"><i data-lucide="gauge" class="w-3.5 h-3.5"></i> scor: ${score}</span>
                  <span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded border bg-white"><i data-lucide="waves" class="w-3.5 h-3.5"></i> incertitudine: ${unc}</span>
                </div>
              </div>
              <div class="flex flex-col gap-1">
                <button class="open-idea inline-flex items-center gap-1 text-xs px-2 py-1 rounded-md border bg-white hover:bg-gray-50" data-strat="${g.key}">
                  <i data-lucide="square-arrow-out-up-right" class="w-3.5 h-3.5"></i> Deschide răspuns
                </button>
                <a class="inline-flex items-center gap-1 text-xs px-2 py-1 rounded-md border bg-white hover:bg-gray-50" href="${cits?.[0]?.url || '#'}" target="_blank" rel="noopener">
                  <i data-lucide="external-link" class="w-3.5 h-3.5"></i> Deschide pasaj
                </a>
              </div>
            </div>`;
          wrap.appendChild(row);
        });
      });

      calendarWrap.innerHTML = '';
      (data?.calendar || []).forEach(ev => {
        const card = document.createElement('div'); card.className = 'rounded-lg border bg-white px-3 py-2';
        card.innerHTML = `
          <div class="flex items-center justify-between">
            <div class="text-sm font-medium">${ev?.title || ''}</div>
            <span class="text-xs text-gray-500">${ev?.time || ''}</span>
          </div>
          <div class="mt-1 text-xs text-gray-600">${ev?.type || ''}${ev?.symbol ? ' • ' + ev.symbol : ''}</div>`;
        calendarWrap.appendChild(card);
      });
      mountIcons();

      ideasWrap.querySelectorAll('.open-idea').forEach(btn => btn.addEventListener('click', (e) => {
        const stratKey = e.currentTarget.getAttribute('data-strat');
        const tab = stratKey === 'EQ_INV' ? 'EQ_INV' : (stratKey === 'EQ_MOM' ? 'EQ_MOM_PEAD' : 'OPT_INCOME');
        setActiveTabUI(tab); closeBrief();
        questionInput.value = e.currentTarget.closest('.rounded-lg').querySelector('.text-sm').textContent.replace(/\s\[(\d+)\]+$/,'').trim();
        askAnswer(questionInput.value);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }));
    }catch(e){
      macroNotes.innerHTML = `<div class="text-sm text-rose-700 bg-rose-50 border border-rose-200 px-2 py-1 rounded-md inline-flex items-center gap-2"><i data-lucide="circle-alert" class="w-4 h-4"></i>Eroare la încărcarea Daily Brief.</div>`;
      ideasWrap.innerHTML = ''; calendarWrap.innerHTML = ''; mountIcons();
    }
  }
  refreshBrief?.addEventListener('click', loadBrief);

  // Journal modal
  function openJournal(prefill){
    journalModal.classList.remove('hidden');
    if (prefill?.strategy) jf_strategy.value = prefill.strategy;
    if (prefill?.rationale) jf_rationale.value = prefill.rationale;
    if (!jf_timestamp.value) jf_timestamp.value = new Date().toISOString().slice(0,16);
    loadJournal();
  }
  function closeJournal(){ journalModal.classList.add('hidden'); }
  document.querySelectorAll('[data-close-journal]').forEach(b => b.addEventListener('click', closeJournal));
  btnJournal?.addEventListener('click', () => openJournal()); mBtnJournal?.addEventListener('click', () => openJournal());

  async function loadJournal(){
    try{ const data = await getJournal(); setJournal(Array.isArray(data) ? data : (Array.isArray(data?.list) ? data.list : [])); renderJournalList(); }
    catch(e){ journalList.innerHTML = `<div class="text-sm text-rose-700 bg-rose-50 border border-rose-200 px-2 py-1 rounded-md inline-flex items-center gap-2"><i data-lucide="circle-alert" class="w-4 h-4"></i>Eroare la încărcarea jurnalului.</div>`; mountIcons(); }
  }

  function renderJournalList(){
    if (!state.journal.length){ journalList.innerHTML = `<div class="text-xs text-gray-500">Nu există intrări încă.</div>`; return; }
    journalList.innerHTML = '';
    state.journal.slice(0, 50).reverse().forEach(item => {
      const row = document.createElement('div'); row.className = 'rounded-lg border bg-white px-3 py-2';
      const rr = item?.rr ?? '—'; const pnl = item?.pnl ?? '—'; const status = item?.status ?? 'open'; const ansId = item?.answer_id;
      row.innerHTML = `
        <div class="flex items-center justify-between gap-2">
          <div class="min-w-0">
            <div class="text-sm font-medium truncate">${item.symbol || '—'} • ${item.direction || '—'} • ${item.entry ?? '—'} / ${item.stop ?? '—'} / ${item.tp ?? '—'}</div>
            <div class="text-xs text-gray-500 truncate">${item.timestamp || ''} • strat: ${item.strategy || ''} • tags: ${item.tags || ''}</div>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs px-2 py-0.5 rounded-md border ${status==='closed' ? 'bg-gray-900 text-white border-gray-900' : 'bg-gray-50'}">${status}</span>
            <span class="text-xs px-2 py-0.5 rounded-md border bg-gray-50">PnL: ${pnl}</span>
            <span class="text-xs px-2 py-0.5 rounded-md border bg-gray-50">R/R: ${rr}</span>
            <button class="see-answer inline-flex items-center gap-1 text-xs px-2 py-1 rounded-md border bg-gray-50 hover:bg-gray-100" ${ansId ? '' : 'disabled'}>
              <i data-lucide="square-arrow-out-up-right" class="w-3.5 h-3.5"></i> Răspuns
            </button>
          </div>
        </div>`;
      const btn = row.querySelector('.see-answer');
      btn?.addEventListener('click', () => { if (!ansId) return; setActiveTabUI('EQ_INV'); closeJournal(); window.scrollTo({ top: 0, behavior: 'smooth' }); });
      journalList.appendChild(row);
    });
    mountIcons();
  }

  function validateSoft(){
    const dir = jf_direction.value; const entry = parseFloat(jf_entry.value); const stop = parseFloat(jf_stop.value); const tp = parseFloat(jf_tp.value); let warn = false;
    if (!isNaN(entry) && !isNaN(stop)) { if (dir === 'long' && stop >= entry) warn = true; if (dir === 'short' && stop <= entry) warn = true; }
    if (!isNaN(entry) && !isNaN(tp)) { if (dir === 'long' && tp <= entry) warn = true; if (dir === 'short' && tp >= entry) warn = true; }
    softWarn.classList.toggle('hidden', !warn); riskHint.classList.toggle('hidden', !warn);
  }
  ;[jf_direction, jf_entry, jf_stop, jf_tp, jf_size].forEach(el => el.addEventListener('input', validateSoft));

  journalForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = { timestamp: jf_timestamp.value, strategy: jf_strategy.value, symbol: jf_symbol.value, direction: jf_direction.value, entry: jf_entry.value ? Number(jf_entry.value) : null, size: jf_size.value ? Number(jf_size.value) : null, stop: jf_stop.value ? Number(jf_stop.value) : null, tp: jf_tp.value ? Number(jf_tp.value) : null, rationale: jf_rationale.value, tags: jf_tags.value };
    validateSoft();
    try{ await postJournal(payload); await loadJournal(); jf_reset.click(); }catch(e2){ /* silent */ }
  });
  jf_reset.addEventListener('click', () => { journalForm.reset(); jf_timestamp.value = new Date().toISOString().slice(0,16); softWarn.classList.add('hidden'); riskHint.classList.add('hidden'); });

  // Export CSV
  exportCSVBtn.addEventListener('click', () => {
    const rows = state.journal.map(j => ({ timestamp: j.timestamp ?? '', strategy: j.strategy ?? '', symbol: j.symbol ?? '', direction: j.direction ?? '', entry: j.entry ?? '', size: j.size ?? '', stop: j.stop ?? '', tp: j.tp ?? '', rationale: (j.rationale ?? '').toString().replace(/\n/g, ' ').replace(/"/g, '""'), tags: (j.tags ?? '').toString().replace(/"/g, '""') }));
    const header = 'timestamp,strategy,symbol,direction,entry,size,stop,tp,rationale,tags';
    const csv = [header].concat(rows.map(r => [ r.timestamp, r.strategy, r.symbol, r.direction, r.entry, r.size, r.stop, r.tp, `"${r.rationale}"`, `"${r.tags}"` ].join(','))).join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = `journal_export_${new Date().toISOString().slice(0,10)}.csv`; document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url);
  });

  // Upload modal
  function openUpload(){ uploadModal.classList.remove('hidden'); }
  function closeUpload(){ uploadModal.classList.add('hidden'); }
  document.querySelectorAll('[data-close-upload]').forEach(b => b.addEventListener('click', closeUpload));
  btnUpload?.addEventListener('click', openUpload); mBtnUpload?.addEventListener('click', openUpload);

  // Dropzone
  let filesQueue = [];
  function renderUploads(list){
    if (!list.length){ uploadList.innerHTML = `<div class="text-xs text-gray-400">Niciun fișier încă.</div>`; return; }
    uploadList.innerHTML = '';
    list.forEach(f => {
      const row = document.createElement('div'); row.className = 'flex items-center justify-between rounded-lg border bg-white px-3 py-2 text-sm';
      const name = document.createElement('div'); name.className = 'truncate mr-2'; name.textContent = f.name;
      const right = document.createElement('div'); right.className = 'flex items-center gap-2';
      const status = document.createElement('span'); status.className = 'text-xs px-2 py-0.5 rounded-md border';
      if (f.status === 'accepted') status.className += ' bg-emerald-50 border-emerald-200 text-emerald-700';
      else if (f.status === 'dedup') status.className += ' bg-amber-50 border-amber-200 text-amber-700';
      else if (f.status === 'rejected') status.className += ' bg-rose-50 border-rose-200 text-rose-700';
      status.textContent = f.status || 'pending';
      const reason = document.createElement('span'); reason.className = 'text-xs text-gray-500'; reason.textContent = f.reason || '';
      right.appendChild(status); if (f.reason) right.appendChild(reason);
      row.appendChild(name); row.appendChild(right); uploadList.appendChild(row);
    });
  }

  ;['dragenter','dragover'].forEach(evt => dropzone.addEventListener(evt, e => { e.preventDefault(); e.stopPropagation(); dropzone.classList.add('ring-2','ring-gray-400'); }));
  ;['dragleave','drop'].forEach(evt => dropzone.addEventListener(evt, e => { e.preventDefault(); e.stopPropagation(); dropzone.classList.remove('ring-2','ring-gray-400'); }));
  dropzone.addEventListener('drop', (e) => { filesQueue = Array.from(e.dataTransfer.files || []); renderUploads(filesQueue); });
  fileInput.addEventListener('change', (e) => { filesQueue = Array.from(e.target.files || []); renderUploads(filesQueue); });
  btnStartUpload.addEventListener('click', async () => {
    if (!filesQueue.length) return; try{ const res = await postUpload(filesQueue, uploadStrategy.value); setUploads(res); renderUploads(res); }catch(e){ /* silent */ }
  });

  // Settings modal
  function openSettings(){ settingsModal.classList.remove('hidden'); }
  function closeSettings(){ settingsModal.classList.add('hidden'); }
  document.querySelectorAll('[data-close-settings]').forEach(b => b.addEventListener('click', closeSettings));
  btnSettings?.addEventListener('click', openSettings); mBtnSettings?.addEventListener('click', openSettings);

  // To journal prefill
  toJournalBtn.addEventListener('click', () => {
    const payload = lastAnswerPayload; if (!payload?.answer) return openJournal();
    const stratLetter = state.activeTab === 'EQ_INV' ? 'A' : (state.activeTab === 'EQ_MOM_PEAD' ? 'B' : 'C');
    openJournal({ strategy: stratLetter, rationale: `${payload.answer?.thesis || ''}\nSetup: ${payload.answer?.setup || ''}\nNiveluri: ${payload.answer?.levels || ''}` });
  });

  // Toggle Mock Mode
  function syncMockUI(){
    toggleMock.checked = state.mockMode; mToggleMock.checked = state.mockMode;
    toggleMockLabel.textContent = state.mockMode ? 'ON' : 'OFF'; mToggleMockLabel.textContent = state.mockMode ? 'ON' : 'OFF';
    toggleMockKnob.style.transform = state.mockMode ? 'translateX(0px)' : 'translateX(16px)';
    mToggleMockKnob.style.transform = state.mockMode ? 'translateX(0px)' : 'translateX(16px)';
    // Visual state: green when ON
    const onClass = 'bg-emerald-600';
    const offClass = 'bg-gray-900';
    const knobOn = 'bg-white';
    const knobOff = 'bg-white';
    const wrap = toggleMockKnob.parentElement; const mwrap = mToggleMockKnob.parentElement;
    if (wrap){ wrap.classList.toggle('bg-emerald-600', state.mockMode); wrap.classList.toggle('bg-gray-200', !state.mockMode); }
    if (mwrap){ mwrap.classList.toggle('bg-emerald-600', state.mockMode); mwrap.classList.toggle('bg-gray-200', !state.mockMode); }
  }
  toggleMock.addEventListener('change', () => { setMockMode(toggleMock.checked); syncMockUI(); });
  mToggleMock.addEventListener('change', () => { setMockMode(mToggleMock.checked); syncMockUI(); });

  // Init
  document.addEventListener('DOMContentLoaded', async () => {
    mountIcons();
    syncMockUI();
    await loadSettings();
  });
})();


