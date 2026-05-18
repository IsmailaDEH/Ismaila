/* ============================================================
   DAILY SCHEDULE MANAGER — app.js
   ============================================================ */
'use strict';

// ── State ────────────────────────────────────────────────────
const STORAGE_KEY = 'dailySchedule_tasks';

const CATEGORIES = {
  Work:     { color: '#818cf8', emoji: '💼' },
  Personal: { color: '#34d399', emoji: '🏠' },
  Health:   { color: '#f472b6', emoji: '💪' },
  Study:    { color: '#fb923c', emoji: '📚' },
  Social:   { color: '#38bdf8', emoji: '👥' },
  Other:    { color: '#a78bfa', emoji: '✨' },
};

const PRIORITY_COLORS = { High: '#f87171', Medium: '#fbbf24', Low: '#4ade80' };

const AppState = {
  tasks: [],
  currentDate: todayStr(),
  view: 'day',
  filterCategory: 'All',
  filterKeyword: '',
  miniCalDate: new Date(),
  dragTask: null,
  dragStartY: 0,
  dragOrigStart: '',
  notifGranted: false,
  notifTimers: {},
};

// ── Helpers ──────────────────────────────────────────────────
function todayStr() {
  return new Date().toISOString().slice(0, 10);
}

function uid() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
}

function timeToMinutes(t) {
  if (!t) return 0;
  const [h, m] = t.split(':').map(Number);
  return h * 60 + m;
}

function minutesToTime(mins) {
  const h = Math.floor(mins / 60) % 24;
  const m = mins % 60;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
}

function formatTime(t) {
  if (!t) return '';
  const [h, m] = t.split(':').map(Number);
  const ampm = h < 12 ? 'AM' : 'PM';
  const hh = h % 12 || 12;
  return `${hh}:${String(m).padStart(2, '0')} ${ampm}`;
}

function formatDate(dateStr) {
  const d = new Date(dateStr + 'T00:00:00');
  const today = todayStr();
  const tomorrow = new Date(); tomorrow.setDate(tomorrow.getDate() + 1);
  const tomorrowStr = tomorrow.toISOString().slice(0, 10);
  if (dateStr === today) return 'Today';
  if (dateStr === tomorrowStr) return 'Tomorrow';
  return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
}

function addDays(dateStr, n) {
  const d = new Date(dateStr + 'T00:00:00');
  d.setDate(d.getDate() + n);
  return d.toISOString().slice(0, 10);
}

function getWeekDays(dateStr) {
  const d = new Date(dateStr + 'T00:00:00');
  const day = d.getDay();
  const days = [];
  for (let i = 0; i < 7; i++) {
    const dd = new Date(d);
    dd.setDate(d.getDate() - day + i);
    days.push(dd.toISOString().slice(0, 10));
  }
  return days;
}

// ── Persistence ──────────────────────────────────────────────
function loadTasks() {
  try {
    AppState.tasks = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    AppState.tasks = [];
  }
  expandRecurring();
}

function saveTasks() {
  const base = AppState.tasks.filter(t => !t._virtual);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(base));
}

function expandRecurring() {
  const base = AppState.tasks.filter(t => !t._virtual);
  const today = todayStr();
  const future = addDays(today, 30);
  const virtual = [];

  base.forEach(task => {
    if (task.recurring === 'daily') {
      let d = addDays(task.date, 1);
      while (d <= future) {
        virtual.push({ ...task, id: task.id + '_' + d, date: d, _virtual: true, _parentId: task.id });
        d = addDays(d, 1);
      }
    } else if (task.recurring === 'weekly') {
      let d = addDays(task.date, 7);
      while (d <= future) {
        virtual.push({ ...task, id: task.id + '_' + d, date: d, _virtual: true, _parentId: task.id });
        d = addDays(d, 7);
      }
    }
  });

  AppState.tasks = [...base, ...virtual];
}

// ── DOM refs ─────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const qs = sel => document.querySelector(sel);

