// Planificateur de Révisions
// Stocke les données dans le localStorage et génère un emploi du temps équilibré

const STORAGE_KEY = "revision-planner-data";

const state = {
  subjects: [],
  settings: {
    startDate: "",
    endDate: "",
    hoursPerDay: 2,
    restDays: [],
  },
};

// ----- Persistance -----
function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function loadState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return;
  try {
    const data = JSON.parse(raw);
    Object.assign(state, data);
  } catch (e) {
    console.warn("Données invalides en cache, réinitialisation.");
  }
}

// ----- Matières -----
function renderSubjects() {
  const list = document.getElementById("subject-list");
  list.innerHTML = "";

  if (state.subjects.length === 0) {
    list.innerHTML = '<li style="justify-content:center;color:#6b7280">Aucune matière ajoutée</li>';
    return;
  }

  const difficultyLabels = ["", "Facile", "Moyenne", "Difficile", "Très difficile"];

  state.subjects.forEach((subject, index) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="subject-info">
        <span class="subject-name">${escapeHtml(subject.name)}</span>
        <span class="subject-meta">${difficultyLabels[subject.difficulty]} · ${subject.chapters} chapitres</span>
      </div>
      <button class="delete-btn" data-index="${index}" title="Supprimer">×</button>
    `;
    list.appendChild(li);
  });

  list.querySelectorAll(".delete-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const idx = parseInt(e.target.dataset.index, 10);
      state.subjects.splice(idx, 1);
      saveState();
      renderSubjects();
    });
  });
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// ----- Génération de l'emploi du temps -----
function generateSchedule() {
  // Lire les paramètres depuis le formulaire
  state.settings.startDate = document.getElementById("start-date").value;
  state.settings.endDate = document.getElementById("end-date").value;
  state.settings.hoursPerDay = parseFloat(document.getElementById("hours-per-day").value);
  state.settings.restDays = Array.from(
    document.querySelectorAll(".rest-days input:checked")
  ).map((el) => parseInt(el.value, 10));

  // Validation
  if (!state.settings.startDate || !state.settings.endDate) {
    alert("Veuillez choisir une date de début et une date de fin.");
    return;
  }
  if (state.subjects.length === 0) {
    alert("Ajoutez au moins une matière.");
    return;
  }

  const start = new Date(state.settings.startDate);
  const end = new Date(state.settings.endDate);

  if (end < start) {
    alert("La date de fin doit être après la date de début.");
    return;
  }

  saveState();

  // Calcul du nombre total de "points de difficulté" pour répartir les heures
  const totalWeight = state.subjects.reduce(
    (sum, s) => sum + s.difficulty * s.chapters,
    0
  );

  // Liste des jours de travail
  const workDays = [];
  const cur = new Date(start);
  while (cur <= end) {
    if (!state.settings.restDays.includes(cur.getDay())) {
      workDays.push(new Date(cur));
    }
    cur.setDate(cur.getDate() + 1);
  }

  if (workDays.length === 0) {
    alert("Aucun jour de travail disponible (vérifie tes jours de repos).");
    return;
  }

  const totalHours = workDays.length * state.settings.hoursPerDay;

  // Heures à allouer par matière (proportionnel au poids)
  const subjectHours = state.subjects.map((s) => ({
    ...s,
    targetHours: (s.difficulty * s.chapters / totalWeight) * totalHours,
    remainingHours: (s.difficulty * s.chapters / totalWeight) * totalHours,
  }));

  // Génération round-robin pondéré : chaque jour on choisit la matière
  // qui a le plus d'heures restantes proportionnellement
  const schedule = [];
  const sessionLength = Math.min(1, state.settings.hoursPerDay); // 1h par session max
  const sessionsPerDay = Math.max(1, Math.round(state.settings.hoursPerDay / sessionLength));
  const actualSessionLength = state.settings.hoursPerDay / sessionsPerDay;

  workDays.forEach((day) => {
    const sessions = [];
    // Ne pas répéter la même matière deux fois de suite dans la journée si possible
    let lastSubject = null;
    for (let i = 0; i < sessionsPerDay; i++) {
      // Trier par heures restantes décroissantes
      const candidates = [...subjectHours]
        .filter((s) => s.remainingHours > 0.01)
        .sort((a, b) => b.remainingHours - a.remainingHours);

      if (candidates.length === 0) break;

      let pick = candidates[0];
      if (candidates.length > 1 && pick.name === lastSubject) {
        pick = candidates[1];
      }

      pick.remainingHours -= actualSessionLength;
      lastSubject = pick.name;

      sessions.push({
        subject: pick.name,
        duration: actualSessionLength,
      });
    }
    schedule.push({ date: day, sessions });
  });

  // Génération de tous les jours (y compris repos) pour l'affichage
  const allDays = [];
  const cur2 = new Date(start);
  let workIdx = 0;
  while (cur2 <= end) {
    if (state.settings.restDays.includes(cur2.getDay())) {
      allDays.push({ date: new Date(cur2), rest: true, sessions: [] });
    } else {
      allDays.push({ ...schedule[workIdx], rest: false });
      workIdx++;
    }
    cur2.setDate(cur2.getDate() + 1);
  }

  renderSchedule(allDays, totalHours, workDays.length);
}

function renderSchedule(days, totalHours, workDaysCount) {
  const section = document.getElementById("schedule-section");
  section.hidden = false;

  // Résumé
  const summary = document.getElementById("schedule-summary");
  summary.innerHTML = `
    <div class="summary-item">
      <div class="summary-value">${days.length}</div>
      <div class="summary-label">jours au total</div>
    </div>
    <div class="summary-item">
      <div class="summary-value">${workDaysCount}</div>
      <div class="summary-label">jours de révision</div>
    </div>
    <div class="summary-item">
      <div class="summary-value">${totalHours.toFixed(1)}h</div>
      <div class="summary-label">total à réviser</div>
    </div>
    <div class="summary-item">
      <div class="summary-value">${state.subjects.length}</div>
      <div class="summary-label">matières</div>
    </div>
  `;

  // Calendrier
  const output = document.getElementById("schedule-output");
  output.innerHTML = "";

  const dayNames = ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"];
  const monthNames = [
    "jan", "fév", "mar", "avr", "mai", "juin",
    "juil", "août", "sep", "oct", "nov", "déc"
  ];

  days.forEach((day) => {
    const card = document.createElement("div");
    card.className = "day-card" + (day.rest ? " rest" : "");

    const date = day.date;
    const header = `
      <div class="day-header">
        <span>${dayNames[date.getDay()]} ${date.getDate()} ${monthNames[date.getMonth()]}</span>
        <span class="day-date">${day.rest ? "Repos" : ""}</span>
      </div>
    `;

    let body = "";
    if (!day.rest && day.sessions) {
      let cumulative = 0;
      day.sessions.forEach((session) => {
        const startMin = cumulative * 60;
        const endMin = (cumulative + session.duration) * 60;
        cumulative += session.duration;
        body += `
          <div class="session">
            <span>${escapeHtml(session.subject)}</span>
            <span class="session-time">${formatDuration(session.duration)}</span>
          </div>
        `;
      });
    }

    card.innerHTML = header + body;
    output.appendChild(card);
  });

  section.scrollIntoView({ behavior: "smooth", block: "start" });
}

function formatDuration(hours) {
  const h = Math.floor(hours);
  const m = Math.round((hours - h) * 60);
  if (h === 0) return `${m} min`;
  if (m === 0) return `${h}h`;
  return `${h}h${m.toString().padStart(2, "0")}`;
}

// ----- Réinitialisation -----
function resetAll() {
  if (!confirm("Tout effacer (matières, paramètres, emploi du temps) ?")) return;
  state.subjects = [];
  state.settings = { startDate: "", endDate: "", hoursPerDay: 2, restDays: [] };
  localStorage.removeItem(STORAGE_KEY);
  document.getElementById("schedule-section").hidden = true;
  applySettingsToForm();
  renderSubjects();
}

function applySettingsToForm() {
  document.getElementById("start-date").value = state.settings.startDate || "";
  document.getElementById("end-date").value = state.settings.endDate || "";
  document.getElementById("hours-per-day").value = state.settings.hoursPerDay || 2;
  document.querySelectorAll(".rest-days input").forEach((el) => {
    el.checked = state.settings.restDays.includes(parseInt(el.value, 10));
  });
}

// ----- Initialisation -----
document.addEventListener("DOMContentLoaded", () => {
  loadState();
  applySettingsToForm();
  renderSubjects();

  // Date par défaut : aujourd'hui
  if (!state.settings.startDate) {
    const today = new Date().toISOString().split("T")[0];
    document.getElementById("start-date").value = today;
  }

  document.getElementById("subject-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const name = document.getElementById("subject-name").value.trim();
    const difficulty = parseInt(document.getElementById("subject-difficulty").value, 10);
    const chapters = parseInt(document.getElementById("subject-chapters").value, 10);

    if (!name) return;
    state.subjects.push({ name, difficulty, chapters });
    saveState();
    renderSubjects();
    e.target.reset();
    document.getElementById("subject-difficulty").value = "2";
    document.getElementById("subject-chapters").value = "5";
    document.getElementById("subject-name").focus();
  });

  document.getElementById("generate-btn").addEventListener("click", generateSchedule);
  document.getElementById("reset-btn").addEventListener("click", resetAll);
  document.getElementById("print-btn").addEventListener("click", () => window.print());
});
