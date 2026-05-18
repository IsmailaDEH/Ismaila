/* =====================================================================
   DayFlow — app.js   (Pure Vanilla JS, ES6+)
   ===================================================================== */
'use strict';

/* ====================================================================
   CONSTANTS & CONFIG
   ==================================================================== */
const LS_KEY = 'dailySchedule_tasks';
const HOUR_H = 60; // px per hour in timeline

const CATEGORY_COLORS = {
  work:     '#6366f1',
  personal: '#ec4899',
  health:   '#22c55e',
  study:    '#f59e0b',
  social:   '#06b6d4',
  other:    '#a78bfa',
};

const PRIORITY_LABELS = { high: 'High', medium: 'Medium', low: 'Low' };
const PRIORITY_COLORS = { high: '#ef4444', medium: '#f59e0b', low: '#22c55e' };

const DAYS_SHORT  = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
const MONTHS_LONG = ['January','February','March','April','May','June',
                     'July','August','September','October','November','December'];

/* ====================================================================
   STATE
   ==================================================================== */
const AppState = {
  tasks:           [],          // all persisted tasks
  currentDate:     new Date(),  // currently viewed date
  view:            'day',       // 'day' | 'week'
  miniCalDate:     new Date(),  // month shown in mini-cal
  filter:          { cat: 'all', keyword: '' },
  notifEnabled:    false,
  notifTimers:     {},          // taskId → timerId
  dragging:        null,        // { taskId, startY, origTop, origStartMin }
  editingId:       null,        // task being edited
};

/* ====================================================================
   UTILITIES
   ==================================================================== */
function genId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

function toDateStr(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function todayStr() { return toDateStr(new Date()); }

function parseDate(str) {
  // "YYYY-MM-DD" → Date (local)
  const [y, m, d] = str.split('-').map(Number);
  return new Date(y, m - 1, d);
}

function timeToMin(t) {
  if (!t) return 0;
  const [h, m] = t.split(':').map(Number);
  return h * 60 + (m || 0);
}

function minToTime(m) {
  const h = Math.floor(m / 60) % 24;
  const min = m % 60;
  return `${String(h).padStart(2,'0')}:${String(min).padStart(2,'0')}`;
}

function formatTime(t) {
  if (!t) return '';
  const [h, m] = t.split(':').map(Number);
  const ampm = h >= 12 ? 'PM' : 'AM';
  const h12 = h % 12 || 12;
  return `${h12}:${String(m).padStart(2,'0')} ${ampm}`;
}

function formatDateLong(date) {
  const dow = DAYS_SHORT[date.getDay()];
  const mon = MONTHS_LONG[date.getMonth()];
  return `${dow}, ${mon} ${date.getDate()}, ${date.getFullYear()}`;
}

function addDays(date, n) {
  const d = new Date(date);
  d.setDate(d.getDate() + n);
  return d;
}

function startOfWeek(date) {
  const d = new Date(date);
  d.setDate(d.getDate() - d.getDay());
  return d;
}

function isSameDay(a, b) {
  return a.getFullYear() === b.getFullYear() &&
         a.getMonth()    === b.getMonth()    &&
         a.getDate()     === b.getDate();
}

function clamp(val, min, max) { return Math.max(min, Math.min(max, val)); }

/* ====================================================================
   LOCAL STORAGE
   ==================================================================== */
function saveTasks() {
  try {
    localStorage.setItem(LS_KEY, JSON.stringify(AppState.tasks));
  } catch (e) { console.warn('LocalStorage write failed', e); }
}

function loadTasks() {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (raw) AppState.tasks = JSON.parse(raw);
  } catch (e) {
    AppState.tasks = [];
  }
}

/* ====================================================================
   RECURRING: EXPAND
   When we need tasks for a date, we expand recurring tasks that originated
   before or on that date.
   ==================================================================== */
function getTasksForDate(dateStr) {
  const date = parseDate(dateStr);
  const results = [];

  for (const t of AppState.tasks) {
    if (t.recurring === 'none' || !t.recurring) {
      if (t.date === dateStr) results.push(t);
    } else if (t.recurring === 'daily') {
      if (t.date <= dateStr) {
        // check if there's a completion override for this date
        const overrideKey = `${t.id}_${dateStr}`;
        const done = t.completionOverrides?.[dateStr] ?? false;
        results.push({ ...t, _virtualDate: dateStr, _done: done, _oid: overrideKey });
      }
    } else if (t.recurring === 'weekly') {
      const orig = parseDate(t.date);
      if (t.date <= dateStr && orig.getDay() === date.getDay()) {
        const done = t.completionOverrides?.[dateStr] ?? false;
        results.push({ ...t, _virtualDate: dateStr, _done: done });
      }
    }
  }

  return results;
}