const els = {
  sidebar:        $('sidebar'),
  sidebarToggle:  $('sidebarToggle'),
  hamburger:      $('hamburger'),
  miniCalPrev:    $('miniCalPrev'),
  miniCalNext:    $('miniCalNext'),
  miniCalTitle:   $('miniCalTitle'),
  miniCalDays:    $('miniCalDays'),
  categoryFilters:$('categoryFilters'),
  weekStats:      $('weekStats'),
  prevDay:        $('prevDay'),
  nextDay:        $('nextDay'),
  datePicker:     $('datePicker'),
  dateLabel:      $('dateLabel'),
  todayBtn:       $('todayBtn'),
  searchInput:    $('searchInput'),
  clearSearch:    $('clearSearch'),
  dayViewBtn:     $('dayViewBtn'),
  weekViewBtn:    $('weekViewBtn'),
  exportBtn:      $('exportBtn'),
  notifBtn:       $('notifBtn'),
  statTotal:      $('statTotal'),
  statDone:       $('statDone'),
  statPending:    $('statPending'),
  progressCircle: $('progressCircle'),
  progressPct:    $('progressPct'),
  dayView:        $('dayView'),
  weekView:       $('weekView'),
  timeline:       $('timeline'),
  weekGrid:       $('weekGrid'),
  fab:            $('fab'),
  modalOverlay:   $('modalOverlay'),
  modalTitle:     $('modalTitle'),
  taskForm:       $('taskForm'),
  taskId:         $('taskId'),
  taskTitle:      $('taskTitle'),
  titleError:     $('titleError'),
  taskDate:       $('taskDate'),
  taskCategory:   $('taskCategory'),
  taskStart:      $('taskStart'),
  taskEnd:        $('taskEnd'),
  taskPriority:   $('taskPriority'),
  taskNotes:      $('taskNotes'),
  taskRecurring:  $('taskRecurring'),
  deleteTaskBtn:  $('deleteTaskBtn'),
  cancelTaskBtn:  $('cancelTaskBtn'),
  saveTaskBtn:    $('saveTaskBtn'),
  taskPopup:      $('taskPopup'),
  popupCategory:  $('popupCategory'),
  popupClose:     $('popupClose'),
  popupTitle:     $('popupTitle'),
  popupTime:      $('popupTime'),
  popupNotes:     $('popupNotes'),
  popupPriority:  $('popupPriority'),
  popupToggleDone:$('popupToggleDone'),
  popupEdit:      $('popupEdit'),
};

let _popupTaskId = null;

// ── Render ────────────────────────────────────────────────────
function render() {
  updateDateLabel();
  updateStats();
  updateMiniCal();
  updateCategoryFilters();
  updateWeekStats();

  if (AppState.view === 'day') {
    els.dayView.classList.remove('hidden');
    els.weekView.classList.add('hidden');
    renderTimeline();
  } else {
    els.dayView.classList.add('hidden');
    els.weekView.classList.remove('hidden');
    renderWeekView();
  }

  scheduleNotifications();
}

function filteredTasksForDate(dateStr) {
  return AppState.tasks.filter(t => {
    if (t.date !== dateStr) return false;
    if (AppState.filterCategory !== 'All' && t.category !== AppState.filterCategory) return false;
    if (AppState.filterKeyword) {
      const kw = AppState.filterKeyword.toLowerCase();
      if (!t.title.toLowerCase().includes(kw) && !(t.notes || '').toLowerCase().includes(kw)) return false;
    }
    return true;
  });
}

// ── Timeline ─────────────────────────────────────────────────
const HOUR_PX = 60;

