# Dashboard Visual Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the CSS of `index.html` to a glassmorphism dark theme with amber/gold accent, without touching any JS logic or data.

**Architecture:** Single HTML file. Only the `<style>` block is fully replaced and 3 ambient orb `<div>` elements are added to `<body>`. All JS-driven IDs/classes remain untouched. Minor HTML class tweaks to header and day-row wrapper (no JS dependency).

**Tech Stack:** Bootstrap 5.3, vanilla JS, CSS `backdrop-filter`, CSS custom properties for accent color.

---

## Files

| Action | Path | What changes |
|--------|------|--------------|
| Modify | `index.html` | Replace `<style>` block; add 3 `.orb` divs; update header div class; update day-row div class |

No new files. No JS changes.

---

### Task 1: Add ambient orb divs + update header HTML

**Files:**
- Modify: `index.html` (HTML only, before `<style>` rewrite)

- [ ] **Step 1: Add orb divs as first children of `<body>`**

Find this line in `index.html`:
```html
<div class="container" style="max-width:680px; padding-bottom: 80px;">
```

Insert immediately before it:
```html
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
<div class="orb orb-3"></div>
```

- [ ] **Step 2: Update header div + add date span**

Find:
```html
  <div class="py-3">
    <h5 class="mb-0 fw-bold">Умиджон <span style="color:#555;font-weight:400;font-size:0.85rem;">/ тайм-менеджмент</span></h5>
  </div>
```

Replace with:
```html
  <div class="header-wrap">
    <h5 class="mb-0 fw-bold">Умиджон <span class="header-sub">/ тайм-менеджмент</span></h5>
    <div class="header-date" id="header-date"></div>
  </div>
```

- [ ] **Step 3: Update day buttons wrapper class**

Find:
```html
      <div class="d-flex gap-1 mb-3 flex-wrap">
```

Replace with:
```html
      <div class="day-row">
```

- [ ] **Step 4: Add date rendering JS snippet before `</script>`**

