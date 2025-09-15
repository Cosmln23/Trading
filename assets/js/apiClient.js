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

  async function postUpload(files, strategy){
    if (state.mockMode) return global.__MOCK_API__.postUpload(files, strategy);
    const form = new FormData();
    (files||[]).forEach(f => form.append('files', f));
    form.append('strategy', strategy);
    return fetchJson('/api/upload', { method: 'POST', body: form });
  }

  global.__API__ = { getSettings, postAnswer, getBrief, getJournal, postJournal, postUpload };
})(window);