function renderTimeline() {
  const tl = els.timeline;
  tl.innerHTML = '';

  // hour rows
  for (let h = 0; h < 24; h++) {
    const row = document.createElement('div');
    row.className = 'time-row';
    row.style.top = (h * HOUR_PX) + 'px';

    const label = document.createElement('div');
    label.className = 'time-label';
    label.textContent = h === 0 ? '12 AM' : h < 12 ? `${h} AM` : h === 12 ? '12 PM' : `${h - 12} PM`;

    const area = document.createElement('div');
    area.className = 'time-line-area';
    area.dataset.hour = h;
    area.addEventListener('click', e => {
      if (e.target !== area) return;
      openModal(null, `${String(h).padStart(2,'0')}:00`);
    });

    row.appendChild(label);
    row.appendChild(area);
    tl.appendChild(row);
  }

  // current time line
  const ctl = document.createElement('div');
  ctl.id = 'currentTimeLine';
  tl.appendChild(ctl);
  updateCurrentTimeLine();

  // tasks
  const tasks = filteredTasksForDate(AppState.currentDate);
  tasks.forEach(t => renderTaskCard(t, tl));

  tl.style.height = (24 * HOUR_PX + 20) + 'px';
}

function renderTaskCard(task, container) {
  const startMin = timeToMinutes(task.startTime);
  const endMin   = timeToMinutes(task.endTime) || startMin + 30;
  const duration = Math.max(endMin - startMin, 20);
  const top      = startMin * (HOUR_PX / 60);
  const height   = duration * (HOUR_PX / 60);

  const card = document.createElement('div');
  card.className = `task-card cat-${task.category}${task.done ? ' done' : ''}`;
  card.style.top    = top + 'px';
  card.style.height = Math.max(height, 28) + 'px';
  card.dataset.id   = task.id;

  card.innerHTML = `
    <div class="tc-title">${escHtml(task.title)}</div>
    ${height > 36 ? `<div class="tc-time">${formatTime(task.startTime)} – ${formatTime(task.endTime)}</div>` : ''}
    <div class="tc-priority-dot" style="background:${PRIORITY_COLORS[task.priority] || '#fff'}"></div>
  `;

  card.addEventListener('click', e => { e.stopPropagation(); showPopup(task.id); });
  makeDraggable(card, task);
  container.appendChild(card);
}

function updateCurrentTimeLine() {
  const ctl = $('currentTimeLine');
  if (!ctl) return;
  const now = new Date();
  const mins = now.getHours() * 60 + now.getMinutes();
  ctl.style.top = (mins * (HOUR_PX / 60)) + 'px';
}

// ── Drag & drop ───────────────────────────────────────────────
function makeDraggable(card, task) {
  let startY, startTop, isDragging = false;

  card.addEventListener('mousedown', e => {
    if (e.button !== 0) return;
    startY   = e.clientY;
    startTop = parseInt(card.style.top);
    isDragging = false;

    const onMove = ev => {
      const dy = ev.clientY - startY;
      if (!isDragging && Math.abs(dy) > 4) {
        isDragging = true;
        card.classList.add('dragging');
      }
      if (!isDragging) return;
      ev.preventDefault();
      const newTop = Math.max(0, startTop + dy);
      card.style.top = newTop + 'px';
    };

    const onUp = ev => {
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', onUp);
      if (!isDragging) return;
      card.classList.remove('dragging');

      const newTop  = parseInt(card.style.top);
      const newMins = Math.round((newTop / HOUR_PX) * 60);
      const clampedMins = Math.max(0, Math.min(23 * 60 + 59, newMins));

      const realTask = AppState.tasks.find(t => t.id === task.id);
      if (realTask) {
        const duration = timeToMinutes(realTask.endTime) - timeToMinutes(realTask.startTime);
        realTask.startTime = minutesToTime(clampedMins);
        realTask.endTime   = minutesToTime(clampedMins + Math.max(duration, 15));
        saveTasks();
        render();
      }
    };

    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onUp);
  });

  // Touch support
  card.addEventListener('touchstart', e => {
    startY   = e.touches[0].clientY;
    startTop = parseInt(card.style.top);
    isDragging = false;
  }, { passive: true });

  card.addEventListener('touchmove', e => {
    const dy = e.touches[0].clientY - startY;
    if (!isDragging && Math.abs(dy) > 4) {
      isDragging = true;
      card.classList.add('dragging');
    }
    if (!isDragging) return;
    e.preventDefault();
    card.style.top = Math.max(0, startTop + dy) + 'px';
  }, { passive: false });

  card.addEventListener('touchend', () => {
    if (!isDragging) return;
    card.classList.remove('dragging');
    const newTop  = parseInt(card.style.top);
    const newMins = Math.round((newTop / HOUR_PX) * 60);
    const clampedMins = Math.max(0, Math.min(23 * 60 + 59, newMins));

    const realTask = AppState.tasks.find(t => t.id === task.id);
    if (realTask) {
      const duration = timeToMinutes(realTask.endTime) - timeToMinutes(realTask.startTime);
      realTask.startTime = minutesToTime(clampedMins);
      realTask.endTime   = minutesToTime(clampedMins + Math.max(duration, 15));
      saveTasks();
      render();
    }
  });
}