function getEffectiveDone(task) {
  if (task._virtualDate) return task._done ?? false;
  return task.done ?? false;
}

/* ====================================================================
   TASK CRUD
   ==================================================================== */
function createTask(data) {
  const task = {
    id:         genId(),
    title:      data.title.trim(),
    date:       data.date,
    start:      data.start,
    end:        data.end,
    category:   data.category || 'other',
    priority:   data.priority || 'medium',
    notes:      data.notes || '',
    recurring:  data.recurring || 'none',
    done:       data.done || false,
    completionOverrides: {},
    createdAt:  Date.now(),
  };
  AppState.tasks.push(task);
  saveTasks();
  scheduleNotification(task);
  return task;
}

function updateTask(id, data) {
  const idx = AppState.tasks.findIndex(t => t.id === id);
  if (idx < 0) return;
  Object.assign(AppState.tasks[idx], data, { id });
  saveTasks();
  clearNotification(id);
  scheduleNotification(AppState.tasks[idx]);
}

function deleteTask(id) {
  AppState.tasks = AppState.tasks.filter(t => t.id !== id);
  saveTasks();
  clearNotification(id);
}

function toggleTaskDone(taskId, virtualDate) {
  const task = AppState.tasks.find(t => t.id === taskId);
  if (!task) return;
  if (virtualDate && task.recurring !== 'none') {
    task.completionOverrides = task.completionOverrides || {};
    task.completionOverrides[virtualDate] = !task.completionOverrides[virtualDate];
  } else {
    task.done = !task.done;
  }
  saveTasks();
}

/* ====================================================================
   NOTIFICATIONS
   ==================================================================== */
async function requestNotifPermission() {
  if (!('Notification' in window)) return false;
  if (Notification.permission === 'granted') return true;
  const p = await Notification.requestPermission();
  return p === 'granted';
}

function scheduleNotification(task) {
  if (!AppState.notifEnabled) return;
  if (task.recurring !== 'none') return; // only non-recurring for now
  const dateStr = task.date;
  const startMin = timeToMin(task.start);
  const notifMin = startMin - 10;
  if (notifMin < 0) return;

  const [y, m, d] = dateStr.split('-').map(Number);
  const notifTime = new Date(y, m - 1, d, Math.floor(notifMin / 60), notifMin % 60, 0, 0);
  const now = Date.now();
  const ms = notifTime.getTime() - now;
  if (ms <= 0) return;

  clearNotification(task.id);
  AppState.notifTimers[task.id] = setTimeout(() => {
    if (!task.done) {
      new Notification(`⏰ Starting in 10 min: ${task.title}`, {
        body: `${formatTime(task.start)} – ${formatTime(task.end)}`,
        icon: 'https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined/schedule/default/24px.svg',
      });
    }
  }, ms);
}

function clearNotification(id) {
  if (AppState.notifTimers[id]) {
    clearTimeout(AppState.notifTimers[id]);
    delete AppState.notifTimers[id];
  }
}

function rescheduleAllNotifications() {
  Object.keys(AppState.notifTimers).forEach(clearNotification);
  AppState.tasks.forEach(scheduleNotification);
}

/* ====================================================================
   TOAST
   ==================================================================== */
function showToast(msg, type = 'info', duration = 2800) {
  const area = document.getElementById('toastArea');
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.textContent = msg;
  area.appendChild(el);
  setTimeout(() => {
    el.classList.add('out');
    el.addEventListener('animationend', () => el.remove());
  }, duration);
}

/* ====================================================================
   FILTERING
   ==================================================================== */
function applyFilters(tasks) {
  const { cat, keyword } = AppState.filter;
  return tasks.filter(t => {
    if (cat !== 'all' && t.category !== cat) return false;
    if (keyword) {
      const kw = keyword.toLowerCase();
      if (!t.title.toLowerCase().includes(kw) &&
          !t.notes.toLowerCase().includes(kw)) return false;
    }
    return true;
  });
}

/* ====================================================================
   STATS
   ==================================================================== */
