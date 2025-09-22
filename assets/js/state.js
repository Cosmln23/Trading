// Global UI state and helpers (no framework)
(function(global){
  const state = {
    activeTab: 'EQ_INV',
    mockMode: true,
    settings: null,
    lastQuestion: '',
    answer: null,
    citations: [],
    brief: null,
    journal: [],
    uploads: [],
    journalPrefill: null,
    catalog: { books: [], news: [] },
    chat: { chatId: null, messages: [] },
    chatMode: false
  };

  function setActiveTab(tab){ state.activeTab = tab; }
  function setMockMode(on){ state.mockMode = !!on; }
  function setSettings(s){ state.settings = s; }
  function setAnswer(ans){ state.answer = ans?.answer || null; state.citations = Array.isArray(ans?.citations) ? ans.citations : []; }
  function setBrief(b){ state.brief = b || null; }
  function setJournal(list){ state.journal = Array.isArray(list) ? list : []; }
  function addJournal(entry){ state.journal = [ ...(state.journal||[]), entry ]; }
  function setUploads(list){ state.uploads = Array.isArray(list) ? list : []; }
  function setLastQuestion(q){ state.lastQuestion = q || ''; }
  function setJournalPrefill(pref){ state.journalPrefill = pref || null; }
  function setCatalog(c){ state.catalog = c || { books: [], news: [] }; }
  function setChatSession(id){ state.chat.chatId = id || null; }
  function setChatMessages(msgs){ state.chat.messages = Array.isArray(msgs) ? msgs : []; }
  function setChatMode(on){ state.chatMode = !!on; }

  // export
  global.__UI_STATE__ = {
    state,
    setActiveTab, setMockMode, setSettings, setAnswer, setBrief,
    setJournal, addJournal, setUploads, setLastQuestion, setJournalPrefill,
    setCatalog,
    setChatSession, setChatMessages, setChatMode
  };
})(window);