// ── Week View ─────────────────────────────────────────────────
function renderWeekView() {
  const wg = els.weekGrid;
  wg.innerHTML = '';
  const days = getWeekDays(AppState.currentDate);
  const today = todayStr();

  // header row
  const corner = document.createElement('div');
  corner.className = 'wg-header';
  wg.appendChild(corner);

  days.forEach(d => {
    const dObj = new Date(d + 'T00:00:00');
    const isToday = d === today;
    const h = document.createElement('div');
    h.className = 'wg-day-header' + (isToday ? ' today' : '');
    const num = document.createElement('span');
    num.className = 'wg-day-num';
    num.textContent = dObj.getDate();
    h.appendChild(num);
    h.appendChild(Object.assign(document.createElement('span'), {
      textContent: dObj.toLocaleDateString('en-US', { weekday: 'short' }),
    }));
    h.addEventListener('click', () => {
      AppState.currentDate = d;
      AppState.view = 'day';
      els.dayViewBtn.classList.add('active');
      els.weekViewBtn.classList.remove('active');
      render();
    });
    wg.appendChild(h);
  });

  // hour rows
  for (let h = 0; h < 24; h++) {
    const tlabel = document.createElement('div');
    tlabel.className = 'wg-time-label';
    tlabel.textContent = h === 0 ? '12a' : h < 12 ? `${h}a` : h === 12 ? '12p' : `${h-12}p`;
    wg.appendChild(tlabel);

    days.forEach(d => {
      const cell = document.createElement('div');
      cell.className = 'wg-cell';
      cell.dataset.date = d;
      cell.dataset.hour = h;
      cell.addEventListener('click', e => {
        if (e.target !== cell) return;
        AppState.currentDate = d;
        openModal(null, `${String(h).padStart(2,'0')}:00`);
      });

      // tasks that start in this hour
      filteredTasksForDate(d)
        .filter(t => Math.floor(timeToMinutes(t.startTime) / 60) === h)
        .forEach(t => {
          const chip = document.createElement('div');
          chip.className = `wg-task-chip cat-${t.category}${t.done ? ' done' : ''}`;
          chip.textContent = t.title;
          chip.addEventListener('click', e => { e.stopPropagation(); showPopup(t.id); });
          cell.appendChild(chip);
        });

      wg.appendChild(cell);
    });
  }
}

// ── Stats ─────────────────────────────────────────────────────
function updateStats() {
  const tasks = filteredTasksForDate(AppState.currentDate);
  const total  = tasks.length;
  const done   = tasks.filter(t => t.done).length;
  const pct    = total ? Math.round((done / total) * 100) : 0;
  const circumf = 138.23;

  els.statTotal.querySelector('.stat-num').textContent   = total;
  els.statDone.querySelector('.stat-num').textContent    = done;
  els.statPending.querySelector('.stat-num').textContent = total - done;
  els.progressPct.textContent                            = pct + '%';
  els.progressCircle.style.strokeDashoffset              = circumf - (circumf * pct / 100);
}