function updateStats() {
  const dateStr  = toDateStr(AppState.currentDate);
  const todayTasks = getTasksForDate(dateStr);
  const visible = applyFilters(todayTasks);
  const total   = visible.length;
  const done    = visible.filter(t => getEffectiveDone(t)).length;
  const pending = total - done;
  const pct     = total > 0 ? Math.round((done / total) * 100) : 0;

  document.getElementById('statTotal').textContent   = total;
  document.getElementById('statDone').textContent    = done;
  document.getElementById('statPending').textContent = pending;
  document.getElementById('statPct').textContent     = pct + '%';

  // progress ring: circumference = 2π*21 ≈ 131.9
  const circ   = 131.9;
  const offset = circ - (pct / 100) * circ;
  document.getElementById('progressRing').style.strokeDashoffset = offset;

  // Week stats
  const weekStart = startOfWeek(AppState.currentDate);
  let wTotal = 0, wDone = 0;
  const dayBars = [];
  for (let i = 0; i < 7; i++) {
    const d = addDays(weekStart, i);
    const ds = toDateStr(d);
    const dt = getTasksForDate(ds);
    wTotal += dt.length;
    wDone  += dt.filter(t => getEffectiveDone(t)).length;
    dayBars.push({ label: DAYS_SHORT[d.getDay()].slice(0,1), total: dt.length, done: dt.filter(t => getEffectiveDone(t)).length, dateStr: ds });
  }
  document.getElementById('weekTotal').textContent = wTotal;
  document.getElementById('weekDone').textContent  = wDone;
  const wPct = wTotal > 0 ? Math.round((wDone / wTotal) * 100) : 0;
  document.getElementById('weekPct').textContent   = wPct + '%';

  // Week bar chart
  const barRow = document.getElementById('weekBarRow');
  const maxT   = Math.max(1, ...dayBars.map(b => b.total));
  barRow.innerHTML = '';
  dayBars.forEach(b => {
    const col = document.createElement('div');
    col.className = 'week-bar-col';
    const bar = document.createElement('div');
    bar.className = 'week-bar';
    bar.title = `${b.label}: ${b.total} tasks`;
    bar.addEventListener('click', () => {
      AppState.currentDate = parseDate(b.dateStr);
      refreshAll();
    });
    const fill = document.createElement('div');
    fill.className = 'week-bar-fill';
    const heightPct = (b.total / maxT) * 100;
    fill.style.height = heightPct + '%';
    bar.appendChild(fill);
    const lbl = document.createElement('div');
    lbl.className = 'week-bar-lbl';
    lbl.textContent = b.label;
    col.appendChild(bar);
    col.appendChild(lbl);
    barRow.appendChild(col);
  });

  // Category counts
  const allTasksForDate = getTasksForDate(dateStr);
  const cats = ['work','personal','health','study','social','other'];
  document.getElementById('catCount-all').textContent = allTasksForDate.length;
  cats.forEach(c => {
    const el = document.getElementById(`catCount-${c}`);
    if (el) el.textContent = allTasksForDate.filter(t => t.category === c).length;
  });
}

/* ====================================================================
   MINI CALENDAR
   ==================================================================== */
