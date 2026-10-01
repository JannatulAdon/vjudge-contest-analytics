# 🏆 VJudge Contest & Problem Analytics Hub

An interactive analytics dashboard and open dataset cataloging **105 competitive programming contests** and **1,317 problems** from VJudge, mapped to a unified **Codeforces difficulty rating scale** and categorized by algorithmic topic.

🌐 **Live Dashboard**: [https://jannatuladon.github.io/vjudge-contest-analytics/](https://jannatuladon.github.io/vjudge-contest-analytics/)

---

## 📊 Overview & Dataset Highlights

* **Total Contests**: 105 contests spanning from December 2022 to September 2026.
* **Total Problems**: 1,317 unique problem appearances across major online judges (Codeforces Gym, Codeforces, AtCoder, CodeChef, CSES, Toph, LightOJ, and UVA).
* **Average Difficulty**: ~1543 CF Rating (Medium Tier).
* **Rating Range**: 800 to 3,164 (Div. 2 A beginner friendly to Grandmaster level).
* **Primary Contest Types**:
  * **Team Forming Contests** (44)
  * **Team Practice Contests** (26)
  * **Weekly Contests** (18)
  * **Beginner Contests** (10)
  * **Topic-Specific Contests** (5)
  * **Special & Practice Contests** (2)

---

## 🎯 Key Features

1. **Contest Explorer (Primary View)**:
   * Overview of all 105 contests with dates, problem counts, average difficulty, and top topics.
   * **Clickable Sortable Headers**: Sort by date, title, problem count, or average difficulty.
   * **Expandable Problem Drawer**: Click on any contest to reveal all problems with their letter, title, origin judge, topic badge, CF rating, and direct VJudge links.
2. **Individual Problems Explorer**:
   * Browse all 1,317 problems with sortable headers (`Date`, `Contest`, `Type`, `#`, `Problem Title`, `OJ Code`, `Topic`, `CF Rating`).
3. **Interactive Visual Analytics**:
   * **Topic Breakdown**: Doughnut chart analyzing algorithmic topic distributions (Dynamic Programming, Graphs, Trees, Math & Number Theory, Geometry, etc.).
   * **Difficulty Histogram**: Bar distribution showing problem volume across Codeforces rating bands (800–999, 1000–1199, ..., 2200+).
   * **Contest Activity Timeline**: Volume trends over time.
4. **Time & Criteria Filters**:
   * Quick presets (*Past 3 Mos, Past 6 Mos, Past 10 Mos, Past 1 Year, 2026, 2024, 2023, All Time*) or custom date range.
   * Filter by Contest Type, Topic, Difficulty Tier, and Search Keywords.
5. **AI Coaching Prompt Generator**:
   * Click **"Export for AI"** on any filtered view to copy a structured training prompt summarizing your practice scope, topic distribution, and representative problems for ChatGPT, Claude, or Gemini.
6. **Data Exports**:
   * Download filtered datasets in CSV and JSON directly from the dashboard.

---

## 📁 Repository Structure

* `index.html` — Zero-dependency, standalone interactive analytics dashboard.
* `contests_public.csv` — Catalog of all 105 contests with metrics and topic summaries.
* `problems_public.csv` — Catalog of all 1,317 problems with ratings and tags.
* `dataset_public.json` — Complete structured dataset for programmatic access and AI ingestion.
* `build_public_site.py` — Python script to rebuild and sanitize `index.html`.
* `build_database.py` — Database enrichment script integrating Codeforces and AtCoder difficulty models.

---

## 🚀 Local Usage

Simply clone the repository and open `index.html` in any modern web browser:

```bash
git clone https://github.com/JannatulAdon/vjudge-contest-analytics.git
cd vjudge-contest-analytics
# Open directly in your browser:
google-chrome index.html # or brave-browser index.html / open index.html
```

---

## 📄 License
MIT License. Created for competitive programmers, ICPC contestants, and algorithmic problem-solving communities.