function updateWeekStats() {
  const days = getWeekDays(AppState.currentDate);
  const stats = days.map(d => {
    const t = AppState.tasks.filter(x => x.date === d);
    return { d, total: t.length, done: t.filter(x => x.done).length };
  });
  const maxTotal = Math.max(...stats.map(s => s.total), 1);

  els.weekStats.innerHTML = stats.map(s => {
    const dObj = new Date(s.d + 'T00:00:00');
    const label = dObj.toLocaleDateString('en-US', { weekday: 'short' });
    const pct = Math.round((s.total / maxTotal) * 100);
    return `<div class="week-stat-row">
      <span class="ws-label">${label}</span>
      <div class="ws-bar"><div class="ws-bar-fill" style="width:${pct}%"></div></div>
      <span class="ws-val">${s.done}/${s.total}</span>
    </div>`;
  }).join('');
}

// ── Date label ───────────────────────────────────────────────
function updateDateLabel() {
  els.dateLabel.textContent = formatDate(AppState.currentDate);
  els.datePicker.value = AppState.currentDate;
}

// ── Mini Calendar ─────────────────────────────────────────────
function updateMiniCal() {
  const mc = AppState.miniCalDate;
  const year = mc.getFullYear(), month = mc.getMonth();
  els.miniCalTitle.textContent = mc.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const daysInPrev  = new Date(year, month, 0).getDate();

  const today = todayStr();
  const taskDates = new Set(AppState.tasks.map(t => t.date));

  let html = '';

  for (let i = firstDay - 1; i >= 0; i--) {
    const d = new Date(year, month - 1, daysInPrev - i);
    const ds = d.toISOString().slice(0, 10);
    html += `<div class="mini-cal-day other-month${ds === AppState.currentDate ? ' selected' : ''}" data-date="${ds}">${daysInPrev - i}</div>`;
  }

  for (let d = 1; d <= daysInMonth; d++) {
    const date = new Date(year, month, d);
    const ds = date.toISOString().slice(0, 10);
    const cls = [
      'mini-cal-day',
      ds === today ? 'today' : '',
      ds === AppState.currentDate ? 'selected' : '',
      taskDates.has(ds) ? 'has-tasks' : '',
    ].filter(Boolean).join(' ');
    html += `<div class="${cls}" data-date="${ds}">${d}</div>`;
  }

  const filled = firstDay + daysInMonth;
  const remaining = filled % 7 === 0 ? 0 : 7 - (filled % 7);
  for (let d = 1; d <= remaining; d++) {
    const date = new Date(year, month + 1, d);
    const ds = date.toISOString().slice(0, 10);
    html += `<div class="mini-cal-day other-month${ds === AppState.currentDate ? ' selected' : ''}" data-date="${ds}">${d}</div>`;
  }

  els.miniCalDays.innerHTML = html;
  els.miniCalDays.querySelectorAll('.mini-cal-day').forEach(el => {
    el.addEventListener('click', () => {
      AppState.currentDate = el.dataset.date;
      render();
    });
  });
}

// ── Category Filters ──────────────────────────────────────────
function updateCategoryFilters() {
  const counts = {};
  Object.keys(CATEGORIES).forEach(c => { counts[c] = 0; });
  AppState.tasks.forEach(t => { if (counts[t.category] !== undefined) counts[t.category]++; });

  const all = AppState.tasks.length;
  let html = `<button class="cat-filter-btn${AppState.filterCategory === 'All' ? ' active' : ''}" data-cat="All">
    <span class="cat-dot" style="background:#fff"></span>All
    <span class="cat-count">${all}</span>
  </button>`;

  Object.entries(CATEGORIES).forEach(([name, cfg]) => {
    html += `<button class="cat-filter-btn${AppState.filterCategory === name ? ' active' : ''}" data-cat="${name}">
      <span class="cat-dot" style="background:${cfg.color}"></span>${cfg.emoji} ${name}
      <span class="cat-count">${counts[name]}</span>
    </button>`;
  });

  els.categoryFilters.innerHTML = html;
  els.categoryFilters.querySelectorAll('.cat-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      AppState.filterCategory = btn.dataset.cat;
      render();
    });
  });
}

