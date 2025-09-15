// Minimal fixtures and simulated delays for demo
(function(global){
  function delay(ms){ return new Promise(r => setTimeout(r, ms)); }

  const settings = { K: 20, N: 4, tau: 0.20, reranker: true, mmr: true, recency_boost: 'news', policy: 'context-only' };

  function buildSuccessAnswer(collection){
    return {
      answer: {
        thesis: 'Teză exemplu pentru ' + collection + ' cu sprijin în surse.',
        setup: 'Condiții tehnice și fundamentale favorabile.',
        invalidation: 'Invalidare la străpungerea nivelului cheie.',
        levels: 'entry 100, stop 95, TP 112; suplimentar 118',
        risk: 'med',
        uncertainty: 'low'
      },
      citations: [
        { doc_id: 'docA', page: 12, preview: 'Previzualizare pasaj A...', url: '#' },
        { doc_id: 'docB', page: 3, preview: 'Previzualizare pasaj B...', url: '#' },
        { doc_id: 'docC', page: 27, preview: 'Previzualizare pasaj C...', url: '#' }
      ]
    };
  }

  async function postAnswer({ question, collection }){
    await delay(400);
    const q = (question||'').toLowerCase();
    if (q.includes('ok')) return buildSuccessAnswer(collection);
    if (q.includes('lowctx')) return { answer: { thesis: '', setup: '', invalidation: '', levels: '', risk: '—', uncertainty: '—' }, citations: [] };
    throw new Error('network');
  }

  async function getBrief(){
    await delay(500);
    return {
      macro: {
        stance: 'favorabil',
        notes: [
          { text: 'CPI sub așteptări; real yields în scădere.', citation: { url: '#' } },
          { text: 'NFP stabil; USD slab; vol redus.', citation: { url: '#' } }
        ]
      },
      ideas: {
        EQ_INV: [ { text: 'ETF broad‑market cu discount la NAV [1]', score: 0.82, uncertainty: 'low', citations: [{url:'#'}] }, { text: 'Sector defensiv supraperformat [2]', score: 0.68, uncertainty: 'med', citations: [{url:'#'}] }, { text: 'Rotire spre quality [3]', score: 0.61, uncertainty: 'med', citations: [{url:'#'}] } ],
        EQ_MOM: [ { text: 'Breakout post‑earnings [1]', score: 0.75, uncertainty: 'med', citations: [{url:'#'}] }, { text: 'Gap + continuare [2]', score: 0.66, uncertainty: 'med', citations: [{url:'#'}] }, { text: 'Reversal pe volum [3]', score: 0.59, uncertainty: 'high', citations: [{url:'#'}] } ],
        OPT_INCOME: [ { text: 'Covered calls pe volatilitate scăzută [1]', score: 0.7, uncertainty: 'low', citations: [{url:'#'}] }, { text: 'Puturi cash‑secured pe suport [2]', score: 0.65, uncertainty: 'med', citations: [{url:'#'}] }, { text: 'Calendar spread conservator [3]', score: 0.6, uncertainty: 'med', citations: [{url:'#'}] } ]
      },
      calendar: [
        { time: '09:00', type: 'macro', title: 'CPI (RO)', symbol: '' },
        { time: '16:30', type: 'earnings', title: 'Earnings', symbol: 'AAPL' },
        { time: '18:00', type: 'macro', title: 'FOMC minutes', symbol: '' }
      ]
    };
  }

  async function getSettings(){ await delay(200); return settings; }

  // Journal
  let journal = [];
  async function getJournal(){ await delay(200); return journal.slice(); }
  async function postJournal(entry){ await delay(200); journal.push(entry); return { ok: true }; }

  // Uploads
  async function postUpload(files, strategy){
    await delay(600);
    return (files||[]).map((f, idx) => {
      if (idx % 3 === 0) return { name: f.name, size: f.size||0, status: 'accepted' };
      if (idx % 3 === 1) return { name: f.name, size: f.size||0, status: 'dedup' };
      return { name: f.name, size: f.size||0, status: 'rejected', reason: 'format neacceptat' };
    });
  }

  global.__MOCK_API__ = { postAnswer, getBrief, getSettings, getJournal, postJournal, postUpload };
})(window);


