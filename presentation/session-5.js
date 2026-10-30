(function () {
  var slides = document.querySelectorAll(".slide");
  var actEl = document.getElementById("hud-act");
  var timerBtn = document.getElementById("hud-timer");
  var notesBtn = document.getElementById("hud-notes");
  var boardBtn = document.getElementById("hud-board");
  var scoreBtn = document.getElementById("hud-score");
  var revealBtn = document.getElementById("hud-reveal");
  var twistBtn = document.getElementById("hud-twist");
  var plusBtn = document.getElementById("hud-plus");
  var minusBtn = document.getElementById("hud-minus");
  var notesPanel = document.getElementById("notes-panel");
  var notesBody = document.getElementById("notes-body");
  var teamsPanel = document.getElementById("teams-panel");
  var scorePanel = document.getElementById("score-panel");
  var twistPanel = document.getElementById("twist-panel");
  var scoreEl = document.getElementById("room-score");
  var remaining = 0;
  var duration = 0;
  var ticking = null;
  var selectedTeam = "A";
  var TEAMS = ["A", "B", "C", "D", "E", "F", "G", "H"];
  var TEAM_NAMES = {
    A: "Getting started",
    B: "Personalisation",
    C: "Home",
    D: "Discover",
    E: "Meditation",
    F: "Goals",
    G: "Journal",
    H: "Profile"
  };
  var STATUSES = ["idle", "mapping", "designing", "ready"];
  var STATUS_LABEL = {
    idle: "Not started",
    mapping: "Problem + HMW",
    designing: "Building",
    ready: "Ready to assemble"
  };

  function scoreKey(letter) {
    return "reva-s5-pts-" + letter;
  }
  function getScore(letter) {
    return Number(window.localStorage.getItem(scoreKey(letter)) || 0);
  }
  function setScore(letter, value) {
    window.localStorage.setItem(scoreKey(letter), String(Math.max(0, value)));
  }
  function roomTotal() {
    return TEAMS.reduce(function (sum, letter) {
      return sum + getScore(letter);
    }, 0);
  }
  function renderScores() {
    TEAMS.forEach(function (letter) {
      var cell = document.querySelector('[data-score-team="' + letter + '"] .pts');
      if (cell) cell.textContent = getScore(letter);
      var row = document.querySelector('[data-score-team="' + letter + '"]');
      if (row) row.classList.toggle("is-selected", letter === selectedTeam);
    });
    if (scoreEl) scoreEl.textContent = "Room " + roomTotal();
  }

  function activeSlide() {
    return document.querySelector(".slide.is-active");
  }

  function formatTime(sec) {
    var m = Math.floor(Math.max(0, sec) / 60);
    var s = Math.max(0, sec) % 60;
    return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
  }

  function stopTimer() {
    if (ticking) window.clearInterval(ticking);
    ticking = null;
    timerBtn.classList.remove("is-hot");
  }

  function startTimer() {
    if (remaining <= 0) remaining = duration || 60;
    stopTimer();
    timerBtn.classList.add("is-hot");
    ticking = window.setInterval(function () {
      remaining -= 1;
      timerBtn.textContent = formatTime(remaining);
      if (remaining <= 0) {
        stopTimer();
        timerBtn.classList.add("is-done");
        timerBtn.textContent = "00:00";
      }
    }, 1000);
  }

  function loadTimerFromSlide(slide) {
    var mins = Number(slide && slide.dataset.timer);
    stopTimer();
    timerBtn.classList.remove("is-done");
    if (!mins) {
      duration = 0;
      remaining = 0;
      timerBtn.textContent = "Timer";
      return;
    }
    duration = Math.round(mins * 60);
    remaining = duration;
    timerBtn.textContent = formatTime(remaining);
  }

  function closePanels(except) {
    [notesPanel, teamsPanel, scorePanel, twistPanel].forEach(function (panel) {
      if (!panel) return;
      if (panel !== except) panel.classList.remove("is-open");
    });
  }

  function syncHud() {
    var slide = activeSlide();
    if (!slide) return;
    actEl.textContent = slide.dataset.act || "SESSION 05";
    var bits = [];
    if (slide.dataset.learn) bits.push(slide.dataset.learn);
    bits.push(slide.dataset.notes || "No speaker note on this slide.");
    if (slide.dataset.transition) bits.push("Next: " + slide.dataset.transition);
    notesBody.textContent = bits.join(" ");
    loadTimerFromSlide(slide);
    if (revealBtn) {
      revealBtn.disabled = !slide.querySelector("[data-reveal]");
    }
  }

  var observer = new MutationObserver(function () { syncHud(); });
  slides.forEach(function (slide) {
    observer.observe(slide, { attributes: true, attributeFilter: ["class"] });
  });

  timerBtn.addEventListener("click", function () {
    if (!duration && remaining <= 0) return;
    if (ticking) stopTimer();
    else startTimer();
  });
  timerBtn.addEventListener("dblclick", function (event) {
    event.preventDefault();
    remaining = duration;
    timerBtn.classList.remove("is-done");
    timerBtn.textContent = duration ? formatTime(duration) : "Timer";
    stopTimer();
  });

  function togglePanel(btn, panel) {
    var open = !panel.classList.contains("is-open");
    closePanels(open ? panel : null);
    panel.classList.toggle("is-open", open);
  }

  notesBtn.addEventListener("click", function () { togglePanel(notesBtn, notesPanel); });
  boardBtn.addEventListener("click", function () { togglePanel(boardBtn, teamsPanel); });
  if (scoreBtn) scoreBtn.addEventListener("click", function () { togglePanel(scoreBtn, scorePanel); });
  if (twistBtn) twistBtn.addEventListener("click", function () { togglePanel(twistBtn, twistPanel); });

  if (revealBtn) {
    revealBtn.addEventListener("click", function () {
      var slide = activeSlide();
      if (!slide) return;
      slide.querySelectorAll("[data-reveal]").forEach(function (node) {
        node.classList.toggle("is-revealed");
      });
    });
  }

  function bump(delta) {
    setScore(selectedTeam, getScore(selectedTeam) + delta);
    renderScores();
  }
  if (plusBtn) plusBtn.addEventListener("click", function () { bump(10); });
  if (minusBtn) minusBtn.addEventListener("click", function () { bump(-10); });

  window.addEventListener("keydown", function (event) {
    if (event.target && /input|textarea/i.test(event.target.tagName)) return;
    var key = event.key.toLowerCase();
    if (key === "n") notesBtn.click();
    if (key === "b") boardBtn.click();
    if (key === "s" && scoreBtn) scoreBtn.click();
    if (key === "r" && revealBtn) revealBtn.click();
    if (key === "t" && twistBtn) twistBtn.click();
    if (key === "+" || key === "=") bump(10);
    if (key === "-" || key === "_") bump(-10);
  });

  document.querySelectorAll(".team-chip").forEach(function (chip, index) {
    var letter = TEAMS[index];
    var stored = window.localStorage.getItem("reva-s5-" + index) || "idle";
    chip.dataset.status = stored;
    var label = chip.querySelector("span");
    if (label) label.textContent = STATUS_LABEL[stored];
    chip.addEventListener("click", function () {
      var next = STATUSES[(STATUSES.indexOf(chip.dataset.status) + 1) % STATUSES.length];
      chip.dataset.status = next;
      if (label) label.textContent = STATUS_LABEL[next];
      window.localStorage.setItem("reva-s5-" + index, next);
      selectedTeam = letter;
      renderScores();
    });
  });

  document.querySelectorAll("[data-score-team]").forEach(function (row) {
    row.addEventListener("click", function () {
      selectedTeam = row.getAttribute("data-score-team");
      renderScores();
    });
  });

  document.querySelectorAll(".game-choices").forEach(function (group) {
    group.addEventListener("click", function (event) {
      var btn = event.target.closest("button");
      if (!btn || group.classList.contains("is-locked")) return;
      group.classList.add("is-locked");
      var right = btn.dataset.answer === "right";
      btn.classList.add(right ? "is-right" : "is-wrong");
      group.querySelectorAll("button").forEach(function (other) {
        if (other.dataset.answer === "right") other.classList.add("is-right");
      });
      var pts = Number(btn.dataset.points || group.dataset.points || (right ? 10 : 0));
      if (right && pts) {
        bump(pts);
        var reveal = group.parentElement && group.parentElement.querySelector("[data-reveal]");
        if (reveal) reveal.classList.add("is-revealed");
      }
    });
  });

  document.querySelectorAll("[data-award]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.classList.toggle("is-awarded");
      if (btn.classList.contains("is-awarded")) bump(25);
    });
  });

  document.querySelectorAll(".twist-list button").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll(".twist-list button").forEach(function (other) {
        other.classList.remove("is-live");
      });
      btn.classList.add("is-live");
      var banner = document.getElementById("twist-banner");
      if (banner) {
        banner.hidden = false;
        banner.querySelector("strong").textContent = btn.dataset.twist;
        banner.querySelector("span").textContent = btn.dataset.detail;
      }
    });
  });

  var dismiss = document.getElementById("twist-dismiss");
  if (dismiss) {
    dismiss.addEventListener("click", function () {
      var banner = document.getElementById("twist-banner");
      if (banner) banner.hidden = true;
    });
  }

  renderScores();
  syncHud();
})();