// ── Modal ─────────────────────────────────────────────────────
function openModal(taskId = null, defaultTime = null) {
  els.modalOverlay.classList.remove('hidden');
  els.titleError.classList.add('hidden');
  els.taskTitle.classList.remove('error');
  els.taskPopup.classList.add('hidden');

  if (taskId) {
    const t = AppState.tasks.find(x => x.id === taskId);
    if (!t) return;
    els.modalTitle.textContent  = 'Edit Task';
    els.taskId.value            = taskId;
    els.taskTitle.value         = t.title;
    els.taskDate.value          = t.date;
    els.taskCategory.value      = t.category;
    els.taskStart.value         = t.startTime;
    els.taskEnd.value           = t.endTime;
    els.taskPriority.value      = t.priority;
    els.taskNotes.value         = t.notes || '';
    els.taskRecurring.value     = t.recurring || 'none';
    els.deleteTaskBtn.classList.remove('hidden');
  } else {
    els.modalTitle.textContent  = 'Add Task';
    els.taskId.value            = '';
    els.taskTitle.value         = '';
    els.taskDate.value          = AppState.currentDate;
    els.taskCategory.value      = 'Work';
    els.taskStart.value         = defaultTime || currentTimeRounded();
    els.taskEnd.value           = addMinutesToTime(els.taskStart.value, 60);
    els.taskPriority.value      = 'Medium';
    els.taskNotes.value         = '';
    els.taskRecurring.value     = 'none';
    els.deleteTaskBtn.classList.add('hidden');
  }

  requestAnimationFrame(() => els.taskTitle.focus());
}

function closeModal() {
  els.modalOverlay.classList.add('hidden');
}

function currentTimeRounded() {
  const now = new Date();
  const mins = Math.ceil((now.getHours() * 60 + now.getMinutes()) / 30) * 30;
  return minutesToTime(mins % (24 * 60));
}

function addMinutesToTime(t, mins) {
  return minutesToTime(timeToMinutes(t) + mins);
}

function saveTask(e) {
  e.preventDefault();
  const title = els.taskTitle.value.trim();
  if (!title) {
    els.titleError.classList.remove('hidden');
    els.taskTitle.focus();
    return;
  }
  els.titleError.classList.add('hidden');

  const id = els.taskId.value || uid();
  const isEdit = Boolean(els.taskId.value);

  const task = {
    id,
    title,
    date:       els.taskDate.value,
    category:   els.taskCategory.value,
    startTime:  els.taskStart.value,
    endTime:    els.taskEnd.value,
    priority:   els.taskPriority.value,
    notes:      els.taskNotes.value.trim(),
    recurring:  els.taskRecurring.value,
    done:       isEdit ? (AppState.tasks.find(t => t.id === id)?.done || false) : false,
  };

  if (isEdit) {
    const idx = AppState.tasks.findIndex(t => t.id === id);
    if (idx >= 0) AppState.tasks[idx] = task;
  } else {
    AppState.tasks.push(task);
  }

  saveTasks();
  expandRecurring();
  closeModal();
  render();
}

function deleteTask(id) {
  AppState.tasks = AppState.tasks.filter(t => t.id !== id && t._parentId !== id);
  saveTasks();
  expandRecurring();
  closeModal();
  render();
}

// ── Popup ─────────────────────────────────────────────────────
function showPopup(taskId) {
  const t = AppState.tasks.find(x => x.id === taskId);
  if (!t) return;
  _popupTaskId = taskId;

  const cfg = CATEGORIES[t.category] || CATEGORIES.Other;
  els.popupCategory.textContent = `${cfg.emoji} ${t.category}`;
  els.popupCategory.style.background = cfg.color + '28';
  els.popupCategory.style.color = cfg.color;
  els.popupTitle.textContent = t.title;
  els.popupTime.textContent  = `${formatTime(t.startTime)} – ${formatTime(t.endTime)}`;
  els.popupNotes.textContent = t.notes || '';
  els.popupNotes.style.display = t.notes ? '' : 'none';
  els.popupPriority.textContent = t.priority;
  els.popupPriority.style.color = PRIORITY_COLORS[t.priority];
  els.popupToggleDone.textContent = t.done ? 'Mark Undone' : 'Mark Done';

  els.taskPopup.classList.remove('hidden');
}

