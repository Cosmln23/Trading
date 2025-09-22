// API client that can switch between mock and real fetch
(function(global){
  const { state } = global.__UI_STATE__;

  async function fetchJson(input, init){
    const res = await fetch(input, init);
    if (!res.ok) throw new Error('network');
    return res.json();
  }

  async function getSettings(){
    if (state.mockMode) return global.__MOCK_API__.getSettings();
    return fetchJson('/api/settings');
  }

  async function postAnswer(payload){
    if (state.mockMode) return global.__MOCK_API__.postAnswer(payload);
    return fetchJson('/api/answer', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  }

  async function getBrief(){
    if (state.mockMode) return global.__MOCK_API__.getBrief();
    return fetchJson('/api/brief');
  }

  async function getJournal(){
    if (state.mockMode) return global.__MOCK_API__.getJournal();
    return fetchJson('/api/journal');
  }

  async function postJournal(entry){
    if (state.mockMode) return global.__MOCK_API__.postJournal(entry);
    return fetchJson('/api/journal', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(entry) });
  }

  async function postUpload(files, strategy, kind){
    if (state.mockMode) return global.__MOCK_API__.postUpload(files, strategy);
    const form = new FormData();
    (files||[]).forEach(f => form.append('files', f));
    form.append('strategy', strategy);
    if (kind) form.append('kind', kind);
    return fetchJson('/api/upload', { method: 'POST', body: form });
  }

  async function getKpis(windowSec){
    if (state.mockMode) return { window_sec: windowSec||300, rpm: 0, error_rate_pct: 0, p50_ms: null, p95_ms: null, count: 0, index: { present: false } };
    const qs = new URLSearchParams(); if (windowSec) qs.set('window', String(windowSec));
    return fetchJson('/observability/kpis' + (qs.toString() ? ('?' + qs.toString()) : ''));
  }

  async function getEvents(limit){
    if (state.mockMode) return { list: [] };
    const qs = new URLSearchParams(); if (limit) qs.set('limit', String(limit));
    return fetchJson('/observability/events' + (qs.toString() ? ('?' + qs.toString()) : ''));
  }

  async function getCatalog(params){
    if (state.mockMode) return { books: [], news: [], count: { books: 0, news: 0 } };
    const qs = new URLSearchParams();
    if (params?.collection) qs.set('collection', params.collection);
    if (params?.q) qs.set('q', params.q);
    if (params?.limit) qs.set('limit', String(params.limit));
    return fetchJson('/api/catalog' + (qs.toString() ? ('?' + qs.toString()) : ''));
  }

  async function getUploadHistory(limit){
    if (state.mockMode) return { list: [] };
    const qs = new URLSearchParams(); if (limit) qs.set('limit', String(limit));
    return fetchJson('/api/upload_history' + (qs.toString() ? ('?' + qs.toString()) : ''));
  }

  // Chat APIs
  async function createChat(){
    if (state.mockMode) return { chat_id: 'demo', expires_at: null };
    return fetchJson('/api/chat/create', { method: 'POST' });
  }
  async function getChat(chatId){
    if (state.mockMode) return { chat_id: chatId || 'demo', messages: [] };
    return fetchJson(`/api/chat/${encodeURIComponent(chatId)}`);
  }
  async function postChat(payload){
    if (state.mockMode) return { chat_id: payload?.chat_id || 'demo', messages: [{ role: 'user', content: payload?.message||'' }, { role: 'assistant', content: '(mock) răspuns'}] };
    return fetchJson('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  }

  global.__API__ = { getSettings, postAnswer, getBrief, getJournal, postJournal, postUpload, getKpis, getEvents, getCatalog, getUploadHistory, createChat, getChat, postChat };
})(window);


