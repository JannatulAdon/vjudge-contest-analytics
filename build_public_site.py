import json
import os
import copy

def build_public_site():
    with open('problems_database.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Sanitize dataset: completely remove all passwords for public deployment
    public_data = copy.deepcopy(data)
    
    for c in public_data.get('contests', []):
        if 'password' in c:
            del c['password']
            
    for p in public_data.get('problems', []):
        if 'contest_password' in p:
            del p['contest_password']

    db_json_str = json.dumps(public_data, ensure_ascii=False)

    html_content = f'''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VJudge Contest & Problem Analytics Hub</title>
  
  <!-- SEO & Social Meta Tags -->
  <meta name="description" content="Interactive archive and analytics of 105 competitive programming contests and 1,317 problems mapped to Codeforces difficulty ratings with topic breakdowns.">
  <meta property="og:title" content="VJudge Contest & Problem Analytics Hub">
  <meta property="og:description" content="Explore 105 contests, 1,317 problems, topic distributions, and Codeforces difficulty ratings with interactive filtering and sorting.">
  <meta property="og:type" content="website">

  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- FontAwesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#f0fdf4',
              500: '#22c55e',
              600: '#16a34a',
              700: '#15803d',
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    body {{
      font-family: 'Inter', sans-serif;
    }}
    .mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    ::-webkit-scrollbar {{
      width: 8px;
      height: 8px;
    }}
    ::-webkit-scrollbar-track {{
      background: #0f172a;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #334155;
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #475569;
    }}
    .sortable-th {{
      cursor: pointer;
      user-select: none;
      transition: all 0.15s ease;
    }}
    .sortable-th:hover {{
      background-color: rgba(51, 65, 85, 0.5);
      color: #ffffff;
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col transition-colors duration-200">

  <!-- Top Navigation Header -->
  <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 via-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-brand-500/20">
          <i class="fa-solid fa-trophy text-white text-lg"></i>
        </div>
        <div>
          <h1 class="font-bold text-lg leading-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
            VJudge Analytics Hub
          </h1>
          <p class="text-xs text-slate-400">105 Contests • 1,317 CP Problems • Codeforces Scaled</p>
        </div>
      </div>
      
      <div class="flex items-center space-x-2 sm:space-x-3">
        <button id="btnAbout" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs font-medium flex items-center space-x-1.5 transition">
          <i class="fa-solid fa-circle-info text-blue-400"></i>
          <span>About</span>
        </button>

        <!-- Export Dropdown -->
        <div class="relative group">
          <button class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium flex items-center space-x-1.5 transition border border-slate-700">
            <i class="fa-solid fa-download text-emerald-400"></i>
            <span>Export</span>
            <i class="fa-solid fa-chevron-down text-[10px] text-slate-400"></i>
          </button>
          <div class="absolute right-0 mt-1 w-48 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl py-1 hidden group-hover:block z-50">
            <button id="btnExportContestsCsv" class="w-full text-left px-3 py-2 text-xs text-slate-300 hover:bg-slate-800 hover:text-white flex items-center space-x-2">
              <i class="fa-solid fa-file-csv text-indigo-400"></i>
              <span>Contests (CSV)</span>
            </button>
            <button id="btnExportProblemsCsv" class="w-full text-left px-3 py-2 text-xs text-slate-300 hover:bg-slate-800 hover:text-white flex items-center space-x-2">
              <i class="fa-solid fa-file-csv text-emerald-400"></i>
              <span>Problems (CSV)</span>
            </button>
            <button id="btnExportJson" class="w-full text-left px-3 py-2 text-xs text-slate-300 hover:bg-slate-800 hover:text-white flex items-center space-x-2">
              <i class="fa-solid fa-code text-amber-400"></i>
              <span>Full Data (JSON)</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- Main Content Layout -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">

    <!-- Filters Panel -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
        <div class="flex items-center space-x-2">
          <i class="fa-solid fa-sliders text-brand-500 text-sm"></i>
          <h2 class="font-semibold text-sm uppercase tracking-wider text-slate-300">Filters & Timeframes</h2>
        </div>
        <!-- Time Presets -->
        <div class="flex flex-wrap items-center gap-1.5" id="timePresets">
          <button data-days="0" class="time-btn active px-3 py-1 rounded-full text-xs font-medium bg-brand-600 text-white shadow-sm">All Time</button>
          <button data-year="2026" class="time-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300">2026</button>
          <button data-year="2024" class="time-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300">2024</button>
          <button data-year="2023" class="time-btn px-3 py-1 rounded-full text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300">2023</button>
        </div>
      </div>

      <!-- Filter Row 1 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        <!-- Search -->
        <div class="relative lg:col-span-2">
          <label class="block text-xs font-medium text-slate-400 mb-1">Search Keywords</label>
          <div class="relative">
            <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-slate-500 text-xs"></i>
            <input type="text" id="searchInput" placeholder="Search contest, problem title, code, tag..." 
              class="w-full pl-8 pr-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 focus:border-brand-500 focus:ring-1 focus:ring-brand-500 text-xs text-white placeholder-slate-500 transition">
          </div>
        </div>

        <!-- Contest Type -->
        <div>
          <label class="block text-xs font-medium text-slate-400 mb-1">Contest Type</label>
          <select id="contestTypeSelect" class="w-full px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-white focus:border-brand-500 transition">
            <option value="ALL">All Types</option>
            <option value="Team Forming">Team Forming (44)</option>
            <option value="Team Practice">Team Practice (26)</option>
            <option value="Weekly Contest">Weekly Contest (18)</option>
            <option value="Beginner Contest">Beginner Contest (10)</option>
            <option value="Topic Contest">Topic Contest (5)</option>
            <option value="Girls Contest">Girls Contest (1)</option>
            <option value="Special / Practice">Special / Practice (1)</option>
          </select>
        </div>

        <!-- Category -->
        <div>
          <label class="block text-xs font-medium text-slate-400 mb-1">Topic Category</label>
          <select id="categorySelect" class="w-full px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-white focus:border-brand-500 transition">
            <option value="ALL">All Topics</option>
            <option value="Dynamic Programming">Dynamic Programming</option>
            <option value="Graphs">Graphs</option>
            <option value="Trees">Trees</option>
            <option value="Math & Number Theory">Math & Number Theory</option>
            <option value="Data Structures">Data Structures</option>
            <option value="Greedy">Greedy</option>
            <option value="Geometry">Geometry</option>
            <option value="Strings">Strings</option>
            <option value="Binary Search & Two Pointers">Binary Search & Two Pointers</option>
            <option value="Games & Constructive">Games & Constructive</option>
            <option value="Implementation">Implementation</option>
          </select>
        </div>

        <!-- Difficulty Tier -->
        <div>
          <label class="block text-xs font-medium text-slate-400 mb-1">CF Difficulty</label>
          <select id="difficultySelect" class="w-full px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-white focus:border-brand-500 transition">
            <option value="ALL">All Difficulties</option>
            <option value="Easy">Easy (&lt; 1200)</option>
            <option value="Medium">Medium (1200 – 1599)</option>
            <option value="Hard">Hard (1600 – 1999)</option>
            <option value="Expert">Expert (2000+)</option>
          </select>
        </div>
      </div>

      <!-- Custom Date Inputs -->
      <div class="flex flex-wrap items-center justify-between text-xs text-slate-400 gap-3 pt-1 border-t border-slate-800/60">
        <div class="flex items-center space-x-2">
          <span>Date Range:</span>
          <input type="date" id="dateStart" class="bg-slate-800 border border-slate-700 px-2 py-1 rounded text-white text-xs">
          <span>to</span>
          <input type="date" id="dateEnd" class="bg-slate-800 border border-slate-700 px-2 py-1 rounded text-white text-xs">
          <button id="btnApplyCustomDate" class="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-white font-medium">Apply</button>
        </div>

        <button id="btnResetFilters" class="text-xs text-slate-400 hover:text-white flex items-center space-x-1.5">
          <i class="fa-solid fa-rotate-left"></i>
          <span>Reset Filters</span>
        </button>
      </div>
    </div>

    <!-- KPI Metric Cards (Public Focus) -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
        <span class="text-xs text-slate-400 font-medium">Contests Selected</span>
        <div class="flex items-baseline justify-between mt-2">
          <span id="kpiContests" class="text-2xl font-bold text-indigo-400 mono">0</span>
          <span class="text-xs text-slate-500">/ 105</span>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
        <span class="text-xs text-slate-400 font-medium">Problems In Scope</span>
        <div class="flex items-baseline justify-between mt-2">
          <span id="kpiProblems" class="text-2xl font-bold text-white mono">0</span>
          <span class="text-xs text-slate-500">/ 1,317</span>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
        <span class="text-xs text-slate-400 font-medium">Avg CF Difficulty</span>
        <div class="flex items-baseline justify-between mt-2">
          <span id="kpiAvgRating" class="text-2xl font-bold text-amber-400 mono">0</span>
          <span id="kpiAvgTier" class="text-xs px-2 py-0.5 rounded bg-amber-400/10 text-amber-400 font-medium">Medium</span>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
        <span class="text-xs text-slate-400 font-medium">Hardest Problem</span>
        <div class="flex items-baseline justify-between mt-2">
          <span id="kpiMaxRating" class="text-2xl font-bold text-rose-400 mono">3164</span>
          <span class="text-xs px-2 py-0.5 rounded bg-rose-400/10 text-rose-400 font-medium">Grandmaster</span>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col justify-between col-span-2 sm:col-span-1">
        <span class="text-xs text-slate-400 font-medium">Top Topic</span>
        <div class="flex items-baseline justify-between mt-2">
          <span id="kpiTopCategory" class="text-base font-bold text-purple-400 truncate">None</span>
          <span id="kpiTopCatCount" class="text-xs text-slate-500 mono">0</span>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Category Chart -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-2">
            <i class="fa-solid fa-chart-pie text-brand-500 text-sm"></i>
            <h3 class="font-semibold text-sm text-slate-200">Problem Categories Breakdown</h3>
          </div>
        </div>
        <div class="relative flex-1 min-h-[280px] flex items-center justify-center">
          <canvas id="categoryChart"></canvas>
        </div>
      </div>

      <!-- Difficulty Rating Histogram -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-2">
            <i class="fa-solid fa-chart-simple text-amber-500 text-sm"></i>
            <h3 class="font-semibold text-sm text-slate-200">Codeforces Difficulty Rating Distribution</h3>
          </div>
        </div>
        <div class="relative flex-1 min-h-[280px]">
          <canvas id="ratingChart"></canvas>
        </div>
      </div>

      <!-- Activity Timeline -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col lg:col-span-2">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-2">
            <i class="fa-solid fa-calendar-days text-indigo-400 text-sm"></i>
            <h3 class="font-semibold text-sm text-slate-200">Contest & Problem Volume Timeline by Month</h3>
          </div>
        </div>
        <div class="relative h-[250px]">
          <canvas id="timelineChart"></canvas>
        </div>
      </div>
    </div>

    <!-- EXPLORER SECTION: CONTESTS FIRST (DEFAULT) THEN PROBLEMS -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl shadow-xl overflow-hidden">
      <!-- Tab Header Bar: Contests First! -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800 px-5 pt-4 pb-0 bg-slate-900/90 gap-4">
        <!-- Tabs -->
        <div class="flex items-center space-x-2">
          <!-- Primary Tab: Contest Explorer -->
          <button id="tabContestsBtn" class="tab-btn px-4 py-2.5 rounded-t-xl text-xs font-semibold flex items-center space-x-2 border-b-2 border-indigo-500 text-indigo-400 bg-slate-800/80 transition">
            <i class="fa-solid fa-trophy"></i>
            <span>Contest Explorer</span>
            <span id="tabBadgeContests" class="px-2 py-0.5 rounded-full text-[10px] bg-indigo-500/20 text-indigo-300 font-mono">105</span>
          </button>

          <!-- Secondary Tab: Problem Explorer -->
          <button id="tabProblemsBtn" class="tab-btn px-4 py-2.5 rounded-t-xl text-xs font-medium flex items-center space-x-2 border-b-2 border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition">
            <i class="fa-solid fa-list-check"></i>
            <span>Individual Problems</span>
            <span id="tabBadgeProblems" class="px-2 py-0.5 rounded-full text-[10px] bg-slate-800 text-slate-400 font-mono">1,317</span>
          </button>
        </div>

        <!-- Tab Context Controls -->
        <div class="flex items-center space-x-3 pb-3 sm:pb-0 text-xs">
          <!-- Contest View Specific Controls -->
          <div id="contestControls" class="flex items-center space-x-2">
            <button id="btnExpandAllContests" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition flex items-center space-x-1">
              <i class="fa-solid fa-angles-down text-[10px]"></i>
              <span>Expand All</span>
            </button>
            <button id="btnCollapseAllContests" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition flex items-center space-x-1">
              <i class="fa-solid fa-angles-up text-[10px]"></i>
              <span>Collapse All</span>
            </button>
          </div>

          <div class="flex items-center space-x-1.5 text-slate-400">
            <span>Per page:</span>
            <select id="pageSizeSelect" class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-white text-xs">
              <option value="15">15</option>
              <option value="25" selected>25</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>
        </div>
      </div>

      <!-- VIEW 1: CONTESTS EXPLORER (DEFAULT ACTIVE) -->
      <div id="viewContests" class="p-5 space-y-4">
        <div class="flex items-center justify-between text-xs text-slate-400">
          <p><i class="fa-solid fa-arrow-down-up-across-line text-indigo-400 mr-1"></i> Contests catalog with difficulty metrics and expandable problem lists. Click any header with <span class="text-slate-300 font-medium">⇅</span> to sort.</p>
          <div class="text-xs text-slate-400">Click any contest row or <span class="text-indigo-400 font-semibold">View Problems</span> to expand.</div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs text-slate-300">
            <thead class="bg-slate-800/80 uppercase tracking-wider text-slate-400 font-semibold border-b border-slate-700">
              <tr>
                <th class="sortable-contest-th py-3 px-3 text-center w-12" data-col="contest_index">
                  <div class="flex items-center justify-center space-x-1">
                    <span>#</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_contest_index"></i>
                  </div>
                </th>
                <th class="sortable-contest-th py-3 px-3" data-col="date">
                  <div class="flex items-center space-x-1">
                    <span>Date</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_date"></i>
                  </div>
                </th>
                <th class="sortable-contest-th py-3 px-3" data-col="title">
                  <div class="flex items-center space-x-1">
                    <span>Contest Title</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_title"></i>
                  </div>
                </th>
                <th class="sortable-contest-th py-3 px-3" data-col="contest_type">
                  <div class="flex items-center space-x-1">
                    <span>Type</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_contest_type"></i>
                  </div>
                </th>
                <th class="sortable-contest-th py-3 px-2 text-center" data-col="problem_count">
                  <div class="flex items-center justify-center space-x-1">
                    <span>Problems</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_problem_count"></i>
                  </div>
                </th>
                <th class="sortable-contest-th py-3 px-3 text-center" data-col="avg_cf_rating">
                  <div class="flex items-center justify-center space-x-1">
                    <span>Avg Difficulty</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_avg_cf_rating"></i>
                  </div>
                </th>
                <th class="py-3 px-3">Top Topics</th>
                <th class="py-3 px-3 text-center">Action</th>
              </tr>
            </thead>
            <tbody id="contestsTableBody" class="divide-y divide-slate-800/60 font-normal">
              <!-- Rendered dynamically -->
            </tbody>
          </table>
        </div>

        <!-- Contests Pagination -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-2 text-xs text-slate-400">
          <div id="contestPageInfo">Showing 1 to 25 of 105 contests</div>
          <div class="flex items-center space-x-1" id="contestPaginationControls">
            <!-- Rendered dynamically -->
          </div>
        </div>
      </div>

      <!-- VIEW 2: PROBLEMS EXPLORER (SECONDARY) -->
      <div id="viewProblems" class="p-5 space-y-4 hidden">
        <div class="flex items-center justify-between text-xs text-slate-400">
          <p><i class="fa-solid fa-arrow-down-up-across-line text-brand-400 mr-1"></i> Individual problem catalog across all contests. Click headers to sort by difficulty, topic, or date.</p>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs text-slate-300">
            <thead class="bg-slate-800/80 uppercase tracking-wider text-slate-400 font-semibold border-b border-slate-700">
              <tr>
                <th class="sortable-th py-3 px-3" data-col="contest_date">
                  <div class="flex items-center space-x-1">
                    <span>Date</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_icon_contest_date"></i>
                  </div>
                </th>
                <th class="sortable-th py-3 px-3" data-col="contest_title">
                  <div class="flex items-center space-x-1">
                    <span>Contest</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_icon_contest_title"></i>
                  </div>
                </th>
                <th class="sortable-th py-3 px-2" data-col="contest_type">
                  <div class="flex items-center space-x-1">
                    <span>Type</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_icon_contest_type"></i>
                  </div>
                </th>
                <th class="sortable-th py-3 px-2 text-center" data-col="problem_letter">
                  <div class="flex items-center justify-center space-x-1">
                    <span>#</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_icon_problem_letter"></i>
                  </div>
                </th>
                <th class="sortable-th py-3 px-3" data-col="problem_title">
                  <div class="flex items-center space-x-1">
                    <span>Problem Title</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_icon_problem_title"></i>
                  </div>
                </th>
                <th class="sortable-th py-3 px-2" data-col="oj_prob_code">
                  <div class="flex items-center space-x-1">
                    <span>OJ Code</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_icon_oj_prob_code"></i>
                  </div>
                </th>
                <th class="sortable-th py-3 px-3" data-col="primary_category">
                  <div class="flex items-center space-x-1">
                    <span>Topic</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_icon_primary_category"></i>
                  </div>
                </th>
                <th class="sortable-th py-3 px-3 text-center" data-col="cf_rating">
                  <div class="flex items-center justify-center space-x-1">
                    <span>CF Rating</span>
                    <i class="fa-solid fa-sort text-slate-500" id="sort_icon_cf_rating"></i>
                  </div>
                </th>
                <th class="py-3 px-2 text-center">Solve</th>
              </tr>
            </thead>
            <tbody id="problemsTableBody" class="divide-y divide-slate-800/60 font-normal">
              <!-- Rendered dynamically -->
            </tbody>
          </table>
        </div>

        <!-- Problems Pagination -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-2 text-xs text-slate-400">
          <div id="pageInfo">Showing 1 to 25 of 1,317 problems</div>
          <div class="flex items-center space-x-1" id="paginationControls">
            <!-- Rendered dynamically -->
          </div>
        </div>
      </div>
    </div>
  </main>

  <!-- Page Footer -->
  <footer class="border-t border-slate-800/80 py-6 mt-12 bg-slate-900/40 text-center text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
      <p>VJudge Contest & Problem Analytics Hub • 105 Contests • 1,317 Problems</p>
      <div class="flex items-center space-x-4">
        <a href="#about" id="footerAboutLink" class="text-indigo-400 hover:text-indigo-300 transition flex items-center space-x-1">
          <i class="fa-solid fa-circle-question"></i>
          <span>About & Methodology</span>
        </a>
        <a href="https://github.com/JannatulAdon/vjudge-contest-analytics" target="_blank" class="hover:text-slate-300 transition flex items-center space-x-1">
          <i class="fa-brands fa-github"></i>
          <span>GitHub</span>
        </a>
      </div>
    </div>
  </footer>

  <!-- About & Methodology Modal -->
  <div id="aboutModal" class="fixed inset-0 bg-black/75 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-xl w-full p-6 shadow-2xl space-y-4">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center space-x-2.5">
          <div class="w-8 h-8 rounded-lg bg-indigo-600/20 text-indigo-400 flex items-center justify-center">
            <i class="fa-solid fa-circle-info text-sm"></i>
          </div>
          <div>
            <h3 class="font-bold text-white text-base">About & Methodology</h3>
            <p class="text-[11px] text-slate-400">Dataset Context & Calibration</p>
          </div>
        </div>
        <button id="btnCloseAboutModal" class="text-slate-400 hover:text-white transition">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>

      <div class="space-y-3 text-xs text-slate-300 leading-relaxed">
        <div class="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80 space-y-1">
          <div class="font-semibold text-white flex items-center space-x-1.5">
            <i class="fa-solid fa-database text-brand-400"></i>
            <span>What is this?</span>
          </div>
          <p class="text-slate-400 text-[11px]">
            A comprehensive practice archive of <strong>105 contests</strong> and <strong>1,317 problems</strong> hosted on Virtual Judge (2022–2026), covering Team Forming, Team Practice, and Weekly contests.
          </p>
        </div>

        <div class="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80 space-y-1">
          <div class="font-semibold text-white flex items-center space-x-1.5">
            <i class="fa-solid fa-scale-balanced text-amber-400"></i>
            <span>How are Codeforces ratings determined?</span>
          </div>
          <ul class="text-slate-400 text-[11px] space-y-1 list-disc list-inside">
            <li><strong>Codeforces:</strong> Official contest problem ratings (800 – 3500+).</li>
            <li><strong>AtCoder:</strong> Converted from Kenkoooo difficulty models onto the CF scale.</li>
            <li><strong>Gym, CSES & Others:</strong> Calibrated by contest division tier and letter index (Div.2 A/B ≈ 800–1200, C/D ≈ 1300–1700, E/F ≈ 1800–2400).</li>
          </ul>
        </div>

        <div class="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80 space-y-1">
          <div class="font-semibold text-white flex items-center space-x-1.5">
            <i class="fa-solid fa-tags text-indigo-400"></i>
            <span>Topic Classification</span>
          </div>
          <p class="text-slate-400 text-[11px]">
            Tagged hierarchically by algorithmic technique: <em>Dynamic Programming &gt; Trees &gt; Graphs &gt; Math &amp; Number Theory &gt; Geometry &gt; Data Structures &gt; Greedy &gt; Implementation</em>.
          </p>
        </div>
      </div>

      <div class="flex items-center justify-between pt-2 border-t border-slate-800 text-xs">
        <span class="text-slate-500 text-[11px]">Direct links open contests & problems on VJudge</span>
        <button id="btnDismissAboutModal" class="px-4 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs transition">
          Got it
        </button>
      </div>
    </div>
  </div>

  <!-- Toast Notification -->
  <div id="toast" class="fixed bottom-6 right-6 bg-slate-900 border border-slate-700 text-white px-4 py-2.5 rounded-xl shadow-2xl text-xs font-medium flex items-center space-x-2 z-50 transform translate-y-20 opacity-0 transition-all duration-300">
    <i class="fa-solid fa-circle-check text-brand-400 text-sm"></i>
    <span id="toastMsg">Notification</span>
  </div>

  <!-- Embedded Sanitized Dataset & Script -->
  <script>
    const DATASET = {db_json_str};
    const ALL_PROBLEMS = DATASET.problems;
    const ALL_CONTESTS = DATASET.contests;

    // State
    let filteredProblems = [...ALL_PROBLEMS];
    let filteredContests = [...ALL_CONTESTS];
    let activeTab = 'contests'; // Default to contests first!

    // Sorting State
    let probSortCol = 'contest_date';
    let probSortAsc = false;
    let contestSortCol = 'contest_index';
    let contestSortAsc = false;

    // Pagination State
    let probPage = 1;
    let probPageSize = 25;
    let contestPage = 1;
    let contestPageSize = 25;

    // Expanded Contests Set
    const expandedContestIds = new Set();

    // Charts
    let categoryChart = null;
    let ratingChart = null;
    let timelineChart = null;

    const latestDate = new Date(DATASET.metadata.latest_date || '2026-09-26');

    // Init
    document.addEventListener('DOMContentLoaded', () => {{
      initDateInputs();
      setupEventListeners();
      applyFilters();
    }});

    function initDateInputs() {{
      const startEl = document.getElementById('dateStart');
      const endEl = document.getElementById('dateEnd');
      startEl.value = DATASET.metadata.earliest_date || '2022-12-29';
      endEl.value = DATASET.metadata.latest_date || '2026-09-26';
    }}

    function showToast(msg) {{
      const toast = document.getElementById('toast');
      const toastMsg = document.getElementById('toastMsg');
      toastMsg.textContent = msg;
      toast.classList.remove('translate-y-20', 'opacity-0');
      toast.classList.add('translate-y-0', 'opacity-100');
      setTimeout(() => {{
        toast.classList.remove('translate-y-0', 'opacity-100');
        toast.classList.add('translate-y-20', 'opacity-0');
      }}, 2200);
    }}

    function copyToClipboard(text, successMsg) {{
      navigator.clipboard.writeText(text).then(() => {{
        showToast(successMsg || 'Copied to clipboard!');
      }}).catch(() => {{
        showToast('Failed to copy');
      }});
    }}

    function setupEventListeners() {{
      // Tabs
      document.getElementById('tabContestsBtn').addEventListener('click', () => switchTab('contests'));
      document.getElementById('tabProblemsBtn').addEventListener('click', () => switchTab('problems'));

      // Filter Inputs
      document.getElementById('searchInput').addEventListener('input', applyFilters);
      document.getElementById('contestTypeSelect').addEventListener('change', applyFilters);
      document.getElementById('categorySelect').addEventListener('change', applyFilters);
      document.getElementById('difficultySelect').addEventListener('change', applyFilters);

      document.getElementById('pageSizeSelect').addEventListener('change', (e) => {{
        const sz = parseInt(e.target.value, 10);
        if (activeTab === 'contests') {{
          contestPageSize = sz;
          contestPage = 1;
          renderContestsTable();
        }} else {{
          probPageSize = sz;
          probPage = 1;
          renderProblemsTable();
        }}
      }});

      // Time presets
      document.getElementById('timePresets').addEventListener('click', (e) => {{
        const btn = e.target.closest('.time-btn');
        if (!btn) return;
        document.querySelectorAll('.time-btn').forEach(b => {{
          b.classList.remove('bg-brand-600', 'text-white');
          b.classList.add('bg-slate-800', 'text-slate-300');
        }});
        btn.classList.add('bg-brand-600', 'text-white');
        btn.classList.remove('bg-slate-800', 'text-slate-300');

        const days = btn.dataset.days;
        const year = btn.dataset.year;
        const endEl = document.getElementById('dateEnd');
        const startEl = document.getElementById('dateStart');

        if (days === '0') {{
          startEl.value = DATASET.metadata.earliest_date;
          endEl.value = DATASET.metadata.latest_date;
        }} else if (days) {{
          const d = parseInt(days, 10);
          const endD = new Date(latestDate);
          const startD = new Date(latestDate);
          startD.setDate(startD.getDate() - d);
          startEl.value = startD.toISOString().slice(0, 10);
          endEl.value = endD.toISOString().slice(0, 10);
        }} else if (year) {{
          startEl.value = year + '-01-01';
          endEl.value = year + '-12-31';
        }}
        applyFilters();
      }});

      // Custom date apply
      document.getElementById('btnApplyCustomDate').addEventListener('click', () => {{
        document.querySelectorAll('.time-btn').forEach(b => {{
          b.classList.remove('bg-brand-600', 'text-white');
          b.classList.add('bg-slate-800', 'text-slate-300');
        }});
        applyFilters();
      }});

      // Reset
      document.getElementById('btnResetFilters').addEventListener('click', () => {{
        document.getElementById('searchInput').value = '';
        document.getElementById('contestTypeSelect').value = 'ALL';
        document.getElementById('categorySelect').value = 'ALL';
        document.getElementById('difficultySelect').value = 'ALL';
        initDateInputs();
        document.querySelectorAll('.time-btn').forEach((b, idx) => {{
          if (idx === 0) {{
            b.classList.add('bg-brand-600', 'text-white');
            b.classList.remove('bg-slate-800', 'text-slate-300');
          }} else {{
            b.classList.remove('bg-brand-600', 'text-white');
            b.classList.add('bg-slate-800', 'text-slate-300');
          }}
        }});
        applyFilters();
      }});

      // Problem Table Header Sort Handlers
      document.querySelectorAll('.sortable-th').forEach(th => {{
        th.addEventListener('click', () => {{
          const col = th.dataset.col;
          if (probSortCol === col) {{
            probSortAsc = !probSortAsc;
          }} else {{
            probSortCol = col;
            probSortAsc = (col === 'cf_rating' || col === 'contest_date') ? false : true;
          }}
          updateProblemSortIcons();
          sortProblems();
          renderProblemsTable();
        }});
      }});

      // Contest Table Header Sort Handlers
      document.querySelectorAll('.sortable-contest-th').forEach(th => {{
        th.addEventListener('click', () => {{
          const col = th.dataset.col;
          if (contestSortCol === col) {{
            contestSortAsc = !contestSortAsc;
          }} else {{
            contestSortCol = col;
            contestSortAsc = (col === 'avg_cf_rating' || col === 'date' || col === 'problem_count') ? false : true;
          }}
          updateContestSortIcons();
          sortContests();
          renderContestsTable();
        }});
      }});

      // Expand / Collapse all contests
      document.getElementById('btnExpandAllContests').addEventListener('click', () => {{
        filteredContests.forEach(c => expandedContestIds.add(c.contest_id));
        renderContestsTable();
      }});
      document.getElementById('btnCollapseAllContests').addEventListener('click', () => {{
        expandedContestIds.clear();
        renderContestsTable();
      }});

      // About Modal
      const openAbout = () => document.getElementById('aboutModal').classList.remove('hidden');
      const closeAbout = () => {{
        document.getElementById('aboutModal').classList.add('hidden');
        if (window.location.hash === '#about') {{
          history.replaceState(null, null, ' ');
        }}
      }};
      document.getElementById('btnAbout').addEventListener('click', openAbout);
      document.getElementById('footerAboutLink').addEventListener('click', (e) => {{
        e.preventDefault();
        openAbout();
      }});
      document.getElementById('btnCloseAboutModal').addEventListener('click', closeAbout);
      document.getElementById('btnDismissAboutModal').addEventListener('click', closeAbout);
      
      // Auto open if #about in URL or on hashchange
      if (window.location.hash === '#about') {{
        openAbout();
      }}
      window.addEventListener('hashchange', () => {{
        if (window.location.hash === '#about') openAbout();
      }});

      // Exports
      document.getElementById('btnExportProblemsCsv').addEventListener('click', exportFilteredProblemsCsv);
      document.getElementById('btnExportContestsCsv').addEventListener('click', exportFilteredContestsCsv);
      document.getElementById('btnExportJson').addEventListener('click', exportFilteredJson);
    }}

    function switchTab(tab) {{
      activeTab = tab;
      const probBtn = document.getElementById('tabProblemsBtn');
      const contestBtn = document.getElementById('tabContestsBtn');
      const viewProb = document.getElementById('viewProblems');
      const viewContest = document.getElementById('viewContests');
      const contestControls = document.getElementById('contestControls');

      if (tab === 'contests') {{
        contestBtn.className = 'tab-btn px-4 py-2.5 rounded-t-xl text-xs font-semibold flex items-center space-x-2 border-b-2 border-indigo-500 text-indigo-400 bg-slate-800/80 transition';
        probBtn.className = 'tab-btn px-4 py-2.5 rounded-t-xl text-xs font-medium flex items-center space-x-2 border-b-2 border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition';
        viewContest.classList.remove('hidden');
        viewProb.classList.add('hidden');
        contestControls.classList.remove('hidden');
        renderContestsTable();
      }} else {{
        probBtn.className = 'tab-btn px-4 py-2.5 rounded-t-xl text-xs font-semibold flex items-center space-x-2 border-b-2 border-brand-500 text-brand-400 bg-slate-800/80 transition';
        contestBtn.className = 'tab-btn px-4 py-2.5 rounded-t-xl text-xs font-medium flex items-center space-x-2 border-b-2 border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 transition';
        viewProb.classList.remove('hidden');
        viewContest.classList.add('hidden');
        contestControls.classList.add('hidden');
        renderProblemsTable();
      }}
    }}

    function applyFilters() {{
      const query = document.getElementById('searchInput').value.trim().toLowerCase();
      const contestType = document.getElementById('contestTypeSelect').value;
      const category = document.getElementById('categorySelect').value;
      const difficulty = document.getElementById('difficultySelect').value;
      const startDate = document.getElementById('dateStart').value;
      const endDate = document.getElementById('dateEnd').value;

      filteredProblems = ALL_PROBLEMS.filter(p => {{
        if (p.contest_date) {{
          if (startDate && p.contest_date < startDate) return false;
          if (endDate && p.contest_date > endDate) return false;
        }}
        if (contestType !== 'ALL' && p.contest_type !== contestType) return false;
        if (category !== 'ALL' && p.primary_category !== category) return false;
        if (difficulty !== 'ALL' && p.difficulty_level !== difficulty) return false;

        if (query) {{
          const haystack = (
            p.problem_title + ' ' + 
            p.contest_title + ' ' + 
            p.oj + ' ' + 
            p.oj_prob_code + ' ' + 
            p.tags.join(' ')
          ).toLowerCase();
          if (!haystack.includes(query)) return false;
        }}
        return true;
      }});

      const matchingContestIds = new Set(filteredProblems.map(p => p.contest_id));
      filteredContests = ALL_CONTESTS.filter(c => {{
        if (c.date) {{
          if (startDate && c.date < startDate) return false;
          if (endDate && c.date > endDate) return false;
        }}
        if (contestType !== 'ALL' && c.contest_type !== contestType) return false;
        
        if (category !== 'ALL' || difficulty !== 'ALL' || query !== '') {{
          if (!matchingContestIds.has(c.contest_id)) {{
            if (query && c.title.toLowerCase().includes(query)) {{
              return true;
            }}
            return false;
          }}
        }}
        return true;
      }});

      document.getElementById('tabBadgeProblems').textContent = filteredProblems.length.toLocaleString();
      document.getElementById('tabBadgeContests').textContent = filteredContests.length.toLocaleString();

      sortProblems();
      sortContests();

      probPage = 1;
      contestPage = 1;

      updateMetrics();
      updateCharts();
      renderContestsTable();
      renderProblemsTable();
    }}

    function sortProblems() {{
      filteredProblems.sort((a, b) => {{
        let valA = a[probSortCol];
        let valB = b[probSortCol];

        if (typeof valA === 'number' && typeof valB === 'number') {{
          return probSortAsc ? (valA - valB) : (valB - valA);
        }}
        valA = (valA || '').toString();
        valB = (valB || '').toString();
        const cmp = valA.localeCompare(valB, undefined, {{ numeric: true, sensitivity: 'base' }});
        return probSortAsc ? cmp : -cmp;
      }});
    }}

    function sortContests() {{
      filteredContests.sort((a, b) => {{
        let valA = a[contestSortCol];
        let valB = b[contestSortCol];

        if (typeof valA === 'number' && typeof valB === 'number') {{
          return contestSortAsc ? (valA - valB) : (valB - valA);
        }}
        valA = (valA || '').toString();
        valB = (valB || '').toString();
        const cmp = valA.localeCompare(valB, undefined, {{ numeric: true, sensitivity: 'base' }});
        return contestSortAsc ? cmp : -cmp;
      }});
    }}

    function updateProblemSortIcons() {{
      document.querySelectorAll('.sortable-th i').forEach(icon => {{
        icon.className = 'fa-solid fa-sort text-slate-500';
      }});
      const activeIcon = document.getElementById(`sort_icon_${{probSortCol}}`);
      if (activeIcon) {{
        activeIcon.className = probSortAsc 
          ? 'fa-solid fa-sort-up text-brand-400' 
          : 'fa-solid fa-sort-down text-brand-400';
      }}
    }}

    function updateContestSortIcons() {{
      document.querySelectorAll('.sortable-contest-th i').forEach(icon => {{
        icon.className = 'fa-solid fa-sort text-slate-500';
      }});
      const activeIcon = document.getElementById(`sort_${{contestSortCol}}`);
      if (activeIcon) {{
        activeIcon.className = contestSortAsc 
          ? 'fa-solid fa-sort-up text-indigo-400' 
          : 'fa-solid fa-sort-down text-indigo-400';
      }}
    }}

    function updateMetrics() {{
      const probCount = filteredProblems.length;
      document.getElementById('kpiProblems').textContent = probCount.toLocaleString();

      const uniqueContests = filteredContests.length;
      document.getElementById('kpiContests').textContent = uniqueContests.toLocaleString();

      if (probCount > 0) {{
        const avgR = Math.round(filteredProblems.reduce((sum, p) => sum + (p.cf_rating || 0), 0) / probCount);
        document.getElementById('kpiAvgRating').textContent = avgR;
        
        let tier = 'Easy';
        let tierClass = 'text-emerald-400 bg-emerald-400/10';
        if (avgR >= 2000) {{ tier = 'Expert'; tierClass = 'text-purple-400 bg-purple-400/10'; }}
        else if (avgR >= 1600) {{ tier = 'Hard'; tierClass = 'text-rose-400 bg-rose-400/10'; }}
        else if (avgR >= 1200) {{ tier = 'Medium'; tierClass = 'text-amber-400 bg-amber-400/10'; }}
        
        const tierEl = document.getElementById('kpiAvgTier');
        tierEl.textContent = tier;
        tierEl.className = 'text-xs px-2 py-0.5 rounded font-medium ' + tierClass;

        // Top Category
        const catMap = {{}};
        filteredProblems.forEach(p => {{
          catMap[p.primary_category] = (catMap[p.primary_category] || 0) + 1;
        }});
        let topCat = 'None', topCount = 0;
        for (const [c, cnt] of Object.entries(catMap)) {{
          if (cnt > topCount) {{
            topCount = cnt;
            topCat = c;
          }}
        }}
        document.getElementById('kpiTopCategory').textContent = topCat;
        document.getElementById('kpiTopCatCount').textContent = topCount + ' probs';

        // Max rating
        const maxR = Math.max(...filteredProblems.map(p => p.cf_rating || 0));
        document.getElementById('kpiMaxRating').textContent = maxR;
      }} else {{
        document.getElementById('kpiAvgRating').textContent = '0';
        document.getElementById('kpiTopCategory').textContent = 'None';
        document.getElementById('kpiTopCatCount').textContent = '0';
        document.getElementById('kpiMaxRating').textContent = '0';
      }}
    }}

    function updateCharts() {{
      updateCategoryChart();
      updateRatingChart();
      updateTimelineChart();
    }}

    function updateCategoryChart() {{
      const counts = {{}};
      filteredProblems.forEach(p => {{
        counts[p.primary_category] = (counts[p.primary_category] || 0) + 1;
      }});
      const sortedKeys = Object.keys(counts).sort((a,b) => counts[b] - counts[a]);
      const labels = sortedKeys;
      const data = sortedKeys.map(k => counts[k]);

      const colors = [
        '#6366f1', '#10b981', '#f59e0b', '#ec4899', '#3b82f6',
        '#8b5cf6', '#14b8a6', '#f97316', '#06b6d4', '#eab308',
        '#64748b', '#a855f7'
      ];

      if (categoryChart) categoryChart.destroy();
      const ctx = document.getElementById('categoryChart').getContext('2d');
      categoryChart = new Chart(ctx, {{
        type: 'doughnut',
        data: {{
          labels: labels,
          datasets: [{{
            data: data,
            backgroundColor: colors.slice(0, labels.length),
            borderWidth: 0,
            hoverOffset: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              position: 'right',
              labels: {{
                color: '#cbd5e1',
                boxWidth: 12,
                padding: 10,
                font: {{ size: 11 }}
              }}
            }}
          }},
          cutout: '68%'
        }}
      }});
    }}

    function updateRatingChart() {{
      const buckets = {{
        '800-999': 0,
        '1000-1199': 0,
        '1200-1399': 0,
        '1400-1599': 0,
        '1600-1799': 0,
        '1800-1999': 0,
        '2000-2199': 0,
        '2200+': 0
      }};

      filteredProblems.forEach(p => {{
        const r = p.cf_rating || 1200;
        if (r < 1000) buckets['800-999']++;
        else if (r < 1200) buckets['1000-1199']++;
        else if (r < 1400) buckets['1200-1399']++;
        else if (r < 1600) buckets['1400-1599']++;
        else if (r < 1800) buckets['1600-1799']++;
        else if (r < 2000) buckets['1800-1999']++;
        else if (r < 2200) buckets['2000-2199']++;
        else buckets['2200+']++;
      }});

      if (ratingChart) ratingChart.destroy();
      const ctx = document.getElementById('ratingChart').getContext('2d');
      ratingChart = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: Object.keys(buckets),
          datasets: [{{
            data: Object.values(buckets),
            backgroundColor: [
              '#10b981', '#10b981',
              '#06b6d4', '#3b82f6',
              '#8b5cf6', '#a855f7',
              '#f59e0b', '#ef4444'
            ],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }}
          }},
          scales: {{
            x: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }}, grid: {{ display: false }} }},
            y: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }}, grid: {{ color: '#1e293b' }} }}
          }}
        }}
      }});
    }}

    function updateTimelineChart() {{
      const monthMap = {{}};
      filteredProblems.forEach(p => {{
        if (p.contest_date) {{
          const m = p.contest_date.slice(0, 7);
          monthMap[m] = (monthMap[m] || 0) + 1;
        }}
      }});
      const sortedMonths = Object.keys(monthMap).sort();

      if (timelineChart) timelineChart.destroy();
      const ctx = document.getElementById('timelineChart').getContext('2d');
      timelineChart = new Chart(ctx, {{
        type: 'line',
        data: {{
          labels: sortedMonths,
          datasets: [{{
            label: 'Problems in Contests',
            data: sortedMonths.map(m => monthMap[m]),
            borderColor: '#6366f1',
            backgroundColor: 'rgba(99, 102, 241, 0.15)',
            fill: true,
            tension: 0.35,
            pointRadius: 3,
            pointBackgroundColor: '#818cf8'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }}
          }},
          scales: {{
            x: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }}, maxRotation: 45 }}, grid: {{ display: false }} }},
            y: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }}, grid: {{ color: '#1e293b' }} }}
          }}
        }}
      }});
    }}

    function renderContestsTable() {{
      const tbody = document.getElementById('contestsTableBody');
      tbody.innerHTML = '';

      const total = filteredContests.length;
      const startIdx = (contestPage - 1) * contestPageSize;
      const endIdx = Math.min(startIdx + contestPageSize, total);
      const pageSlice = filteredContests.slice(startIdx, endIdx);

      if (pageSlice.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="8" class="py-12 text-center text-slate-500">No contests match the current filter selection.</td></tr>`;
      }} else {{
        pageSlice.forEach(c => {{
          const tr = document.createElement('tr');
          const isExpanded = expandedContestIds.has(c.contest_id);
          tr.className = `hover:bg-slate-800/40 transition cursor-pointer ${{isExpanded ? 'bg-slate-800/30' : ''}}`;

          let badgeColor = 'bg-slate-800 text-slate-300';
          if (c.avg_cf_rating >= 2000) badgeColor = 'bg-purple-900/40 text-purple-300 border border-purple-700/50';
          else if (c.avg_cf_rating >= 1600) badgeColor = 'bg-rose-900/40 text-rose-300 border border-rose-700/50';
          else if (c.avg_cf_rating >= 1200) badgeColor = 'bg-amber-900/40 text-amber-300 border border-amber-700/50';
          else badgeColor = 'bg-emerald-900/40 text-emerald-300 border border-emerald-700/50';

          let typeColor = 'bg-slate-800 text-slate-300';
          if (c.contest_type === 'Team Forming') typeColor = 'bg-indigo-900/40 text-indigo-300 border border-indigo-700/40';
          else if (c.contest_type === 'Team Practice') typeColor = 'bg-blue-900/40 text-blue-300 border border-blue-700/40';
          else if (c.contest_type === 'Weekly Contest') typeColor = 'bg-emerald-900/40 text-emerald-300 border border-emerald-700/40';
          else if (c.contest_type === 'Beginner Contest') typeColor = 'bg-teal-900/40 text-teal-300 border border-teal-700/40';
          else if (c.contest_type === 'Topic Contest') typeColor = 'bg-purple-900/40 text-purple-300 border border-purple-700/40';

          tr.innerHTML = `
            <td class="py-3 px-3 text-center mono text-slate-400 font-semibold">#${{c.contest_index}}</td>
            <td class="py-3 px-3 text-slate-400 mono whitespace-nowrap">${{c.date || 'N/A'}}</td>
            <td class="py-3 px-3 max-w-[280px]">
              <a href="${{c.link}}" target="_blank" onclick="event.stopPropagation()" class="font-semibold text-white hover:text-indigo-400 transition" title="Open contest #${{c.contest_id}} on VJudge">
                ${{c.title}}
              </a>
            </td>
            <td class="py-3 px-3 whitespace-nowrap">
              <span class="px-2 py-0.5 rounded text-[10px] font-medium ${{typeColor}}">
                ${{c.contest_type}}
              </span>
            </td>
            <td class="py-3 px-2 text-center whitespace-nowrap">
              <span class="px-2 py-0.5 rounded-full text-xs font-mono font-bold bg-slate-800 text-white">
                ${{c.problem_count}}
              </span>
            </td>
            <td class="py-3 px-3 text-center whitespace-nowrap">
              <span class="px-2 py-0.5 rounded text-[11px] font-semibold mono ${{badgeColor}}">
                ${{c.avg_cf_rating}}
              </span>
              <div class="text-[10px] text-slate-500 mt-0.5">${{c.min_cf_rating}} - ${{c.max_cf_rating}}</div>
            </td>
            <td class="py-3 px-3 max-w-[220px] truncate text-slate-400 text-[11px]" title="${{c.category_summary || ''}}">
              ${{c.category_summary || 'N/A'}}
            </td>
            <td class="py-3 px-3 text-center whitespace-nowrap">
              <button onclick="toggleContestAccordion(${{c.contest_id}}, event)" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-indigo-300 font-medium text-xs flex items-center space-x-1 mx-auto transition">
                <span>${{isExpanded ? 'Hide' : 'Problems'}}</span>
                <i class="fa-solid ${{isExpanded ? 'fa-chevron-up' : 'fa-chevron-down'}} text-[10px]"></i>
              </button>
            </td>
          `;

          tr.addEventListener('click', () => toggleContestAccordion(c.contest_id));
          tbody.appendChild(tr);

          if (isExpanded) {{
            const accTr = document.createElement('tr');
            accTr.className = 'bg-slate-900/90 border-b border-indigo-900/40';

            const probs = c.problems_preview || [];
            let probRowsHtml = '';

            probs.forEach(p => {{
              let pBadge = 'bg-slate-800 text-slate-300';
              if (p.rating >= 2000) pBadge = 'bg-purple-900/40 text-purple-300 border border-purple-700/50';
              else if (p.rating >= 1600) pBadge = 'bg-rose-900/40 text-rose-300 border border-rose-700/50';
              else if (p.rating >= 1200) pBadge = 'bg-amber-900/40 text-amber-300 border border-amber-700/50';
              else pBadge = 'bg-emerald-900/40 text-emerald-300 border border-emerald-700/50';

              const contestProbUrl = p.contest_url || `${{c.link}}#problem/${{p.letter}}`;

              probRowsHtml += `
                <tr class="hover:bg-slate-800/50 transition border-b border-slate-800/40">
                  <td class="py-2 px-3 font-bold text-white mono text-center">${{p.letter}}</td>
                  <td class="py-2 px-3 text-slate-200 font-medium">
                    <a href="${{contestProbUrl}}" target="_blank" onclick="event.stopPropagation()" class="hover:text-indigo-400 transition">
                      ${{p.title}}
                    </a>
                  </td>
                  <td class="py-2 px-3 mono text-slate-400 text-xs">
                    <a href="${{p.vjudge_url}}" target="_blank" onclick="event.stopPropagation()" class="hover:text-brand-400 transition" title="Open source problem on VJudge">
                      ${{p.oj}} ${{p.code}}
                    </a>
                  </td>
                  <td class="py-2 px-3">
                    <span class="px-2 py-0.5 rounded-full text-[10px] bg-slate-800 text-slate-300 border border-slate-700">
                      ${{p.category}}
                    </span>
                  </td>
                  <td class="py-2 px-3 text-center">
                    <span class="px-2 py-0.5 rounded text-[10px] font-semibold mono ${{pBadge}}">
                      ${{p.rating}}
                    </span>
                  </td>
                  <td class="py-2 px-3 text-center">
                    <a href="${{contestProbUrl}}" target="_blank" onclick="event.stopPropagation()" class="p-1 rounded text-indigo-400 hover:bg-slate-800 transition" title="Solve problem">
                      <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
                    </a>
                  </td>
                </tr>
              `;
            }});

            accTr.innerHTML = `
              <td colspan="8" class="p-4 bg-slate-950/60">
                <div class="rounded-xl border border-slate-800 bg-slate-900/90 p-4 space-y-3">
                  <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800 pb-2.5 gap-2">
                    <div class="flex items-center space-x-3">
                      <span class="font-bold text-sm text-white">Contest Problems (${{probs.length}})</span>
                      <span class="text-xs text-slate-400">${{c.title}}</span>
                    </div>
                    <div class="flex items-center space-x-2 text-xs">
                      <a href="${{c.link}}" target="_blank" onclick="event.stopPropagation()" class="px-3 py-1 rounded bg-indigo-600 hover:bg-indigo-500 text-white font-medium flex items-center space-x-1.5 transition">
                        <i class="fa-solid fa-arrow-up-right-from-square"></i>
                        <span>Open Entire Contest</span>
                      </a>
                    </div>
                  </div>

                  <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                      <thead class="text-slate-500 uppercase tracking-wider text-[10px] bg-slate-800/40">
                        <tr>
                          <th class="py-2 px-3 text-center w-10">#</th>
                          <th class="py-2 px-3">Problem Title</th>
                          <th class="py-2 px-3">Source OJ</th>
                          <th class="py-2 px-3">Topic</th>
                          <th class="py-2 px-3 text-center">CF Rating</th>
                          <th class="py-2 px-3 text-center w-12">Solve</th>
                        </tr>
                      </thead>
                      <tbody class="divide-y divide-slate-800/60 font-normal">
                        ${{probRowsHtml}}
                      </tbody>
                    </table>
                  </div>
                </div>
              </td>
            `;
            tbody.appendChild(accTr);
          }}
        }});
      }}

      document.getElementById('contestPageInfo').textContent = total === 0 ? 'No contests found' :
        `Showing ${{startIdx + 1}} to ${{endIdx}} of ${{total.toLocaleString()}} contests`;

      renderContestsPagination(total);
    }}

    function toggleContestAccordion(contestId, e) {{
      if (e) e.stopPropagation();
      if (expandedContestIds.has(contestId)) {{
        expandedContestIds.delete(contestId);
      }} else {{
        expandedContestIds.add(contestId);
      }}
      renderContestsTable();
    }}

    function renderContestsPagination(total) {{
      const totalPages = Math.ceil(total / contestPageSize) || 1;
      const container = document.getElementById('contestPaginationControls');
      container.innerHTML = '';

      const createBtn = (label, page, disabled, active) => {{
        const b = document.createElement('button');
        b.innerHTML = label;
        b.disabled = disabled;
        b.className = `px-2.5 py-1 rounded text-xs font-medium transition ${{
          active ? 'bg-indigo-600 text-white' :
          disabled ? 'bg-slate-900 text-slate-600 cursor-not-allowed' :
          'bg-slate-800 hover:bg-slate-700 text-slate-300'
        }}`;
        if (!disabled) {{
          b.addEventListener('click', () => {{
            contestPage = page;
            renderContestsTable();
          }});
        }}
        return b;
      }};

      container.appendChild(createBtn('<i class="fa-solid fa-angles-left"></i>', 1, contestPage === 1, false));
      container.appendChild(createBtn('<i class="fa-solid fa-angle-left"></i>', contestPage - 1, contestPage === 1, false));

      const maxBtns = 5;
      let startP = Math.max(1, contestPage - 2);
      let endP = Math.min(totalPages, startP + maxBtns - 1);
      if (endP - startP < maxBtns - 1) {{
        startP = Math.max(1, endP - maxBtns + 1);
      }}

      for (let p = startP; p <= endP; p++) {{
        container.appendChild(createBtn(p, p, false, p === contestPage));
      }}

      container.appendChild(createBtn('<i class="fa-solid fa-angle-right"></i>', contestPage + 1, contestPage === totalPages, false));
      container.appendChild(createBtn('<i class="fa-solid fa-angles-right"></i>', totalPages, contestPage === totalPages, false));
    }}

    function renderProblemsTable() {{
      const tbody = document.getElementById('problemsTableBody');
      tbody.innerHTML = '';

      const total = filteredProblems.length;
      const startIdx = (probPage - 1) * probPageSize;
      const endIdx = Math.min(startIdx + probPageSize, total);
      const pageSlice = filteredProblems.slice(startIdx, endIdx);

      if (pageSlice.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="9" class="py-12 text-center text-slate-500">No problems match the current filter selection.</td></tr>`;
      }} else {{
        pageSlice.forEach(p => {{
          const tr = document.createElement('tr');
          tr.className = 'hover:bg-slate-800/40 transition';

          let badgeColor = 'bg-slate-800 text-slate-300';
          if (p.cf_rating >= 2000) badgeColor = 'bg-purple-900/40 text-purple-300 border border-purple-700/50';
          else if (p.cf_rating >= 1600) badgeColor = 'bg-rose-900/40 text-rose-300 border border-rose-700/50';
          else if (p.cf_rating >= 1200) badgeColor = 'bg-amber-900/40 text-amber-300 border border-amber-700/50';
          else badgeColor = 'bg-emerald-900/40 text-emerald-300 border border-emerald-700/50';

          tr.innerHTML = `
            <td class="py-2.5 px-3 text-slate-400 mono whitespace-nowrap">${{p.contest_date || 'N/A'}}</td>
            <td class="py-2.5 px-3 max-w-[200px] truncate">
              <a href="${{p.contest_link}}" target="_blank" class="hover:text-brand-400 text-slate-300 transition" title="${{p.contest_title}}">
                ${{p.contest_title}}
              </a>
            </td>
            <td class="py-2.5 px-2 whitespace-nowrap">
              <span class="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-800 text-slate-300 border border-slate-700">
                ${{p.contest_type}}
              </span>
            </td>
            <td class="py-2.5 px-2 text-center font-bold text-white mono">${{p.problem_letter}}</td>
            <td class="py-2.5 px-3 font-medium text-slate-100 max-w-[220px] truncate" title="${{p.problem_title}}">
              <a href="${{p.contest_url || p.vjudge_url}}" target="_blank" class="hover:text-brand-400 transition">
                ${{p.problem_title}}
              </a>
            </td>
            <td class="py-2.5 px-2 mono text-slate-400 whitespace-nowrap">
              <a href="${{p.vjudge_url}}" target="_blank" class="hover:text-indigo-400 transition" title="Open source problem on VJudge">
                ${{p.oj}} ${{p.oj_prob_code}}
              </a>
            </td>
            <td class="py-2.5 px-3 whitespace-nowrap">
              <span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-slate-800/80 text-slate-300 border border-slate-700/60">
                ${{p.primary_category}}
              </span>
            </td>
            <td class="py-2.5 px-3 text-center whitespace-nowrap">
              <span class="px-2 py-0.5 rounded text-[11px] font-semibold mono ${{badgeColor}}">
                ${{p.cf_rating}}
              </span>
            </td>
            <td class="py-2.5 px-2 text-center whitespace-nowrap">
              <a href="${{p.contest_url || p.vjudge_url}}" target="_blank" class="p-1 rounded hover:bg-slate-700 text-brand-400 text-xs" title="Solve in Contest">
                <i class="fa-solid fa-arrow-up-right-from-square"></i>
              </a>
            </td>
          `;
          tbody.appendChild(tr);
        }});
      }}

      document.getElementById('pageInfo').textContent = total === 0 ? 'No entries found' :
        `Showing ${{startIdx + 1}} to ${{endIdx}} of ${{total.toLocaleString()}} problems`;

      renderProblemsPagination(total);
    }}

    function renderProblemsPagination(total) {{
      const totalPages = Math.ceil(total / probPageSize) || 1;
      const container = document.getElementById('paginationControls');
      container.innerHTML = '';

      const createBtn = (label, page, disabled, active) => {{
        const b = document.createElement('button');
        b.innerHTML = label;
        b.disabled = disabled;
        b.className = `px-2.5 py-1 rounded text-xs font-medium transition ${{
          active ? 'bg-brand-600 text-white' :
          disabled ? 'bg-slate-900 text-slate-600 cursor-not-allowed' :
          'bg-slate-800 hover:bg-slate-700 text-slate-300'
        }}`;
        if (!disabled) {{
          b.addEventListener('click', () => {{
            probPage = page;
            renderProblemsTable();
          }});
        }}
        return b;
      }};

      container.appendChild(createBtn('<i class="fa-solid fa-angles-left"></i>', 1, probPage === 1, false));
      container.appendChild(createBtn('<i class="fa-solid fa-angle-left"></i>', probPage - 1, probPage === 1, false));

      const maxBtns = 5;
      let startP = Math.max(1, probPage - 2);
      let endP = Math.min(totalPages, startP + maxBtns - 1);
      if (endP - startP < maxBtns - 1) {{
        startP = Math.max(1, endP - maxBtns + 1);
      }}

      for (let p = startP; p <= endP; p++) {{
        container.appendChild(createBtn(p, p, false, p === probPage));
      }}

      container.appendChild(createBtn('<i class="fa-solid fa-angle-right"></i>', probPage + 1, probPage === totalPages, false));
      container.appendChild(createBtn('<i class="fa-solid fa-angles-right"></i>', totalPages, probPage === totalPages, false));
    }}

    function exportFilteredProblemsCsv() {{
      const headers = ['id', 'contest_id', 'contest_index', 'contest_title', 'contest_type', 'contest_date', 'contest_link', 'problem_letter', 'problem_title', 'oj', 'oj_prob_code', 'cf_rating', 'difficulty_level', 'primary_category', 'contest_url', 'vjudge_url'];
      const rows = [headers.join(',')];
      filteredProblems.forEach(p => {{
        const row = [
          p.id,
          p.contest_id,
          p.contest_index,
          `"${{(p.contest_title || '').replace(/"/g, '""')}}"`,
          `"${{p.contest_type}}"`,
          p.contest_date || '',
          p.contest_link,
          p.problem_letter,
          `"${{(p.problem_title || '').replace(/"/g, '""')}}"`,
          p.oj,
          `"${{p.oj_prob_code}}"`,
          p.cf_rating,
          p.difficulty_level,
          `"${{p.primary_category}}"`,
          p.contest_url,
          p.vjudge_url
        ];
        rows.push(row.join(','));
      }});
      const blob = new Blob([rows.join('\\n')], {{ type: 'text/csv' }});
      downloadBlob(blob, 'vjudge_problems_filtered.csv');
    }}

    function exportFilteredContestsCsv() {{
      const headers = ['contest_index', 'contest_id', 'title', 'contest_type', 'date', 'link', 'problem_count', 'avg_cf_rating', 'min_cf_rating', 'max_cf_rating', 'difficulty_level', 'category_summary'];
      const rows = [headers.join(',')];
      filteredContests.forEach(c => {{
        const row = [
          c.contest_index,
          c.contest_id,
          `"${{(c.title || '').replace(/"/g, '""')}}"`,
          `"${{c.contest_type}}"`,
          c.date || '',
          c.link,
          c.problem_count,
          c.avg_cf_rating,
          c.min_cf_rating,
          c.max_cf_rating,
          c.difficulty_level,
          `"${{(c.category_summary || '').replace(/"/g, '""')}}"`
        ];
        rows.push(row.join(','));
      }});
      const blob = new Blob([rows.join('\\n')], {{ type: 'text/csv' }});
      downloadBlob(blob, 'vjudge_contests_filtered.csv');
    }}

    function exportFilteredJson() {{
      const exportData = {{
        metadata: {{
          exported_at: new Date().toISOString(),
          filtered_problems_count: filteredProblems.length,
          filtered_contests_count: filteredContests.length
        }},
        contests: filteredContests,
        problems: filteredProblems
      }};
      const blob = new Blob([JSON.stringify(exportData, null, 2)], {{ type: 'application/json' }});
      downloadBlob(blob, 'vjudge_database_filtered.json');
    }}

    function downloadBlob(blob, filename) {{
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = filename;
      a.click();
    }}
  </script>
</body>
</html>
'''

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Successfully generated public sanitized index.html ({len(html_content):,} bytes)")

if __name__ == '__main__':
    build_public_site()