function toggleTaskDone(id) {
  const t = AppState.tasks.find(x => x.id === id);
  if (!t) return;
  t.done = !t.done;
  saveTasks();
  render();
  if (_popupTaskId === id) showPopup(id);
}

// ── Notifications ─────────────────────────────────────────────
async function requestNotifications() {
  if (!('Notification' in window)) return;
  const perm = await Notification.requestPermission();
  AppState.notifGranted = perm === 'granted';
  els.notifBtn.style.color = AppState.notifGranted ? 'var(--success)' : '';
  if (AppState.notifGranted) scheduleNotifications();
}

function scheduleNotifications() {
  if (!AppState.notifGranted) return;
  Object.values(AppState.notifTimers).forEach(clearTimeout);
  AppState.notifTimers = {};

  const now = Date.now();
  AppState.tasks
    .filter(t => t.date === todayStr() && !t.done)
    .forEach(t => {
      const taskTime = new Date(`${t.date}T${t.startTime}:00`).getTime();
      const notifTime = taskTime - 10 * 60 * 1000;
      const delay = notifTime - now;
      if (delay > 0 && delay < 24 * 3600 * 1000) {
        AppState.notifTimers[t.id] = setTimeout(() => {
          new Notification(`⏰ Upcoming: ${t.title}`, {
            body: `Starts at ${formatTime(t.startTime)}`,
            icon: 'https://api.iconify.design/twemoji/alarm-clock.svg',
          });
        }, delay);
      }
    });
}

// ── Export ────────────────────────────────────────────────────
function exportTasks() {
  const data = JSON.stringify(AppState.tasks.filter(t => !t._virtual), null, 2);
  const blob = new Blob([data], { type: 'application/json' });
  const url  = URL.createObjectURL(blob);
  const a = Object.assign(document.createElement('a'), {
    href: url,
    download: `schedule-${AppState.currentDate}.json`,
  });
  a.click();
  URL.revokeObjectURL(url);
}