Find `// INIT` section at the bottom of `<script>` and add before `initDayTab();`:
```js
// Render header date
(function() {
  const el = document.getElementById('header-date');
  if (!el) return;
  const d = new Date();
  const days = ['Вс','Пн','Вт','Ср','Чт','Пт','Сб'];
  const months = ['янв','фев','мар','апр','май','июн','июл','авг','сен','окт','ноя','дек'];
  el.textContent = `${days[d.getDay()]}, ${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`;
})();
```

- [ ] **Step 5: Open `index.html` in browser and verify structure renders without errors (no JS console errors)**

---

### Task 2: Replace `<style>` block — Base + Header + Tabs

**Files:**
- Modify: `index.html` — `<style>` block

- [ ] **Step 1: Delete the entire existing `<style>...</style>` block and replace with the new one below**

Start with the opening and base styles:

```css
<style>
/* ============================================================
   BASE
   ============================================================ */
*, *::before, *::after { box-sizing: border-box; }

body {
  background: #0a0a0f;
  color: #e0e0e0;
  font-size: 0.92rem;
}

/* Ambient orbs — decorative blurred blobs */
.orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  z-index: 0;
}
.orb-1 { width: 400px; height: 400px; background: rgba(251,191,36,0.07);  top: -100px; right: -80px; }
.orb-2 { width: 300px; height: 300px; background: rgba(251,146,60,0.05);  bottom: 100px; left: -80px; }
.orb-3 { width: 200px; height: 200px; background: rgba(99,102,241,0.04);  top: 50%; left: 40%; }

/* Lift container above orbs */
.container { position: relative; z-index: 1; }

/* ============================================================
   HEADER
   ============================================================ */
.header-wrap {
  padding: 18px 0 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.header-sub {
  color: #555;
  font-weight: 400;
  font-size: 0.82rem;
  margin-left: 6px;
}
.header-date {
  font-size: 11px;
  color: #555;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  padding: 4px 12px;
  border-radius: 20px;
  white-space: nowrap;
}

/* ============================================================
   TABS
   ============================================================ */
.nav-tabs {
  border: 1px solid rgba(255,255,255,0.07) !important;
  background: rgba(255,255,255,0.03);
  border-radius: 10px;
  padding: 3px;
  backdrop-filter: blur(12px);
  display: flex;
  gap: 2px;
}
.nav-tabs .nav-link {
  flex: 1;
  text-align: center;
  color: #555;
  border: 1px solid transparent !important;
  border-radius: 7px !important;
  padding: 6px 4px;
  font-size: 12px;
  transition: color 0.2s, background 0.2s;
}
.nav-tabs .nav-link:hover {
  color: #888;
  background: rgba(255,255,255,0.04);
}
.nav-tabs .nav-link.active {
  color: #fbbf24 !important;
  background: rgba(251,191,36,0.13) !important;
  border-color: rgba(251,191,36,0.25) !important;
  font-weight: 600;
  box-shadow: 0 0 12px rgba(251,191,36,0.08);
}

/* General */
.tab-content { padding-top: 16px; }
h6.section-title {
  color: #333;
  text-transform: uppercase;
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  margin: 20px 0 10px;
}
```

- [ ] **Step 2: Open browser, verify header and tabs look correct — amber active tab, glass background, orbs visible**

---

### Task 3: Day tab CSS — pills, schedule rows, progress bar

- [ ] **Step 1: Append Day tab CSS to the `<style>` block**

```css
/* ============================================================
   DAY TAB
   ============================================================ */

/* Day selector pills */
.day-row {
  display: flex;
  gap: 6px;
  margin-bottom: 16px;
}
.day-btn {
  flex: 1;
  text-align: center;
  padding: 6px 2px;
  border-radius: 8px;
  font-size: 11px;
  color: #444;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06) !important;
  cursor: pointer;
  min-width: unset;
  transition: all 0.15s;
  font-weight: 500;
}
.day-btn:hover { color: #777; background: rgba(255,255,255,0.05); }
.day-btn.martial {
  color: rgba(239,68,68,0.65);
  border-color: rgba(239,68,68,0.18) !important;
  background: rgba(239,68,68,0.04);
}
.day-btn.active-day {
  background: rgba(251,191,36,0.12) !important;
  color: #fbbf24 !important;
  border-color: rgba(251,191,36,0.3) !important;
  font-weight: 700;
}
.day-btn.martial.active-day {
  background: rgba(239,68,68,0.15) !important;
  color: #f87171 !important;
  border-color: rgba(239,68,68,0.35) !important;
}

/* Schedule rows */
.schedule-row {
  display: flex;
  align-items: center;
  gap: 0;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 8px;
  margin-bottom: 4px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  backdrop-filter: blur(8px);
  transition: background 0.15s, border-color 0.15s;
}
.schedule-row:hover { background: rgba(255,255,255,0.05); }
.schedule-row.done {
  background: rgba(251,191,36,0.03);
  border-color: rgba(251,191,36,0.08);
}
.schedule-row.done .task-text { text-decoration: line-through; color: #3a3a3a; }
.schedule-row.done .task-time { color: #2e2e2e; }

.cat-bar {
  width: 3px;
  min-height: 28px;
  border-radius: 2px;
  margin-right: 10px;
  flex-shrink: 0;
}
.task-time {
  width: 40px;
  color: #555;
  font-size: 0.8rem;
  flex-shrink: 0;
}
.task-icon {
  width: 24px;
  text-align: center;
  flex-shrink: 0;
  font-size: 0.95rem;
}
.task-text {
  flex: 1;
  color: #ccc;
  font-size: 0.875rem;
  margin-left: 4px;
}
/* Checkmark box */
.task-check {
  margin-left: 8px;
  width: 16px;
  height: 16px;
  border: 1.5px solid #252525;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  flex-shrink: 0;
  color: transparent;
}
.schedule-row.done .task-check {
  background: rgba(251,191,36,0.18);
  border-color: rgba(251,191,36,0.4);
  color: #fbbf24;
}

/* Sticky progress bar */
#day-progress-wrap {
  position: sticky;
  bottom: 0;
  background: rgba(10,10,15,0.92);
  backdrop-filter: blur(16px);
  border-top: 1px solid rgba(255,255,255,0.05);
  padding: 10px 0 4px;
}
#day-progress-wrap .d-flex small { font-size: 11px; }
#progress-label { color: #555; }
#progress-pct { color: #fbbf24; }
#progress-bar {
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
  box-shadow: 0 0 8px rgba(251,191,36,0.35);
}
.progress {
  background: rgba(255,255,255,0.05);
  border-radius: 3px;
}
```

- [ ] **Step 2: Open browser on Day tab, verify: glass rows, amber active day pill, red martial day pills, amber progress bar, done rows strikethrough with amber checkmark**

---

### Task 4: Week tab CSS

- [ ] **Step 1: Append Week tab CSS**

```css
/* ============================================================
   WEEK TAB
   ============================================================ */
.week-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 10px;
  padding: 12px 14px;
  margin-bottom: 8px;
  backdrop-filter: blur(8px);
}
.week-card.martial-day { border-left: 2px solid rgba(239,68,68,0.4); }
/* Today highlight applied inline in JS via style.borderColor — override here */
.week-card .day-label {
  font-weight: 600;
  font-size: 0.9rem;
  color: #ddd;
  margin-bottom: 3px;
}
.week-card .day-theme {
  font-size: 0.8rem;
  color: #555;
  margin-bottom: 8px;
}
/* Tasks as tags */
.week-card ul {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.week-card ul li {
  font-size: 10px;
  color: #666;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 4px;
  padding: 2px 7px;
}

/* Weekly rules */
.rule-item {
  padding: 6px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  font-size: 0.87rem;
  color: #777;
}
.rule-item:last-child { border-bottom: none; }

/* Badge override for "сегодня" */
.badge.bg-warning { background: rgba(251,191,36,0.2) !important; color: #fbbf24 !important; font-size: 0.65rem !important; border: 1px solid rgba(251,191,36,0.3); }
```

- [ ] **Step 2: Switch to Week tab in browser — verify glass cards, red left border on martial days, amber "сегодня" badge, tasks as tags**

---

### Task 5: Finance tab CSS

- [ ] **Step 1: Append Finance tab CSS**

```css
/* ============================================================
   FINANCE TAB
   ============================================================ */
.fin-bar-wrap { margin-bottom: 16px; }
.fin-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 0.87rem;
}
.fin-label span:first-child { color: #bbb; }
.fin-label span:last-child  { color: #555; font-size: 0.8rem; }
.fin-bar { height: 6px; border-radius: 3px; }

/* Summary card */
.fin-total-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  font-size: 0.87rem;
  color: #888;
}
.fin-total-row:last-child { border-bottom: none; }
.fin-total-row.bold { font-weight: 700; color: #fbbf24; font-size: 0.92rem; }

/* Expense tracker table */
.tracker-input {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  color: #ddd;
  width: 120px;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 0.82rem;
  transition: border-color 0.15s;
}
.tracker-input:focus {
  outline: none;
  border-color: rgba(251,191,36,0.4);
  background: rgba(251,191,36,0.04);
}
.diff-pos { color: #4ade80; }
.diff-neg { color: #f87171; }

/* Shared glass card used on this tab */
.goal-section {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 10px;
  padding: 12px 14px;
  margin-bottom: 8px;
  backdrop-filter: blur(8px);
}
```

- [ ] **Step 2: Switch to Finance tab — verify: amber salary text, progress bars colored by category, amber ИТОГО row, glass rule card, tracker inputs with amber focus ring**

---

### Task 6: Goals tab CSS

- [ ] **Step 1: Append Goals tab CSS**

```css
/* ============================================================
   GOALS TAB
   ============================================================ */
.goal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.goal-title { font-weight: 600; font-size: 0.95rem; color: #ddd; }
.goal-progress-text { font-size: 0.8rem; color: #555; }

.goal-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  cursor: pointer;
  font-size: 0.87rem;
  color: #888;
  transition: background 0.12s;
}
.goal-item:last-of-type { border-bottom: none; }
.goal-item:hover {
  background: rgba(255,255,255,0.03);
  border-radius: 4px;
  padding-left: 4px;
}
.goal-item.done span { text-decoration: line-through; color: #3a3a3a; }

/* Checkbox */
.goal-cb {
  width: 15px;
  height: 15px;
  border: 1.5px solid #252525;
  border-radius: 3px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  color: transparent;
  transition: background 0.15s, border-color 0.15s;
}
.goal-cb.checked {
  background: rgba(251,191,36,0.18);
  border-color: rgba(251,191,36,0.4);
  color: #fbbf24;
}

/* Mini progress bar per section */
.goal-mini-bar {
  height: 2px;
  background: rgba(255,255,255,0.05);
  border-radius: 1px;
  margin-top: 10px;
}
.goal-mini-fill {
  height: 100%;
  border-radius: 1px;
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
  transition: width 0.3s ease;
}

/* Overall progress */
#goals-bar {
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
  box-shadow: 0 0 8px rgba(251,191,36,0.3);
}
#goals-pct { color: #fbbf24; }

/* Close the <style> tag */
</style>
```

- [ ] **Step 2: Switch to Goals tab — verify 9 sections including ♟ Шахматы (100→1200), amber checkboxes, gradient mini-bars, amber overall progress**

---

### Task 7: Final QA + commit

- [ ] **Step 1: Full cross-tab QA checklist**

Open `index.html` in browser and verify:

| Check | Expected |
|-------|----------|
| Body background | `#0a0a0f`, 3 soft ambient glows visible at edges |
| Header | Name left, date pill right |
| Tabs | Glass container, amber active tab, grey inactive |
| Day tab | Glass rows, colored cat-strip, amber progress bar |
| Done rows | Strikethrough grey text, amber checkmark box |
| Martial day pills | Red-tinted border |
| Today day pill | Amber |
| Week tab | Cards as glass, martial days red left border, tags as pills |
| Finance tab | Amber salary, colored bars, amber ИТОГО |
| Tracker inputs | Dark glass, amber focus ring |
| Goals tab | 9 sections total (Sport, English, Russian, Quran, Vibe, Books, Rhetoric, Career, Chess) |
| Checkboxes | Amber when checked |
| Mini-bars | Amber gradient |
| localStorage | Check/uncheck persists on page reload |
| Mobile | Open DevTools → responsive, no horizontal overflow |

- [ ] **Step 2: Verify no JS console errors**

Open DevTools Console. Should be empty.

- [ ] **Step 3: Commit**

```bash
git init  # if not already a git repo
git add index.html docs/superpowers/specs/2026-03-18-dashboard-redesign.md docs/superpowers/plans/2026-03-18-dashboard-redesign.md
git commit -m "feat: glassmorphism redesign with amber accent"
```
