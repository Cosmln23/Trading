<html lang="ro"><head>
    <meta charset="utf-8">
    <title>Asistent Trading — Cloud-assisted RAG</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&amp;display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="min-h-screen antialiased bg-gray-50 text-gray-900" style="font-family: Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto;">
    <!-- Background (adapted from Responsive Navigation with Background) -->
    <div class="fixed inset-0 -z-10">
      <div class="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1542142460-5de862c36a6d?q=80&amp;w=2069&amp;auto=format&amp;fit=crop')] bg-cover bg-center"></div>
      <div class="absolute inset-0 bg-white/60"></div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
      <!-- Global Header -->
      <nav class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-gray-900 text-white flex items-center justify-center shadow-md">
            <i data-lucide="activity" class="w-4 h-4"></i>
          </div>
          <span class="text-lg tracking-tight font-semibold">Asistent Trading</span>
          <span class="hidden sm:inline text-gray-500 text-sm font-medium">Cloud‑assisted RAG</span>
        </div>

        <div class="hidden md:flex items-center gap-2">
          <button id="btnBrief" class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-white/70 backdrop-blur border border-gray-200 hover:bg-white transition focus:outline-none focus:ring-2 focus:ring-gray-900/10" aria-label="Daily Brief">
            <i data-lucide="sunrise" class="w-4 h-4"></i>
            <span class="text-sm font-medium">Daily Brief</span>
          </button>
          <button id="btnJournal" class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-white/70 backdrop-blur border border-gray-200 hover:bg-white transition focus:outline-none focus:ring-2 focus:ring-gray-900/10" aria-label="Jurnal">
            <i data-lucide="notebook-pen" class="w-4 h-4"></i>
            <span class="text-sm font-medium">Jurnal</span>
          </button>
          <button id="btnUpload" class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-white/70 backdrop-blur border border-gray-200 hover:bg-white transition focus:outline-none focus:ring-2 focus:ring-gray-900/10" aria-label="Upload">
            <i data-lucide="upload-cloud" class="w-4 h-4"></i>
            <span class="text-sm font-medium">Upload</span>
          </button>
          <button id="btnSettings" class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-900 text-white border border-gray-900 hover:bg-gray-800 transition focus:outline-none focus:ring-2 focus:ring-gray-900/20" aria-label="Setări">
            <i data-lucide="settings" class="w-4 h-4"></i>
            <span class="text-sm font-medium">Setări</span>
          </button>
        </div>

        <div class="md:hidden">
          <button id="btnMenu" class="inline-flex items-center justify-center p-2 rounded-lg bg-white/70 backdrop-blur border border-gray-200 hover:bg-white transition focus:outline-none focus:ring-2 focus:ring-gray-900/10" aria-label="Menu">
            <i data-lucide="menu" class="w-5 h-5"></i>
          </button>
        </div>
      </nav>

      <!-- Mobile Actions -->
      <div id="mobileActions" class="md:hidden mt-3 hidden">
        <div class="flex flex-wrap items-center gap-2">
          <button id="mBtnBrief" class="flex-1 inline-flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-white/70 backdrop-blur border border-gray-200 hover:bg-white transition focus:outline-none focus:ring-2 focus:ring-gray-900/10">
            <i data-lucide="sunrise" class="w-4 h-4"></i>
            <span class="text-sm font-medium">Daily Brief</span>
          </button>
          <button id="mBtnJournal" class="flex-1 inline-flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-white/70 backdrop-blur border border-gray-200 hover:bg-white transition focus:outline-none focus:ring-2 focus:ring-gray-900/10">
            <i data-lucide="notebook-pen" class="w-4 h-4"></i>
            <span class="text-sm font-medium">Jurnal</span>
          </button>
          <button id="mBtnUpload" class="flex-1 inline-flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-white/70 backdrop-blur border border-gray-200 hover:bg-white transition focus:outline-none focus:ring-2 focus:ring-gray-900/10">
            <i data-lucide="upload-cloud" class="w-4 h-4"></i>
            <span class="text-sm font-medium">Upload</span>
          </button>
          <button id="mBtnSettings" class="flex-1 inline-flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-gray-900 text-white border border-gray-900 hover:bg-gray-800 transition focus:outline-none focus:ring-2 focus:ring-gray-900/20">
            <i data-lucide="settings" class="w-4 h-4"></i>
            <span class="text-sm font-medium">Setări</span>
          </button>
        </div>
      </div>

      <!-- Context-Only Policy + Risk Notice -->
      <div class="mt-4 flex flex-wrap items-center gap-2">
        <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/70 backdrop-blur border border-gray-200">
          <div class="w-1.5 h-1.5 rounded-full bg-emerald-500"></div>
          <span class="text-xs font-medium">Răspuns generat strict din pasaje citate (Context-Only).</span>
        </div>
        <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-50 border border-amber-200 text-amber-800">
          <i data-lucide="alert-triangle" class="w-4 h-4"></i>
          <span class="text-xs font-medium">Sugestii, nu ordine. Respectă limitele de risc setate.</span>
        </div>
      </div>

      <!-- Strategy Tabs -->
      <div class="mt-6 bg-white/70 backdrop-blur border border-gray-200 rounded-2xl p-2">
        <div class="flex items-center justify-between">
          <div class="flex gap-1" role="tablist" aria-label="Strategii">
            <button data-tab="EQ_INV" class="tab-btn px-4 py-2 rounded-xl text-sm font-medium hover:bg-white focus:outline-none focus:ring-2 focus:ring-gray-900/10" aria-selected="true">EQ-INV</button>
            <button data-tab="EQ_MOM_PEAD" class="tab-btn px-4 py-2 rounded-xl text-sm font-medium hover:bg-white focus:outline-none focus:ring-2 focus:ring-gray-900/10" aria-selected="false">EQ-MOM/PEAD</button>
            <button data-tab="OPT_INCOME" class="tab-btn px-4 py-2 rounded-xl text-sm font-medium hover:bg-white focus:outline-none focus:ring-2 focus:ring-gray-900/10" aria-selected="false">OPT-INCOME</button>
          </div>
          <div class="hidden sm:flex items-center gap-2 text-xs text-gray-500 pr-1">
            <span class="inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-white border border-gray-200"><i data-lucide="filter" class="w-3.5 h-3.5"></i><span>K=—</span></span>
            <span class="inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-white border border-gray-200"><i data-lucide="list-filter" class="w-3.5 h-3.5"></i><span>N=—</span></span>
            <span class="inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-white border border-gray-200"><i data-lucide="sigma" class="w-3.5 h-3.5"></i><span>τ=—</span></span>
            <span class="inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-white border border-gray-200"><i data-lucide="scan-line" class="w-3.5 h-3.5"></i><span>Reranker ON</span></span>
            <span class="inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-white border border-gray-200"><i data-lucide="shuffle" class="w-3.5 h-3.5"></i><span>MMR ON</span></span>
            <span class="inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-white border border-gray-200"><i data-lucide="newspaper" class="w-3.5 h-3.5"></i><span>Recency: News</span></span>
          </div>
        </div>

        <!-- Query Row -->
        <div class="mt-3 bg-white border border-gray-200 rounded-xl p-2.5">
          <form id="qaForm" class="flex items-center gap-2" aria-label="Întrebare strategie">
            <div class="flex-1 relative">
              <input id="questionInput" type="text" placeholder="Adresează întrebarea ta pentru strategia activă..." class="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900/10 focus:border-gray-300 placeholder:text-gray-400" aria-label="Întrebare">
              <div class="absolute right-2.5 top-2.5 text-gray-400">
                <i data-lucide="message-square" class="w-4 h-4"></i>
              </div>
            </div>
            <button id="btnAsk" type="submit" class="inline-flex items-center gap-2 rounded-lg bg-gray-900 text-white px-4 py-2.5 text-sm font-medium hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-900/20">
              <i data-lucide="sparkles" class="w-4 h-4"></i>
              Răspunde
            </button>
          </form>
        </div>

        <!-- States and Answer -->
        <div id="answerRegion" class="mt-4">
          <!-- Skeleton -->
          <div id="answerSkeleton" class="hidden bg-white border border-gray-200 rounded-2xl p-4">
            <div class="animate-pulse">
              <div class="h-4 bg-gray-100 rounded w-24 mb-2"></div>
              <div class="h-5 bg-gray-100 rounded w-3/4 mb-1.5"></div>
              <div class="h-5 bg-gray-100 rounded w-2/3 mb-4"></div>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div class="h-24 bg-gray-100 rounded"></div>
                <div class="h-24 bg-gray-100 rounded"></div>
                <div class="h-24 bg-gray-100 rounded"></div>
              </div>
              <div class="h-4 bg-gray-100 rounded w-40 mt-4"></div>
            </div>
          </div>

          <!-- Error -->
          <div id="answerError" class="hidden bg-rose-50 text-rose-800 border border-rose-200 rounded-xl p-3 text-sm">
            <div class="flex items-center gap-2">
              <i data-lucide="circle-alert" class="w-4 h-4"></i>
              <span>Eroare de rețea. Reîncearcă.</span>
              <button id="retryAsk" class="ml-auto inline-flex items-center gap-1 px-2 py-1 rounded-md bg-rose-100 hover:bg-rose-200 text-rose-900 text-xs">
                <i data-lucide="rotate-cw" class="w-3.5 h-3.5"></i> Reîncearcă
              </button>
            </div>
          </div>

          <!-- Insufficient context -->
          <div id="answerInsufficient" class="hidden bg-amber-50 text-amber-900 border border-amber-200 rounded-xl p-3 text-sm">
            <div class="flex items-center gap-2">
              <i data-lucide="info" class="w-4 h-4"></i>
              <span>Nu am context suficient peste pragul de relevanță. Încarcă surse sau relaxează filtrele.</span>
            </div>
          </div>

          <!-- Answer Card -->
          <div id="answerCard" class="hidden bg-white border border-gray-200 rounded-2xl overflow-hidden">
            <div class="p-4 border-b border-gray-200 flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="w-7 h-7 rounded-lg bg-gray-900 text-white flex items-center justify-center">
                  <i data-lucide="brain-circuit" class="w-3.5 h-3.5"></i>
                </div>
                <h3 class="text-base tracking-tight font-semibold">Răspuns Strategie</h3>
                <span id="answerStrategy" class="ml-2 text-xs px-2 py-0.5 rounded-md border bg-gray-50 text-gray-700">—</span>
                <span class="ml-2 inline-flex items-center gap-1 text-xs text-gray-500"><i data-lucide="check-circle" class="w-3.5 h-3.5"></i> Citări obligatorii</span>
              </div>
              <div class="flex items-center gap-2">
                <span id="riskBadge" class="text-xs px-2 py-1 rounded-md border bg-gray-50 text-gray-700">Risc: —</span>
                <span id="uncertaintyBadge" class="text-xs px-2 py-1 rounded-md border bg-gray-50 text-gray-700">Incertitudine: —</span>
              </div>
            </div>

            <div class="p-4 space-y-4">
              <div>
                <div class="text-xs text-gray-500 mb-1">Teză</div>
                <p id="thesis" class="text-sm leading-relaxed"></p>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div class="rounded-xl border border-gray-200 p-3 bg-gray-50/50">
                  <div class="text-xs text-gray-500 mb-1">Setup</div>
                  <p id="setup" class="text-sm"></p>
                </div>
                <div class="rounded-xl border border-gray-200 p-3 bg-gray-50/50">
                  <div class="text-xs text-gray-500 mb-1">Invalidare</div>
                  <p id="invalidation" class="text-sm"></p>
                </div>
                <div class="rounded-xl border border-gray-200 p-3 bg-gray-50/50">
                  <div class="text-xs text-gray-500 mb-1">Niveluri</div>
                  <div id="levels" class="text-sm"></div>
                </div>
              </div>

              <div class="flex flex-wrap items-center gap-2 pt-1">
                <button id="toJournal" class="inline-flex items-center gap-2 rounded-lg bg-gray-900 text-white px-3 py-2 text-sm font-medium hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-900/20">
                  <i data-lucide="send" class="w-4 h-4"></i>
                  Trimite în Jurnal
                </button>
              </div>

              <div class="pt-2 border-t border-gray-200">
                <div class="text-xs text-gray-500 mb-2">Surse</div>
                <ul id="sourcesList" class="space-y-2"></ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer tiny -->
      <div class="py-8">
        <div class="text-center text-xs text-gray-500">
          Latency țintă: Query &lt; 3s • Daily Brief &lt; 8s • Toate ideile au citări clicabile.
        </div>
      </div>
    </div>

    <!-- Daily Brief Modal -->
    <div id="briefModal" class="hidden fixed inset-0 z-50">
      <div class="absolute inset-0 bg-black/40"></div>
      <div class="relative mx-auto my-8 w-[95%] max-w-5xl bg-white rounded-2xl border border-gray-200 overflow-hidden">
        <div class="flex items-center justify-between px-4 py-3 border-b border-gray-200">
          <div class="flex items-center gap-2">
            <i data-lucide="sunrise" class="w-5 h-5 text-gray-700"></i>
            <h2 class="text-lg tracking-tight font-semibold">Daily Brief (08:00)</h2>
            <span class="text-xs text-gray-500">Regim Macro + Idei + Calendar</span>
          </div>
          <div class="flex items-center gap-2">
            <button id="refreshBrief" class="inline-flex items-center gap-1 text-xs px-2 py-1 rounded-md border bg-gray-50 hover:bg-gray-100">
              <i data-lucide="rotate-cw" class="w-3.5 h-3.5"></i> Actualizează
            </button>
            <button data-close-brief="" class="p-2 rounded-lg border bg-gray-50 hover:bg-gray-100" aria-label="Închide">
              <i data-lucide="x" class="w-4 h-4"></i>
            </button>
          </div>
        </div>

        <div id="briefBody" class="p-4 grid grid-cols-1 lg:grid-cols-3 gap-4">
          <!-- Macro Panel -->
          <div class="lg:col-span-1 rounded-xl border border-gray-200 bg-gray-50/50 p-3">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-2">
                <i data-lucide="globe-2" class="w-4 h-4 text-gray-700"></i>
                <h3 class="text-sm font-semibold tracking-tight">Regim piață (Macro)</h3>
              </div>
              <span id="macroStance" class="text-xs px-2 py-1 rounded-md border bg-white">—</span>
            </div>
            <div id="macroNotes">
              <!-- Skeleton -->
              <div class="brief-skel animate-pulse space-y-2">
                <div class="h-4 bg-gray-100 rounded"></div>
                <div class="h-4 bg-gray-100 rounded w-5/6"></div>
                <div class="h-4 bg-gray-100 rounded w-4/6"></div>
              </div>
            </div>
          </div>

          <!-- Ideas Panel -->
          <div class="lg:col-span-2 rounded-xl border border-gray-200 bg-gray-50/50 p-3">
            <div class="flex items-center gap-2 mb-2">
              <i data-lucide="lightbulb" class="w-4 h-4 text-gray-700"></i>
              <h3 class="text-sm font-semibold tracking-tight">Top 3 idei / strategie</h3>
            </div>
            <div id="ideasWrap" class="space-y-3">
              <!-- Skeleton -->
              <div class="animate-pulse grid grid-cols-1 md:grid-cols-3 gap-3">
                <div class="h-24 bg-gray-100 rounded"></div>
                <div class="h-24 bg-gray-100 rounded"></div>
                <div class="h-24 bg-gray-100 rounded"></div>
              </div>
            </div>
          </div>

          <!-- Calendar Panel -->
          <div class="lg:col-span-3 rounded-xl border border-gray-200 bg-gray-50/50 p-3">
            <div class="flex items-center gap-2 mb-2">
              <i data-lucide="calendar-days" class="w-4 h-4 text-gray-700"></i>
              <h3 class="text-sm font-semibold tracking-tight">Calendar evenimente (azi)</h3>
            </div>
            <div id="calendarWrap" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              <!-- Skeleton items -->
              <div class="animate-pulse h-16 bg-gray-100 rounded"></div>
              <div class="animate-pulse h-16 bg-gray-100 rounded"></div>
              <div class="animate-pulse h-16 bg-gray-100 rounded"></div>
            </div>
          </div>
        </div>

        <div class="px-4 py-3 border-t border-gray-200 flex items-center justify-between">
          <span class="text-xs text-gray-500">Toate notele și ideile includ citări. Click „Deschide pasaj” pentru auditare.</span>
          <button data-close-brief="" class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-900 text-white text-sm hover:bg-gray-800">
            <i data-lucide="check" class="w-4 h-4"></i> Închis
          </button>
        </div>
      </div>
    </div>

    <!-- Journal Modal -->
    <div id="journalModal" class="hidden fixed inset-0 z-50">
      <div class="absolute inset-0 bg-black/40"></div>
      <div class="relative mx-auto my-8 w-[95%] max-w-5xl bg-white rounded-2xl border border-gray-200 overflow-hidden">
        <div class="flex items-center justify-between px-4 py-3 border-b border-gray-200">
          <div class="flex items-center gap-2">
            <i data-lucide="notebook-pen" class="w-5 h-5 text-gray-700"></i>
            <h2 class="text-lg tracking-tight font-semibold">Jurnal decizii</h2>
            <span class="text-xs text-gray-500">CSV schema fixă</span>
          </div>
          <div class="flex items-center gap-2">
            <button id="exportCSV" class="inline-flex items-center gap-2 px-3 py-2 rounded-lg border bg-gray-50 hover:bg-gray-100 text-sm">
              <i data-lucide="file-down" class="w-4 h-4"></i> Export CSV
            </button>
            <button data-close-journal="" class="p-2 rounded-lg border bg-gray-50 hover:bg-gray-100" aria-label="Închide">
              <i data-lucide="x" class="w-4 h-4"></i>
            </button>
          </div>
        </div>

        <div class="p-4 grid grid-cols-1 lg:grid-cols-3 gap-4">
          <!-- Add Entry -->
          <div class="lg:col-span-1 rounded-xl border border-gray-200 bg-gray-50/50 p-3">
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-sm font-semibold tracking-tight">Add entry</h3>
              <span id="riskHint" class="text-xs text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded-md hidden">Verifică riscul</span>
            </div>

            <form id="journalForm" class="space-y-2 text-sm">
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-xs text-gray-500 mb-1">timestamp</label>
                  <input id="jf_timestamp" type="datetime-local" class="w-full rounded-lg border border-gray-200 px-2 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900/10">
                </div>
                <div>
                  <label class="block text-xs text-gray-500 mb-1">strategy (A/B/C)</label>
                  <select id="jf_strategy" class="w-full rounded-lg border border-gray-200 px-2 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900/10">
                    <option value="A">A — EQ-INV</option>
                    <option value="B">B — EQ-MOM/PEAD</option>
                    <option value="C">C — OPT-INCOME</option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-xs text-gray-500 mb-1">symbol</label>
                  <input id="jf_symbol" type="text" placeholder="AAPL" class="w-full rounded-lg border border-gray-200 px-2 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900/10">
                </div>
                <div>
                  <label class="block text-xs text-gray-500 mb-1">direction</label>
                  <select id="jf_direction" class="w-full rounded-lg border border-gray-200 px-2 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900/10">
                    <option value="long">long</option>
                    <option value="short">short</option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-3 gap-2">
                <div>
                  <label class="block text-xs text-gray-500 mb-1">entry</label>
                  <input id="jf_entry" type="number" step="0.0001" class="w-full rounded-lg border border-gray-200 px-2 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900/10">
                </div>
                <div>
                  <label class="block text-xs text-gray-500 mb-1">size</label>
                  <input id="jf_size" type="number" step="0.0001" class="w-full rounded-lg border border-gray-200 px-2 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900/10">
                </div>
                <div>
                  <label class="block text-xs text-gray-500 mb-1">stop</label>
                  <input id="jf_stop" type="number" step="0.0001" class="w-full rounded-lg border border-gray-200 px-2 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900/10">
                </div>
              </div>

              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-xs text-gray-500 mb-1">tp</label>
                  <input id="jf_tp" type="number" step="0.0001" class="w-full rounded-lg border border-gray-200 px-2 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900/10">
                </div>
                <div>
                  <label class="block text-xs text-gray-500 mb-1">tags</label>
                  <input id="jf_tags" type="text" placeholder="breakout, earnings" class="w-full rounded-lg border border-gray-200 px-2 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900/10">
                </div>
              </div>

              <div>
                <label class="block text-xs text-gray-500 mb-1">rationale</label>
                <textarea id="jf_rationale" rows="4" class="w-full rounded-lg border border-gray-200 px-2 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900/10" placeholder="Teză + niveluri (precompletate din răspuns)."></textarea>
              </div>

              <div id="softWarn" class="hidden text-xs text-amber-700 bg-amber-50 border border-amber-200 px-2 py-1 rounded-md">
                Avertizare: setarea stop/TP sau mărimea poate depăși profilul de risc al trade-ului.
              </div>

              <div class="pt-1 flex items-center gap-2">
                <button id="jf_submit" type="submit" class="inline-flex items-center gap-2 rounded-lg bg-gray-900 text-white px-3 py-2 text-sm hover:bg-gray-800">
                  <i data-lucide="plus" class="w-4 h-4"></i> Adaugă
                </button>
                <button id="jf_reset" type="button" class="inline-flex items-center gap-2 rounded-lg border bg-gray-50 px-3 py-2 text-sm hover:bg-gray-100">
                  <i data-lucide="eraser" class="w-4 h-4"></i> Reset
                </button>
              </div>
            </form>
          </div>

          <!-- List -->
          <div class="lg:col-span-2 rounded-xl border border-gray-200 bg-gray-50/50 p-3">
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-sm font-semibold tracking-tight">Decizii recente</h3>
              <div class="text-xs text-gray-500">Status • PnL • R/R • Link răspuns</div>
            </div>
            <div id="journalList" class="space-y-2">
              <div class="animate-pulse h-16 bg-gray-100 rounded"></div>
              <div class="animate-pulse h-16 bg-gray-100 rounded"></div>
            </div>
          </div>
        </div>

        <div class="px-4 py-3 border-t border-gray-200 text-xs text-gray-500">
          Export CSV: câmpuri — timestamp,strategy,symbol,direction,entry,size,stop,tp,rationale,tags
        </div>
      </div>
    </div>

    <!-- Upload Modal -->
    <div id="uploadModal" class="hidden fixed inset-0 z-50">
      <div class="absolute inset-0 bg-black/40"></div>
      <div class="relative mx-auto my-8 w-[95%] max-w-3xl bg-white rounded-2xl border border-gray-200 overflow-hidden">
        <div class="flex items-center justify-between px-4 py-3 border-b border-gray-200">
          <div class="flex items-center gap-2">
            <i data-lucide="upload-cloud" class="w-5 h-5 text-gray-700"></i>
            <h2 class="text-lg tracking-tight font-semibold">Upload surse</h2>
          </div>
          <button data-close-upload="" class="p-2 rounded-lg border bg-gray-50 hover:bg-gray-100" aria-label="Închide">
            <i data-lucide="x" class="w-4 h-4"></i>
          </button>
        </div>

        <div class="p-4 space-y-3">
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div class="sm:col-span-2">
              <label class="block text-xs text-gray-500 mb-1">Fișiere (drag &amp; drop sau alege)</label>
              <div id="dropzone" class="flex items-center justify-center h-28 rounded-xl border-2 border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100 text-gray-500">
                <div class="text-center">
                  <i data-lucide="files" class="w-5 h-5 mx-auto mb-1"></i>
                  <div class="text-xs">Trage fișiere aici sau</div>
                  <label class="inline-flex items-center gap-1 mt-1 px-2 py-1 rounded-md border bg-white text-xs cursor-pointer">
                    <i data-lucide="folder-open" class="w-3.5 h-3.5"></i>
                    <input id="fileInput" type="file" class="hidden" multiple="">
                    Alege fișiere
                  </label>
                </div>
              </div>
            </div>
            <div>
              <label class="block text-xs text-gray-500 mb-1">Strategia țintă</label>
              <select id="uploadStrategy" class="w-full rounded-lg border border-gray-200 px-2 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900/10">
                <option value="A">A — EQ-INV</option>
                <option value="B">B — EQ-MOM/PEAD</option>
                <option value="C">C — OPT-INCOME</option>
              </select>
              <button id="btnStartUpload" class="mt-2 w-full inline-flex items-center justify-center gap-2 rounded-lg bg-gray-900 text-white px-3 py-2 text-sm hover:bg-gray-800">
                <i data-lucide="arrow-up-right" class="w-4 h-4"></i> Încarcă
              </button>
            </div>
          </div>

          <div class="pt-2 border-t border-gray-200">
            <div class="text-xs text-gray-500 mb-2">Status ingestie</div>
            <div id="uploadList" class="space-y-2">
              <div class="text-xs text-gray-400">Niciun fișier încă.</div>
            </div>
          </div>
        </div>

        <div class="px-4 py-3 border-t border-gray-200 text-xs text-gray-500">
          Acceptat • Dedup • Respins (motiv)
        </div>
      </div>
    </div>

    <!-- Settings Modal -->
    <div id="settingsModal" class="hidden fixed inset-0 z-50">
      <div class="absolute inset-0 bg-black/40"></div>
      <div class="relative mx-auto my-8 w-[95%] max-w-3xl bg-white rounded-2xl border border-gray-200 overflow-hidden">
        <div class="flex items-center justify-between px-4 py-3 border-b border-gray-200">
          <div class="flex items-center gap-2">
            <i data-lucide="settings" class="w-5 h-5 text-gray-700"></i>
            <h2 class="text-lg tracking-tight font-semibold">Setări</h2>
          </div>
          <button data-close-settings="" class="p-2 rounded-lg border bg-gray-50 hover:bg-gray-100" aria-label="Închide">
            <i data-lucide="x" class="w-4 h-4"></i>
          </button>
        </div>

        <div class="p-4 grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
          <div class="rounded-xl border border-gray-200 bg-gray-50/50 p-3">
            <div class="text-xs text-gray-500 mb-2">Retrieval (read-only)</div>
            <div class="grid grid-cols-2 gap-2">
              <div class="flex items-center justify-between rounded-lg border bg-white px-2 py-1.5"><span>K</span><span id="s_K" class="text-gray-600">—</span></div>
              <div class="flex items-center justify-between rounded-lg border bg-white px-2 py-1.5"><span>N</span><span id="s_N" class="text-gray-600">—</span></div>
              <div class="flex items-center justify-between rounded-lg border bg-white px-2 py-1.5"><span>τ</span><span id="s_tau" class="text-gray-600">—</span></div>
              <div class="flex items-center justify-between rounded-lg border bg-white px-2 py-1.5"><span>Reranker</span><span id="s_reranker" class="text-gray-600">—</span></div>
              <div class="flex items-center justify-between rounded-lg border bg-white px-2 py-1.5"><span>MMR</span><span id="s_mmr" class="text-gray-600">—</span></div>
              <div class="flex items-center justify-between rounded-lg border bg-white px-2 py-1.5"><span>Recency</span><span id="s_recency" class="text-gray-600">—</span></div>
            </div>
          </div>

          <div class="rounded-xl border border-gray-200 bg-gray-50/50 p-3">
            <div class="text-xs text-gray-500 mb-2">Policy</div>
            <div class="flex items-center justify-between rounded-lg border bg-white px-3 py-2">
              <div class="text-sm">Context-Only</div>
              <div class="relative">
                <label class="inline-flex items-center">
                  <input type="checkbox" checked="" disabled="" class="peer sr-only">
                  <span class="w-10 h-6 rounded-full bg-gray-900/80 peer-checked:bg-gray-900 relative">
                    <span class="absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white transition-all peer-checked:translate-x-4"></span>
                  </span>
                </label>
              </div>
            </div>
            <div class="mt-2 text-xs text-gray-500">Fixat ON în V1 (nu poate fi modificat).</div>
          </div>

          <div class="sm:col-span-2 rounded-xl border border-gray-200 bg-gray-50/50 p-3">
            <div class="text-xs text-gray-500 mb-2">Portofoliu CSV — format câmpuri (conform Jurnal)</div>
            <div class="rounded-lg border bg-white px-3 py-2 text-xs text-gray-700 overflow-x-auto">timestamp,strategy,symbol,direction,entry,size,stop,tp,rationale,tags</div>
          </div>
        </div>

        <div class="px-4 py-3 border-t border-gray-200 text-xs text-gray-500">
          Valorile sunt informative; UI nu modifică parametrii de retrieval.
        </div>
      </div>
    </div>

    <!-- Scripts -->
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <script>
      // Icon setup with stroke-width=1.5
      function mountIcons() {
        lucide.createIcons({
          attrs: { 'stroke-width': 1.5 }
        });
      }
      document.addEventListener('DOMContentLoaded', mountIcons);

      // State
      const state = {
        activeTab: 'EQ_INV',
        settings: null,
        lastQuestion: '',
        answer: null,
        citations: [],
        brief: null,
        journal: [],
        uploads: [],
        journalPrefill: null
      };

      // Elements
      const tabButtons = Array.from(document.querySelectorAll('.tab-btn'));
      const questionInput = document.getElementById('questionInput');
      const qaForm = document.getElementById('qaForm');
      const btnAsk = document.getElementById('btnAsk');

      const answerRegion = document.getElementById('answerRegion');
      const answerSkeleton = document.getElementById('answerSkeleton');
      const answerError = document.getElementById('answerError');
      const retryAsk = document.getElementById('retryAsk');
      const answerInsufficient = document.getElementById('answerInsufficient');
      const answerCard = document.getElementById('answerCard');

      const thesisEl = document.getElementById('thesis');
      const setupEl = document.getElementById('setup');
      const invalidationEl = document.getElementById('invalidation');
      const levelsEl = document.getElementById('levels');
      const riskBadge = document.getElementById('riskBadge');
      const uncertaintyBadge = document.getElementById('uncertaintyBadge');
      const sourcesList = document.getElementById('sourcesList');
      const answerStrategy = document.getElementById('answerStrategy');
      const toJournalBtn = document.getElementById('toJournal');

      // Header actions
      const btnMenu = document.getElementById('btnMenu');
      const mobileActions = document.getElementById('mobileActions');
      const btnBrief = document.getElementById('btnBrief');
      const btnJournal = document.getElementById('btnJournal');
      const btnUpload = document.getElementById('btnUpload');
      const btnSettings = document.getElementById('btnSettings');
      const mBtnBrief = document.getElementById('mBtnBrief');
      const mBtnJournal = document.getElementById('mBtnJournal');
      const mBtnUpload = document.getElementById('mBtnUpload');
      const mBtnSettings = document.getElementById('mBtnSettings');

      // Modals
      const briefModal = document.getElementById('briefModal');
      const briefBody = document.getElementById('briefBody');
      const refreshBrief = document.getElementById('refreshBrief');
      const macroStance = document.getElementById('macroStance');
      const macroNotes = document.getElementById('macroNotes');
      const ideasWrap = document.getElementById('ideasWrap');
      const calendarWrap = document.getElementById('calendarWrap');

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
      const jf_submit = document.getElementById('jf_submit');
      const jf_reset = document.getElementById('jf_reset');
      const riskHint = document.getElementById('riskHint');
      const softWarn = document.getElementById('softWarn');
      const exportCSVBtn = document.getElementById('exportCSV');

      const uploadModal = document.getElementById('uploadModal');
      const dropzone = document.getElementById('dropzone');
      const fileInput = document.getElementById('fileInput');
      const uploadList = document.getElementById('uploadList');
      const uploadStrategy = document.getElementById('uploadStrategy');
      const btnStartUpload = document.getElementById('btnStartUpload');

      const settingsModal = document.getElementById('settingsModal');
      const s_K = document.getElementById('s_K');
      const s_N = document.getElementById('s_N');
      const s_tau = document.getElementById('s_tau');
      const s_reranker = document.getElementById('s_reranker');
      const s_mmr = document.getElementById('s_mmr');
      const s_recency = document.getElementById('s_recency');

      // Helpers
      function mapTabToJournalStrategy(tab) {
        return tab === 'EQ_INV' ? 'A' : (tab === 'EQ_MOM_PEAD' ? 'B' : 'C');
      }
      function mapJournalStrategyToTab(letter) {
        return letter === 'A' ? 'EQ_INV' : (letter === 'B' ? 'EQ_MOM_PEAD' : 'OPT_INCOME');
      }
      function stanceBadge(stance) {
        const base = 'text-xs px-2 py-1 rounded-md border';
        if (!stance) return `<span class="${base} bg-white text-gray-700">—</span>`;
        if (stance.toLowerCase().includes('favorabil')) return `<span class="${base} bg-emerald-50 border-emerald-200 text-emerald-700">favorabil</span>`;
        if (stance.toLowerCase().includes('nefavorabil')) return `<span class="${base} bg-rose-50 border-rose-200 text-rose-700">nefavorabil</span>`;
        return `<span class="${base} bg-amber-50 border-amber-200 text-amber-700">neutru</span>`;
      }
      function riskChip(label, type='risk') {
        const base = 'text-xs px-2 py-1 rounded-md border bg-gray-50 text-gray-700';
        if (!label) return `<span class="${base}">${type === 'risk' ? 'Risc' : 'Incertitudine'}: —</span>`;
        const l = String(label).toLowerCase();
        if (l.includes('low')) return `<span class="${base} border-emerald-200 bg-emerald-50 text-emerald-700">${type === 'risk' ? 'Risc' : 'Incertitudine'}: low</span>`;
        if (l.includes('high')) return `<span class="${base} border-rose-200 bg-rose-50 text-rose-700">${type === 'risk' ? 'Risc' : 'Incertitudine'}: high</span>`;
        return `<span class="${base} border-amber-200 bg-amber-50 text-amber-700">${type === 'risk' ? 'Risc' : 'Incertitudine'}: med</span>`;
      }
      function uniqCitations(cits) {
        return (cits || []).map((c, idx) => idx + 1);
      }
      function inlineWithCitations(text, cits) {
        const nums = uniqCitations(cits);
        if (!nums.length) return text || '';
        const refs = nums.map(n => `[${n}]`).join('');
        return `${text || ''} ${refs}`;
      }
      function truncate(str, n) {
        if (!str) return '';
        return str.length > n ? str.slice(0, n - 1) + '…' : str;
      }
      function setActiveTab(tab) {
        state.activeTab = tab;
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

      // Fetch Settings
      async function loadSettings() {
        try {
          const res = await fetch('/api/settings');
          if (!res.ok) throw new Error('err');
          const data = await res.json();
          state.settings = data || {};
          s_K.textContent = data?.K ?? '—';
          s_N.textContent = data?.N ?? '—';
          s_tau.textContent = data?.tau ?? '—';
          s_reranker.textContent = data?.reranker ? 'ON' : 'OFF';
          s_mmr.textContent = data?.mmr ? 'ON' : 'OFF';
          s_recency.textContent = data?.recency_boost ?? '—';

          // Mirror into header chips
          const chips = document.querySelectorAll('.sm\\:flex span');
          if (chips.length >= 6) {
            chips[0].querySelector('span:last-child').textContent = `K=${data?.K ?? '—'}`;
            chips[1].querySelector('span:last-child').textContent = `N=${data?.N ?? '—'}`;
            chips[2].querySelector('span:last-child').textContent = `τ=${data?.tau ?? '—'}`;
          }
        } catch (e) {
          // leave defaults
        }
      }

      // Ask /api/answer
      let lastAnswerPayload = null;
      async function askAnswer(question) {
        state.lastQuestion = question;
        answerCard.classList.add('hidden');
        answerError.classList.add('hidden');
        answerInsufficient.classList.add('hidden');
        answerSkeleton.classList.remove('hidden');

        try {
          const res = await fetch('/api/answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              question,
              collection: state.activeTab // strict routing per tab
            })
          });
          if (!res.ok) throw new Error('network');
          const data = await res.json();
          lastAnswerPayload = data;
          const cits = Array.isArray(data?.citations) ? data.citations : [];
          // Fail-safe: if < 3 passages above threshold (proxied here by citations count)
          if (cits.length < 3) {
            answerSkeleton.classList.add('hidden');
            answerInsufficient.classList.remove('hidden');
            return;
          }

          // Render answer with inline [n]
          const nums = uniqCitations(cits);
          thesisEl.textContent = ''; setupEl.textContent=''; invalidationEl.textContent=''; levelsEl.textContent='';

          thesisEl.innerText = inlineWithCitations(data?.answer?.thesis || '', cits);
          setupEl.innerText = inlineWithCitations(data?.answer?.setup || '', cits);
          invalidationEl.innerText = inlineWithCitations(data?.answer?.invalidation || '', cits);

          // Levels list (clear, bullet)
          const lv = (data?.answer?.levels || '').toString();
          levelsEl.innerHTML = '';
          if (lv) {
            const parts = lv.split(/[,;]+/).map(s => s.trim()).filter(Boolean);
            const ul = document.createElement('ul');
            ul.className = 'list-disc pl-5 space-y-1';
            parts.forEach(p => {
              const li = document.createElement('li');
              li.textContent = p;
              ul.appendChild(li);
            });
            levelsEl.appendChild(ul);
            const refs = document.createElement('div');
            refs.className = 'text-xs text-gray-500 mt-1';
            refs.textContent = nums.map(n => `[${n}]`).join('');
            levelsEl.appendChild(refs);
          } else {
            levelsEl.textContent = '—';
          }

          riskBadge.outerHTML = riskChip(data?.answer?.risk || '—', 'risk');
          uncertaintyBadge.outerHTML = riskChip(data?.answer?.uncertainty || '—', 'uncertainty');

          // Strategy chip
          answerStrategy.textContent = state.activeTab.replace('_', '-');

          // Sources
          sourcesList.innerHTML = '';
          cits.forEach((c, idx) => {
            const li = document.createElement('li');
            li.className = 'text-sm';
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
              </div>
            `;
            sourcesList.appendChild(li);
          });

          answerSkeleton.classList.add('hidden');
          answerCard.classList.remove('hidden');
          mountIcons();
        } catch (e) {
          answerSkeleton.classList.add('hidden');
          answerError.classList.remove('hidden');
        }
      }

      // Tab events
      tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
          setActiveTab(btn.getAttribute('data-tab'));
          questionInput.focus();
        });
      });
      setActiveTab('EQ_INV');

      // Ask handlers
      qaForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const q = questionInput.value.trim();
        if (!q) return;
        askAnswer(q);
      });
      retryAsk.addEventListener('click', () => {
        if (state.lastQuestion) askAnswer(state.lastQuestion);
      });

      // Journal prefill
      toJournalBtn.addEventListener('click', () => {
        const payload = lastAnswerPayload;
        if (!payload?.answer) return openJournal();
        const stratLetter = mapTabToJournalStrategy(state.activeTab);
        openJournal({
          strategy: stratLetter,
          rationale: `${payload.answer?.thesis || ''}\nSetup: ${payload.answer?.setup || ''}\nNiveluri: ${payload.answer?.levels || ''}`
        });
      });

      // Mobile menu
      btnMenu?.addEventListener('click', () => {
        mobileActions.classList.toggle('hidden');
      });

      // Brief modal
      function openBrief() {
        briefModal.classList.remove('hidden');
        loadBrief();
      }
      function closeBrief() {
        briefModal.classList.add('hidden');
      }
      document.querySelectorAll('[data-close-brief]').forEach(b => b.addEventListener('click', closeBrief));
      btnBrief?.addEventListener('click', openBrief);
      mBtnBrief?.addEventListener('click', openBrief);

      async function loadBrief() {
        // skeletons are already present
        try {
          const res = await fetch('/api/brief');
          if (!res.ok) throw new Error('net');
          const data = await res.json();
          state.brief = data;

          // Macro stance
          macroStance.outerHTML = stanceBadge(data?.macro?.stance || '—');
          // Notes
          macroNotes.innerHTML = '';
          (data?.macro?.notes || []).forEach((n, idx) => {
            const row = document.createElement('div');
            row.className = 'flex items-start gap-2 rounded-lg border bg-white px-2 py-2 mb-2';
            row.innerHTML = `
              <span class="text-xs text-gray-500">[${idx+1}]</span>
              <div class="flex-1 text-sm">${n?.text || ''}</div>
              <a href="${n?.citation?.url || '#'}" target="_blank" rel="noopener" class="ml-2 text-xs inline-flex items-center gap-1 px-2 py-1 rounded-md border bg-gray-50 hover:bg-gray-100">
                <i data-lucide="external-link" class="w-3.5 h-3.5"></i> Deschide pasaj
              </a>
            `;
            macroNotes.appendChild(row);
          });

          // Ideas per strategy (Top 3)
          ideasWrap.innerHTML = '';
          const groups = [
            { key: 'EQ_INV', title: 'EQ-INV' },
            { key: 'EQ_MOM', title: 'EQ-MOM/PEAD' },
            { key: 'OPT_INCOME', title: 'OPT-INCOME' }
          ];
          groups.forEach(g => {
            const arr = data?.ideas?.[g.key] || [];
            const box = document.createElement('div');
            box.className = 'rounded-xl border bg-white p-3';
            box.innerHTML = `
              <div class="flex items-center justify-between mb-2">
                <div class="text-sm font-semibold">${g.title}</div>
                <span class="text-xs text-gray-500">${Math.min(3, arr.length)} idei</span>
              </div>
              <div class="space-y-2" id="ideas_${g.key}"></div>
            `;
            ideasWrap.appendChild(box);
            const wrap = box.querySelector(`#ideas_${g.key}`);
            arr.slice(0,3).forEach((idea, idx) => {
              const cits = idea?.citations || [];
              const row = document.createElement('div');
              row.className = 'rounded-lg border bg-gray-50 px-2 py-2';
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
                </div>
              `;
              wrap.appendChild(row);
            });
          });

          // Calendar
          calendarWrap.innerHTML = '';
          (data?.calendar || []).forEach(ev => {
            const card = document.createElement('div');
            card.className = 'rounded-lg border bg-white px-3 py-2';
            card.innerHTML = `
              <div class="flex items-center justify-between">
                <div class="text-sm font-medium">${ev?.title || ''}</div>
                <span class="text-xs text-gray-500">${ev?.time || ''}</span>
              </div>
              <div class="mt-1 text-xs text-gray-600">${ev?.type || ''}${ev?.symbol ? ' • ' + ev.symbol : ''}</div>
            `;
            calendarWrap.appendChild(card);
          });

          mountIcons();

          // Open idea -> switch tab and ask
          ideasWrap.querySelectorAll('.open-idea').forEach(btn => {
            btn.addEventListener('click', (e) => {
              const stratKey = e.currentTarget.getAttribute('data-strat');
              const tab = stratKey === 'EQ_INV' ? 'EQ_INV' : (stratKey === 'EQ_MOM' ? 'EQ_MOM_PEAD' : 'OPT_INCOME');
              setActiveTab(tab);
              closeBrief();
              const ideaText = e.currentTarget.closest('.rounded-lg').querySelector('.text-sm').textContent;
              questionInput.value = ideaText.replace(/\s\[(\d+)\]+$/,'').trim();
              askAnswer(questionInput.value);
              window.scrollTo({ top: 0, behavior: 'smooth' });
            });
          });
        } catch (e) {
          // graceful fallback
          macroNotes.innerHTML = `<div class="text-sm text-rose-700 bg-rose-50 border border-rose-200 px-2 py-1 rounded-md inline-flex items-center gap-2"><i data-lucide="circle-alert" class="w-4 h-4"></i>Eroare la încărcarea Daily Brief.</div>`;
          ideasWrap.innerHTML = '';
          calendarWrap.innerHTML = '';
          mountIcons();
        }
      }
      refreshBrief?.addEventListener('click', loadBrief);

      // Journal modal
      function openJournal(prefill) {
        journalModal.classList.remove('hidden');
        // prefill
        if (prefill?.strategy) jf_strategy.value = prefill.strategy;
        if (prefill?.rationale) jf_rationale.value = prefill.rationale;
        if (!jf_timestamp.value) jf_timestamp.value = new Date().toISOString().slice(0,16);
        loadJournal();
      }
      function closeJournal() {
        journalModal.classList.add('hidden');
      }
      document.querySelectorAll('[data-close-journal]').forEach(b => b.addEventListener('click', closeJournal));
      btnJournal?.addEventListener('click', () => openJournal());
      mBtnJournal?.addEventListener('click', () => openJournal());

      async function loadJournal() {
        try {
          const res = await fetch('/api/journal');
          if (!res.ok) throw new Error('net');
          const data = await res.json();
          state.journal = Array.isArray(data) ? data : (Array.isArray(data?.list) ? data.list : []);
          renderJournalList();
        } catch (e) {
          journalList.innerHTML = `<div class="text-sm text-rose-700 bg-rose-50 border border-rose-200 px-2 py-1 rounded-md inline-flex items-center gap-2"><i data-lucide="circle-alert" class="w-4 h-4"></i>Eroare la încărcarea jurnalului.</div>`;
          mountIcons();
        }
      }

      function renderJournalList() {
        if (!state.journal.length) {
          journalList.innerHTML = `<div class="text-xs text-gray-500">Nu există intrări încă.</div>`;
          return;
        }
        journalList.innerHTML = '';
        state.journal.slice(0, 50).reverse().forEach(item => {
          const row = document.createElement('div');
          row.className = 'rounded-lg border bg-white px-3 py-2';
          const rr = item?.rr ?? '—';
          const pnl = item?.pnl ?? '—';
          const status = item?.status ?? 'open';
          const ansId = item?.answer_id;
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
            </div>
          `;
          const btn = row.querySelector('.see-answer');
          btn?.addEventListener('click', () => {
            if (!ansId) return;
            // Open answer tab: we only have question-based endpoint; fallback: bring user to tab and let them query manually
            setActiveTab(mapJournalStrategyToTab(item.strategy || 'A'));
            closeJournal();
            window.scrollTo({ top: 0, behavior: 'smooth' });
          });
          journalList.appendChild(row);
        });
        mountIcons();
      }

      function validateSoft() {
        const dir = jf_direction.value;
        const entry = parseFloat(jf_entry.value);
        const stop = parseFloat(jf_stop.value);
        const tp = parseFloat(jf_tp.value);
        let warn = false;
        if (!isNaN(entry) && !isNaN(stop)) {
          if (dir === 'long' && stop >= entry) warn = true;
          if (dir === 'short' && stop <= entry) warn = true;
        }
        if (!isNaN(entry) && !isNaN(tp)) {
          if (dir === 'long' && tp <= entry) warn = true;
          if (dir === 'short' && tp >= entry) warn = true;
        }
        softWarn.classList.toggle('hidden', !warn);
        riskHint.classList.toggle('hidden', !warn);
      }
      [jf_direction, jf_entry, jf_stop, jf_tp, jf_size].forEach(el => el.addEventListener('input', validateSoft));

      journalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
          timestamp: jf_timestamp.value,
          strategy: jf_strategy.value,
          symbol: jf_symbol.value,
          direction: jf_direction.value,
          entry: jf_entry.value ? Number(jf_entry.value) : null,
          size: jf_size.value ? Number(jf_size.value) : null,
          stop: jf_stop.value ? Number(jf_stop.value) : null,
          tp: jf_tp.value ? Number(jf_tp.value) : null,
          rationale: jf_rationale.value,
          tags: jf_tags.value
        };
        validateSoft();
        try {
          const res = await fetch('/api/journal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          if (!res.ok) throw new Error('net');
          await loadJournal();
          jf_reset.click();
        } catch (e2) {
          // no block, graceful
        }
      });
      jf_reset.addEventListener('click', () => {
        journalForm.reset();
        jf_timestamp.value = new Date().toISOString().slice(0,16);
        softWarn.classList.add('hidden');
        riskHint.classList.add('hidden');
      });

      // Export CSV
      exportCSVBtn.addEventListener('click', () => {
        const rows = state.journal.map(j => ({
          timestamp: j.timestamp ?? '',
          strategy: j.strategy ?? '',
          symbol: j.symbol ?? '',
          direction: j.direction ?? '',
          entry: j.entry ?? '',
          size: j.size ?? '',
          stop: j.stop ?? '',
          tp: j.tp ?? '',
          rationale: (j.rationale ?? '').toString().replace(/\n/g, ' ').replace(/"/g, '""'),
          tags: (j.tags ?? '').toString().replace(/"/g, '""')
        }));
        const header = 'timestamp,strategy,symbol,direction,entry,size,stop,tp,rationale,tags';
        const csv = [header].concat(rows.map(r => [
          r.timestamp, r.strategy, r.symbol, r.direction, r.entry, r.size, r.stop, r.tp, `"${r.rationale}"`, `"${r.tags}"`
        ].join(','))).join('\n');
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `journal_export_${new Date().toISOString().slice(0,10)}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      });

      // Upload modal
      function openUpload() { uploadModal.classList.remove('hidden'); }
      function closeUpload() { uploadModal.classList.add('hidden'); }
      document.querySelectorAll('[data-close-upload]').forEach(b => b.addEventListener('click', closeUpload));
      btnUpload?.addEventListener('click', openUpload);
      mBtnUpload?.addEventListener('click', openUpload);

      // Dropzone
      let filesQueue = [];
      function renderUploads(list) {
        if (!list.length) {
          uploadList.innerHTML = `<div class="text-xs text-gray-400">Niciun fișier încă.</div>`;
          return;
        }
        uploadList.innerHTML = '';
        list.forEach(f => {
          const row = document.createElement('div');
          row.className = 'flex items-center justify-between rounded-lg border bg-white px-3 py-2 text-sm';
          const right = document.createElement('div');
          right.className = 'flex items-center gap-2';
          const status = document.createElement('span');
          status.className = 'text-xs px-2 py-0.5 rounded-md border';
          if (f.status === 'accepted') status.className += ' bg-emerald-50 border-emerald-200 text-emerald-700';
          else if (f.status === 'dedup') status.className += ' bg-amber-50 border-amber-200 text-amber-700';
          else if (f.status === 'rejected') status.className += ' bg-rose-50 border-rose-200 text-rose-700';
          status.textContent = f.status || 'pending';
          const reason = document.createElement('span');
          reason.className = 'text-xs text-gray-500';
          reason.textContent = f</script></body></html>