// ── Utility ───────────────────────────────────────────────────
function escHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ── Event Listeners ───────────────────────────────────────────
function initEvents() {
  // Sidebar toggle
  els.sidebarToggle.addEventListener('click', () => els.sidebar.classList.toggle('collapsed'));
  els.hamburger.addEventListener('click',     () => els.sidebar.classList.toggle('collapsed'));

  // Mini cal nav
  els.miniCalPrev.addEventListener('click', () => {
    AppState.miniCalDate.setMonth(AppState.miniCalDate.getMonth() - 1);
    updateMiniCal();
  });
  els.miniCalNext.addEventListener('click', () => {
    AppState.miniCalDate.setMonth(AppState.miniCalDate.getMonth() + 1);
    updateMiniCal();
  });

  // Date nav
  els.prevDay.addEventListener('click',    () => { AppState.currentDate = addDays(AppState.currentDate, -1); render(); });
  els.nextDay.addEventListener('click',    () => { AppState.currentDate = addDays(AppState.currentDate,  1); render(); });
  els.todayBtn.addEventListener('click',   () => { AppState.currentDate = todayStr(); render(); });
  els.datePicker.addEventListener('change', e => { AppState.currentDate = e.target.value; render(); });

  // Search
  els.searchInput.addEventListener('input', e => {
    AppState.filterKeyword = e.target.value;
    els.clearSearch.classList.toggle('hidden', !e.target.value);
    render();
  });
  els.clearSearch.addEventListener('click', () => {
    els.searchInput.value = '';
    AppState.filterKeyword = '';
    els.clearSearch.classList.add('hidden');
    render();
  });

  // View toggle
  els.dayViewBtn.addEventListener('click',  () => { AppState.view = 'day';  els.dayViewBtn.classList.add('active'); els.weekViewBtn.classList.remove('active'); render(); });
  els.weekViewBtn.addEventListener('click', () => { AppState.view = 'week'; els.weekViewBtn.classList.add('active'); els.dayViewBtn.classList.remove('active'); render(); });

  // Export
  els.exportBtn.addEventListener('click', exportTasks);

  // Notifications
  els.notifBtn.addEventListener('click', requestNotifications);

  // FAB
  els.fab.addEventListener('click', () => openModal());

  // Modal
  els.modalClose.addEventListener('click',    closeModal);
  els.cancelTaskBtn.addEventListener('click', closeModal);
  els.modalOverlay.addEventListener('click',  e => { if (e.target === els.modalOverlay) closeModal(); });
  els.taskForm.addEventListener('submit',     saveTask);
  els.deleteTaskBtn.addEventListener('click', () => deleteTask(els.taskId.value));

  // Popup
  els.popupClose.addEventListener('click', () => els.taskPopup.classList.add('hidden'));
  els.popupToggleDone.addEventListener('click', () => toggleTaskDone(_popupTaskId));
  els.popupEdit.addEventListener('click', () => {
    els.taskPopup.classList.add('hidden');
    openModal(_popupTaskId);
  });

  // Keyboard shortcuts
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeModal(); els.taskPopup.classList.add('hidden'); }
    if (e.key === 'n' && !e.ctrlKey && !e.metaKey && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') openModal();
  });

  // Auto-update current time line every minute
  setInterval(() => {
    updateCurrentTimeLine();
    if (AppState.currentDate === todayStr()) scheduleNotifications();
  }, 60_000);
}

// ── Seed demo tasks ───────────────────────────────────────────
function seedDemoTasks() {
  if (AppState.tasks.length) return;
  const today = todayStr();
  const demos = [
    { title: 'Morning standup', date: today, startTime: '09:00', endTime: '09:30', category: 'Work',     priority: 'High',   notes: 'Daily sync with the team', recurring: 'daily' },
    { title: 'Deep work session', date: today, startTime: '10:00', endTime: '12:00', category: 'Work',   priority: 'High',   notes: '',                          recurring: 'none' },
    { title: 'Lunch break',      date: today, startTime: '12:00', endTime: '13:00', category: 'Personal',priority: 'Low',    notes: '',                          recurring: 'daily' },
    { title: 'Gym workout',      date: today, startTime: '07:00', endTime: '08:00', category: 'Health',  priority: 'Medium', notes: 'Chest & triceps',           recurring: 'none' },
    { title: 'Read chapter 3',   date: today, startTime: '20:00', endTime: '21:00', category: 'Study',   priority: 'Medium', notes: 'Clean Code by Robert Martin', recurring: 'none' },
    { title: 'Team dinner',      date: addDays(today, 1), startTime: '19:00', endTime: '21:00', category: 'Social', priority: 'Low', notes: 'Downtown restaurant', recurring: 'none' },
  ];
  demos.forEach(d => AppState.tasks.push({ id: uid(), done: false, ...d }));
  saveTasks();
  expandRecurring();
}

// ── Bootstrap ─────────────────────────────────────────────────
function init() {
  loadTasks();
  seedDemoTasks();
  initEvents();
  render();

  // Scroll to current hour on day view
  setTimeout(() => {
    const h = new Date().getHours();
    const wrap = els.dayView;
    wrap.scrollTop = Math.max(0, (h - 1) * HOUR_PX - 40);
  }, 100);

  // Check notif permission
  if (Notification?.permission === 'granted') {
    AppState.notifGranted = true;
    els.notifBtn.style.color = 'var(--success)';
    scheduleNotifications();
  }
}

document.addEventListener('DOMContentLoaded', init);