function renderMiniCal() {
  const mc   = AppState.miniCalDate;
  const year = mc.getFullYear();
  const mon  = mc.getMonth();

  document.getElementById('miniCalTitle').textContent =
    `${MONTHS_LONG[mon].slice(0,3)} ${year}`;

  const container = document.getElementById('miniCalDays');
  container.innerHTML = '';

  const firstDay = new Date(year, mon, 1).getDay();
  const daysInMonth = new Date(year, mon + 1, 0).getDate();
  const today = new Date();
  const selStr = toDateStr(AppState.currentDate);

  // Previous month filler
  const prevDays = new Date(year, mon, 0).getDate();
  for (let i = firstDay - 1; i >= 0; i--) {
    const day = document.createElement('div');
    day.className = 'mini-cal-day other-month';
    day.textContent = prevDays - i;
    container.appendChild(day);
  }

  // This month
  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `${year}-${String(mon + 1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    const day = document.createElement('div');
    day.className = 'mini-cal-day';
    day.textContent = d;
    if (isSameDay(new Date(year, mon, d), today)) day.classList.add('today');
    if (dateStr === selStr) day.classList.add('selected');
    if (getTasksForDate(dateStr).length > 0) day.classList.add('has-tasks');
    day.addEventListener('click', () => {
      AppState.currentDate = new Date(year, mon, d);
      refreshAll();
    });
    container.appendChild(day);
  }

  // Next month filler
  const remaining = 42 - (firstDay + daysInMonth);
  for (let d = 1; d <= remaining; d++) {
    const day = document.createElement('div');
    day.className = 'mini-cal-day other-month';
    day.textContent = d;
    container.appendChild(day);
  }
}

/* ====================================================================
   TOPBAR DATE
   ==================================================================== */
function updateDateHeading() {
  const d = AppState.currentDate;
  document.getElementById('dateHeading').textContent = formatDateLong(d);
  document.getElementById('datePicker').value = toDateStr(d);
}

/* ====================================================================
   TIMELINE (DAY VIEW)
   ==================================================================== */
function buildTimeline() {
  const tl = document.getElementById('timeline');
  tl.innerHTML = '';

  for (let h = 0; h < 24; h++) {
    const row = document.createElement('div');
    row.className = 'hour-row';
    row.dataset.hour = h;

    const lbl = document.createElement('div');
    lbl.className = 'hour-label';
    lbl.textContent = h === 0 ? '12 AM' : h < 12 ? `${h} AM` : h === 12 ? '12 PM' : `${h - 12} PM`;

    const content = document.createElement('div');
    content.className = 'hour-content';

    row.appendChild(lbl);
    row.appendChild(content);

    // Click to add task
    row.addEventListener('click', (e) => {
      if (e.target.closest('.task-card')) return;
      openFormModal(null, { startHour: h });
    });

    // Drag-over
    row.addEventListener('dragover', handleDragOver);
    row.addEventListener('drop', handleDrop);
    row.addEventListener('dragleave', handleDragLeave);

    tl.appendChild(row);
  }
}

function renderTimeline() {
  // Clear old task cards
  document.querySelectorAll('.task-card').forEach(el => el.remove());

  const dateStr = toDateStr(AppState.currentDate);
  const tasks   = applyFilters(getTasksForDate(dateStr));

  // Group overlapping tasks into columns
  const placed  = placeTasks(tasks);
  const tl = document.getElementById('timeline');

  placed.forEach(({ task, col, cols }) => {
    const card = makeTaskCard(task, col, cols);
    tl.appendChild(card);
  });

  positionTimeNowBar();
}

// Simple greedy overlap placement
function placeTasks(tasks) {
  // Sort by start time
  const sorted = [...tasks].sort((a, b) => timeToMin(a.start) - timeToMin(b.start));
  const columns = []; // each column = array of tasks (as time ranges)
  const result  = [];

  sorted.forEach(task => {
    const sMin = timeToMin(task.start);
    const eMin = timeToMin(task.end) || sMin + 30;

    let placed = false;
    for (let c = 0; c < columns.length; c++) {
      const last = columns[c][columns[c].length - 1];
      if (timeToMin(last.end) <= sMin) {
        columns[c].push(task);
        result.push({ task, col: c });
        placed = true;
        break;
      }
    }
    if (!placed) {
      columns.push([task]);
      result.push({ task, col: columns.length - 1 });
    }
  });

  // Assign total cols count per task
  return result.map(r => ({ ...r, cols: columns.length }));
}

function makeTaskCard(task, col, cols) {
  const sMin = timeToMin(task.start);
  const eMin = timeToMin(task.end) || sMin + 30;
  const duration = Math.max(eMin - sMin, 15);

  const top  = (sMin / 60) * HOUR_H;
  const h    = (duration / 60) * HOUR_H;
  const done = getEffectiveDone(task);

  const card = document.createElement('div');
  card.className = `task-card tc-cat-${task.category}${done ? ' completed' : ''}`;
  card.style.top    = `${top}px`;
  card.style.height = `${Math.max(h, 24)}px`;
  card.dataset.id   = task.id;
  if (task._virtualDate) card.dataset.virtualDate = task._virtualDate;

  // Column positioning
  if (cols > 1) {
    const colW = (100 - 24) / cols; // leave room for check btn
    card.style.left  = `${4 + col * colW}%`;
    card.style.right = `${4 + (cols - col - 1) * colW}%`;
    card.style.width = 'auto';
  }

  // Priority dot
  const priDot = PRIORITY_COLORS[task.priority] || '#888';

  card.innerHTML = `
    <div class="tc-title">
      <span style="display:inline-block;width:7px;height:7px;border-radius:50%;
        background:${priDot};margin-right:5px;flex-shrink:0;vertical-align:middle;"></span>${escHtml(task.title)}
    </div>
    <div class="tc-time">${formatTime(task.start)}${task.end ? ' – ' + formatTime(task.end) : ''}</div>
    <div class="tc-check" data-id="${task.id}" data-vdate="${task._virtualDate || ''}">
      <svg width="9" height="9" viewBox="0 0 9 9" fill="none" aria-hidden="true">
        <path d="M1 4.5L3.5 7 8 2" stroke="white" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
  `;

  // Click → detail
  card.addEventListener('click', (e) => {
    if (e.target.closest('.tc-check')) {
      e.stopPropagation();
      const vd = task._virtualDate || null;
      toggleTaskDone(task.id, vd);
      refreshAll();
      return;
    }
    openDetailModal(task.id, task._virtualDate);
  });

  // Drag
  card.setAttribute('draggable', 'true');
  card.addEventListener('dragstart', handleDragStart);
  card.addEventListener('dragend',   handleDragEnd);

  return card;
}

function positionTimeNowBar() {
  const bar = document.getElementById('timeNowBar');
  const now = new Date();
  if (!isSameDay(now, AppState.currentDate)) {
    bar.classList.add('hidden');
    return;
  }
  bar.classList.remove('hidden');
  const totalMin = now.getHours() * 60 + now.getMinutes();
  const top = (totalMin / 60) * HOUR_H;
  bar.style.top = `${top}px`;
}

/* ====================================================================
   WEEK VIEW
   ==================================================================== */
function renderWeekView() {
  const grid = document.getElementById('weekGrid');
  grid.innerHTML = '';

  const weekStart = startOfWeek(AppState.currentDate);
  const today = new Date();
  const selStr = toDateStr(AppState.currentDate);

  for (let i = 0; i < 7; i++) {
    const day  = addDays(weekStart, i);
    const ds   = toDateStr(day);
    const tasks = applyFilters(getTasksForDate(ds));

    const col = document.createElement('div');
    col.className = 'week-col';
    if (isSameDay(day, today)) col.classList.add('is-today');
    if (ds === selStr) col.classList.add('is-selected');

    col.innerHTML = `
      <div class="week-col-hd">
        <div class="week-col-dow">${DAYS_SHORT[day.getDay()]}</div>
        <div class="week-col-datenum">${day.getDate()}</div>
      </div>
      <div class="week-col-body" id="wkcol-${ds}"></div>
    `;
    grid.appendChild(col);

    const body = col.querySelector('.week-col-body');

    tasks.forEach(t => {
      const chip = document.createElement('div');
      const done = getEffectiveDone(t);
      chip.className = `week-chip cat-${t.category}${done ? ' completed' : ''}`;
      chip.title = `${t.title} — ${formatTime(t.start)}`;
      chip.textContent = t.title;
      chip.addEventListener('click', () => openDetailModal(t.id, t._virtualDate));
      body.appendChild(chip);
    });

    const addBtn = document.createElement('button');
    addBtn.className = 'week-add-btn';
    addBtn.innerHTML = `<svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
      <path d="M6 2v8M2 6h8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
    </svg> Add`;
    addBtn.addEventListener('click', () => {
      AppState.currentDate = day;
      openFormModal(null, {});
    });
    body.appendChild(addBtn);
  }
}

/* ====================================================================
   DRAG & DROP (rescheduling on timeline)
   ==================================================================== */
function handleDragStart(e) {
  const card = e.currentTarget;
  AppState.dragging = { taskId: card.dataset.id };
  card.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', card.dataset.id);
}

function handleDragEnd(e) {
  e.currentTarget.classList.remove('dragging');
  document.querySelectorAll('.hour-row.drag-over').forEach(r => r.classList.remove('drag-over'));
  AppState.dragging = null;
}

function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  e.currentTarget.classList.add('drag-over');
}

function handleDragLeave(e) {
  e.currentTarget.classList.remove('drag-over');
}

function handleDrop(e) {
  e.preventDefault();
  const row = e.currentTarget;
  row.classList.remove('drag-over');
  const hour = parseInt(row.dataset.hour, 10);
  const taskId = e.dataTransfer.getData('text/plain');
  const task = AppState.tasks.find(t => t.id === taskId);
  if (!task) return;

  const startMin = timeToMin(task.start);
  const endMin   = timeToMin(task.end) || startMin + 30;
  const dur      = endMin - startMin;

  // Snap to 15-min within the hour based on drop Y position
  const rowRect = row.getBoundingClientRect();
  const yOff    = e.clientY - rowRect.top;
  const minFrac = clamp(Math.round((yOff / HOUR_H) * 4) * 15, 0, 45);
  const newStart = hour * 60 + minFrac;
  const newEnd   = clamp(newStart + dur, 0, 23 * 60 + 59);

  updateTask(taskId, {
    start: minToTime(newStart),
    end:   minToTime(newEnd),
  });
  refreshAll();
  showToast(`"${task.title}" moved to ${minToTime(newStart)}`, 'info');
}

/* ====================================================================
   FORM MODAL
   ==================================================================== */
function openFormModal(taskId, prefill = {}) {
  AppState.editingId = taskId;
  const form     = document.getElementById('taskForm');
  const title    = document.getElementById('formModalTitle');
  const saveBtn  = document.getElementById('saveBtn');
  const delBtn   = document.getElementById('deleteBtn');

  // Reset
  form.reset();
  document.getElementById('fTitleErr').classList.add('hidden');
  document.getElementById('editingId').value = '';
  document.getElementById('fDone').checked   = false;

  if (taskId) {
    // Edit mode
    const t = AppState.tasks.find(t => t.id === taskId);
    if (!t) return;
    title.textContent = 'Edit Task';
    saveBtn.textContent = 'Update Task';
    delBtn.classList.remove('hidden');
    document.getElementById('editingId').value = t.id;
    document.getElementById('fTitle').value    = t.title;
    document.getElementById('fDate').value     = t.date;
    document.getElementById('fStart').value    = t.start;
    document.getElementById('fEnd').value      = t.end;
    document.getElementById('fCategory').value = t.category;
    document.getElementById('fPriority').value = t.priority;
    document.getElementById('fRecurring').value= t.recurring;
    document.getElementById('fNotes').value    = t.notes;
    document.getElementById('fDone').checked   = t.done;
  } else {
    title.textContent = 'Add Task';
    saveBtn.textContent = 'Save Task';
    delBtn.classList.add('hidden');

    const ds   = toDateStr(AppState.currentDate);
    const hour = prefill.startHour ?? new Date().getHours();
    document.getElementById('fDate').value     = ds;
    document.getElementById('fStart').value    = `${String(hour).padStart(2,'0')}:00`;
    document.getElementById('fEnd').value      = `${String(Math.min(hour + 1, 23)).padStart(2,'0')}:00`;
    document.getElementById('fCategory').value = prefill.category || 'work';
    document.getElementById('fPriority').value = 'medium';
    document.getElementById('fRecurring').value= 'none';
  }

  const overlay = document.getElementById('formOverlay');
  overlay.classList.remove('hidden');
  setTimeout(() => document.getElementById('fTitle').focus(), 50);
}

function closeFormModal() {
  document.getElementById('formOverlay').classList.add('hidden');
  AppState.editingId = null;
}

function handleFormSubmit(e) {
  e.preventDefault();
  const titleVal = document.getElementById('fTitle').value.trim();
  const errEl    = document.getElementById('fTitleErr');

  if (!titleVal) {
    errEl.classList.remove('hidden');
    document.getElementById('fTitle').focus();
    return;
  }
  errEl.classList.add('hidden');

  const data = {
    title:     titleVal,
    date:      document.getElementById('fDate').value,
    start:     document.getElementById('fStart').value,
    end:       document.getElementById('fEnd').value,
    category:  document.getElementById('fCategory').value,
    priority:  document.getElementById('fPriority').value,
    recurring: document.getElementById('fRecurring').value,
    notes:     document.getElementById('fNotes').value.trim(),
    done:      document.getElementById('fDone').checked,
  };

  const eid = document.getElementById('editingId').value;
  if (eid) {
    updateTask(eid, data);
    showToast('Task updated', 'success');
  } else {
    createTask(data);
    showToast('Task added', 'success');
  }

  closeFormModal();
  refreshAll();
}

/* ====================================================================
   DETAIL MODAL
   ==================================================================== */
function openDetailModal(taskId, virtualDate) {
  const task = AppState.tasks.find(t => t.id === taskId);
  if (!task) return;

  const vd    = virtualDate || null;
  const done  = vd ? (task.completionOverrides?.[vd] ?? false) : task.done;
  const color = CATEGORY_COLORS[task.category] || '#888';

  document.getElementById('detailCatChip').textContent = task.category;
  document.getElementById('detailCatChip').style.background = color + '33';
  document.getElementById('detailCatChip').style.color       = color;
  document.getElementById('detailCatChip').style.border      = `1px solid ${color}55`;

  document.getElementById('detailHeading').textContent  = task.title;
  document.getElementById('detailTimeText').textContent =
    `${formatTime(task.start)}${task.end ? ' – ' + formatTime(task.end) : ''} · ${formatDateLong(parseDate(task.date))}`;

  const priChip = document.getElementById('detailPriChip');
  priChip.textContent = `${PRIORITY_LABELS[task.priority]} priority`;
  priChip.style.color  = PRIORITY_COLORS[task.priority];

  const recChip = document.getElementById('detailRecurChip');
  if (task.recurring && task.recurring !== 'none') {
    recChip.textContent = `Repeats ${task.recurring}`;
    recChip.classList.remove('hidden');
  } else {
    recChip.classList.add('hidden');
  }

  document.getElementById('detailNotes').textContent = task.notes || 'No notes.';

  const doneBtn = document.getElementById('detailDoneBtn');
  doneBtn.textContent = done ? 'Mark Incomplete' : 'Mark Complete';
  doneBtn.className   = done ? 'btn btn-undo' : 'btn btn-done';
  doneBtn.onclick = () => {
    toggleTaskDone(taskId, vd);
    refreshAll();
    closeDetailModal();
  };

  document.getElementById('detailEditBtn').onclick = () => {
    closeDetailModal();
    openFormModal(taskId);
  };
  document.getElementById('detailDeleteBtn').onclick = () => {
    deleteTask(taskId);
    closeDetailModal();
    refreshAll();
    showToast('Task deleted', 'error');
  };

  document.getElementById('detailOverlay').classList.remove('hidden');
}

function closeDetailModal() {
  document.getElementById('detailOverlay').classList.add('hidden');
}

/* ====================================================================
   EXPORT
   ==================================================================== */
function exportTasks() {
  const blob = new Blob(
    [JSON.stringify(AppState.tasks, null, 2)],
    { type: 'application/json' }
  );
  const url = URL.createObjectURL(blob);
  const a   = document.createElement('a');
  a.href    = url;
  a.download = `dayflow-tasks-${todayStr()}.json`;
  a.click();
  URL.revokeObjectURL(url);
  showToast('Tasks exported!', 'success');
}

/* ====================================================================
   FULL REFRESH
   ==================================================================== */
function refreshAll() {
  updateDateHeading();
  renderMiniCal();
  updateStats();

  if (AppState.view === 'day') {
    buildTimeline();
    renderTimeline();
  } else {
    renderWeekView();
  }
}

/* ====================================================================
   SCROLL TO CURRENT TIME
   ==================================================================== */
function scrollToCurrentTime() {
  const scroll = document.getElementById('timelineScroll');
  const now    = new Date();
  const totalMin = now.getHours() * 60 + now.getMinutes();
  const top      = (totalMin / 60) * HOUR_H;
  scroll.scrollTo({ top: Math.max(0, top - 120), behavior: 'smooth' });
}

/* ====================================================================
   HTML ESCAPE
   ==================================================================== */
function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* ====================================================================
   INIT — WIRE UP ALL EVENT LISTENERS
   ==================================================================== */
function init() {
  loadTasks();

  // ---- Sidebar toggle ----
  const sidebar  = document.getElementById('sidebar');
  const backdrop = document.getElementById('sidebarBackdrop');
  function openSidebar() {
    sidebar.classList.add('open');
    backdrop.classList.add('visible');
  }
  function closeSidebar() {
    sidebar.classList.remove('open');
    backdrop.classList.remove('visible');
  }
  document.getElementById('menuBtn').addEventListener('click', () => {
    sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
  });
  document.getElementById('sidebarClose').addEventListener('click', closeSidebar);
  backdrop.addEventListener('click', closeSidebar);

  // ---- Mini calendar nav ----
  document.getElementById('miniCalPrev').addEventListener('click', () => {
    const d = AppState.miniCalDate;
    AppState.miniCalDate = new Date(d.getFullYear(), d.getMonth() - 1, 1);
    renderMiniCal();
  });
  document.getElementById('miniCalNext').addEventListener('click', () => {
    const d = AppState.miniCalDate;
    AppState.miniCalDate = new Date(d.getFullYear(), d.getMonth() + 1, 1);
    renderMiniCal();
  });

  // ---- Date navigation ----
  document.getElementById('prevDay').addEventListener('click', () => {
    AppState.currentDate = addDays(AppState.currentDate, AppState.view === 'week' ? -7 : -1);
    refreshAll();
  });
  document.getElementById('nextDay').addEventListener('click', () => {
    AppState.currentDate = addDays(AppState.currentDate, AppState.view === 'week' ? 7 : 1);
    refreshAll();
  });
  document.getElementById('todayBtn').addEventListener('click', () => {
    AppState.currentDate = new Date();
    AppState.miniCalDate = new Date();
    refreshAll();
    if (AppState.view === 'day') scrollToCurrentTime();
  });
  document.getElementById('datePicker').addEventListener('change', (e) => {
    if (e.target.value) {
      AppState.currentDate = parseDate(e.target.value);
      AppState.miniCalDate = new Date(AppState.currentDate);
      refreshAll();
    }
  });

  // ---- View toggle ----
  document.getElementById('dayViewBtn').addEventListener('click', () => {
    if (AppState.view === 'day') return;
    AppState.view = 'day';
    document.getElementById('dayViewBtn').classList.add('active');
    document.getElementById('weekViewBtn').classList.remove('active');
    document.getElementById('dayView').classList.remove('hidden');
    document.getElementById('weekView').classList.add('hidden');
    refreshAll();
    setTimeout(scrollToCurrentTime, 80);
  });
  document.getElementById('weekViewBtn').addEventListener('click', () => {
    if (AppState.view === 'week') return;
    AppState.view = 'week';
    document.getElementById('weekViewBtn').classList.add('active');
    document.getElementById('dayViewBtn').classList.remove('active');
    document.getElementById('weekView').classList.remove('hidden');
    document.getElementById('dayView').classList.add('hidden');
    refreshAll();
  });

  // ---- Search ----
  const searchInput = document.getElementById('searchInput');
  const searchClear = document.getElementById('searchClearBtn');
  searchInput.addEventListener('input', (e) => {
    AppState.filter.keyword = e.target.value;
    searchClear.classList.toggle('hidden', !e.target.value);
    refreshAll();
  });
  searchClear.addEventListener('click', () => {
    searchInput.value = '';
    AppState.filter.keyword = '';
    searchClear.classList.add('hidden');
    refreshAll();
  });

  // ---- Category filter ----
  document.getElementById('categoryFilters').addEventListener('click', (e) => {
    const btn = e.target.closest('.cat-filter-btn');
    if (!btn) return;
    document.querySelectorAll('.cat-filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    AppState.filter.cat = btn.dataset.cat;
    refreshAll();
  });

  // ---- FAB ----
  document.getElementById('fab').addEventListener('click', () => openFormModal(null, {}));

  // ---- Form Modal ----
  document.getElementById('taskForm').addEventListener('submit', handleFormSubmit);
  document.getElementById('formModalClose').addEventListener('click', closeFormModal);
  document.getElementById('cancelBtn').addEventListener('click', closeFormModal);
  document.getElementById('deleteBtn').addEventListener('click', () => {
    const eid = document.getElementById('editingId').value;
    if (eid) {
      deleteTask(eid);
      closeFormModal();
      refreshAll();
      showToast('Task deleted', 'error');
    }
  });
  document.getElementById('formOverlay').addEventListener('click', (e) => {
    if (e.target === document.getElementById('formOverlay')) closeFormModal();
  });

  // ---- Detail Modal ----
  document.getElementById('detailClose').addEventListener('click', closeDetailModal);
  document.getElementById('detailOverlay').addEventListener('click', (e) => {
    if (e.target === document.getElementById('detailOverlay')) closeDetailModal();
  });

  // ---- Keyboard shortcuts ----
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeFormModal();
      closeDetailModal();
    }
    // 'n' to add new task (when no input focused)
    if (e.key === 'n' && !e.ctrlKey && !e.metaKey &&
        !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)) {
      openFormModal(null, {});
    }
  });

  // ---- Notifications ----
  const notifBtn = document.getElementById('notifBtn');
  notifBtn.addEventListener('click', async () => {
    if (!('Notification' in window)) {
      showToast('Notifications not supported in this browser', 'error');
      return;
    }
    const granted = await requestNotifPermission();
    if (granted) {
      AppState.notifEnabled = !AppState.notifEnabled;
      notifBtn.classList.toggle('enabled', AppState.notifEnabled);
      if (AppState.notifEnabled) {
        rescheduleAllNotifications();
        showToast('Notifications enabled', 'success');
      } else {
        Object.keys(AppState.notifTimers).forEach(clearNotification);
        showToast('Notifications disabled', 'info');
      }
    } else {
      showToast('Notification permission denied', 'error');
    }
  });

  // ---- Export ----
  document.getElementById('exportBtn').addEventListener('click', exportTasks);

  // ---- Auto-update time bar every minute ----
  setInterval(() => {
    positionTimeNowBar();
    updateStats(); // keep stats fresh
  }, 60_000);

  // ---- Initial render ----
  refreshAll();
  setTimeout(scrollToCurrentTime, 100);
}

/* ====================================================================
   BOOTSTRAP
   ==================================================================== */
document.addEventListener('DOMContentLoaded', init);
