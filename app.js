const state = {
  allQuestions: [],
  queue: [],
  totalTarget: 0,
  current: null,
  answered: 0,
  ok: 0,
  ko: 0,
  conceptStats: {}
};

const el = {
  setupCard: document.getElementById("setupCard"),
  quizCard: document.getElementById("quizCard"),
  resultsCard: document.getElementById("resultsCard"),
  datasetMeta: document.getElementById("datasetMeta"),
  questionCount: document.getElementById("questionCount"),
  startBtn: document.getElementById("startBtn"),
  restartBtn: document.getElementById("restartBtn"),
  progressText: document.getElementById("progressText"),
  conceptText: document.getElementById("conceptText"),
  okCount: document.getElementById("okCount"),
  koCount: document.getElementById("koCount"),
  questionText: document.getElementById("questionText"),
  choicesContainer: document.getElementById("choicesContainer"),
  feedbackBox: document.getElementById("feedbackBox"),
  nextBtn: document.getElementById("nextBtn"),
  multiActions: document.getElementById("multiActions"),
  submitMultiBtn: document.getElementById("submitMultiBtn"),
  finalSummary: document.getElementById("finalSummary"),
  finalPercent: document.getElementById("finalPercent"),
  conceptStatsBody: document.getElementById("conceptStatsBody")
};

function shuffle(arr) {
  const out = [...arr];
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

function sameSet(a, b) {
  if (a.length !== b.length) {
    return false;
  }
  const sa = [...a].sort().join("");
  const sb = [...b].sort().join("");
  return sa === sb;
}

function normalizeExplanation(text) {
  // Basic markdown cleanup for a readable inline explanation.
  return text.replace(/\*\*/g, "").trim();
}

function updateTopScore() {
  el.okCount.textContent = String(state.ok);
  el.koCount.textContent = String(state.ko);
  el.progressText.textContent = `Pregunta ${state.answered + 1}/${state.totalTarget}`;
}

function showFeedback(kind, html) {
  el.feedbackBox.classList.remove("hidden", "ok", "ko");
  el.feedbackBox.classList.add(kind);
  el.feedbackBox.innerHTML = html;
}

function hideFeedback() {
  el.feedbackBox.classList.add("hidden");
  el.feedbackBox.classList.remove("ok", "ko");
  el.feedbackBox.textContent = "";
}

function conceptBucket(concept) {
  if (!state.conceptStats[concept]) {
    state.conceptStats[concept] = { ok: 0, ko: 0 };
  }
  return state.conceptStats[concept];
}

function getNextQuestion() {
  if (state.answered >= state.totalTarget || state.queue.length === 0) {
    finishQuiz();
    return;
  }

  state.current = state.queue.pop();
  renderQuestion();
}

function markAndContinue(isCorrect, selectedAnswers) {
  const question = state.current;
  const bucket = conceptBucket(question.concept);

  state.answered += 1;
  if (isCorrect) {
    state.ok += 1;
    bucket.ok += 1;
  } else {
    state.ko += 1;
    bucket.ko += 1;
  }

  updateTopScore();

  const explanation = normalizeExplanation(question.explanation || "");
  const refLink = question.reference
    ? `<br/><a href="${question.reference}" target="_blank" rel="noopener">📖 Documentación oficial de Salesforce</a>`
    : "";

  if (isCorrect) {
    showFeedback("ok", `<strong>¡Correcto!</strong><br/><br/>${explanation}${refLink}`);
    el.nextBtn.classList.remove("hidden");
    return;
  }

  const selected = selectedAnswers.length ? selectedAnswers.join(", ") : "(sin respuesta)";
  const expected = question.correctAnswers.join(", ");

  showFeedback(
    "ko",
    `<strong>Incorrecto.</strong><br/>Tu respuesta: ${selected}<br/>Correcta: ${expected}<br/><br/>${explanation}${refLink}`
  );
  el.nextBtn.classList.remove("hidden");
}

function renderSingleChoice(question) {
  question.choices.forEach((choice) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "choice-btn";
    btn.innerHTML = `<strong>${choice.id}.</strong> ${choice.text}`;
    btn.addEventListener("click", () => {
      const selected = [choice.id];
      const correct = sameSet(selected, question.correctAnswers);
      markAndContinue(correct, selected);
    });
    el.choicesContainer.appendChild(btn);
  });
}

function renderMultiChoice(question) {
  question.choices.forEach((choice) => {
    const wrapper = document.createElement("div");
    wrapper.className = "choice-check";

    const label = document.createElement("label");
    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.value = choice.id;
    label.appendChild(cb);

    const text = document.createElement("span");
    text.innerHTML = `<strong>${choice.id}.</strong> ${choice.text}`;
    label.appendChild(text);

    wrapper.appendChild(label);
    el.choicesContainer.appendChild(wrapper);
  });

  el.multiActions.classList.remove("hidden");
  el.submitMultiBtn.onclick = () => {
    const selected = Array.from(el.choicesContainer.querySelectorAll("input[type='checkbox']:checked"))
      .map((node) => node.value)
      .sort();

    const required = state.current.correctAnswers.length;
    if (selected.length !== required) {
      showFeedback(
        "ko",
        `<strong>Seleccion incompleta.</strong><br/>Debes elegir exactamente ${required} opcion(es).`
      );
      return;
    }

    const correct = sameSet(selected, state.current.correctAnswers);
    markAndContinue(correct, selected);
  };
}

function renderQuestion() {
  const question = state.current;

  const chooseHint = question.correctAnswers.length > 1
    ? ` (Elige ${question.correctAnswers.length})`
    : "";
  el.questionText.textContent = question.question + chooseHint;
  el.conceptText.textContent = `Apartado: ${question.concept}`;

  el.choicesContainer.innerHTML = "";
  el.nextBtn.classList.add("hidden");
  hideFeedback();
  el.multiActions.classList.add("hidden");

  if (question.correctAnswers.length > 1) {
    renderMultiChoice(question);
  } else {
    renderSingleChoice(question);
  }
}

function finishQuiz() {
  el.quizCard.classList.add("hidden");
  el.resultsCard.classList.remove("hidden");

  const total = state.ok + state.ko;
  const pct = total > 0 ? (state.ok * 100) / total : 0;

  el.finalSummary.textContent = `Aciertos: ${state.ok} | Fallos: ${state.ko} | Total: ${total}`;
  el.finalPercent.textContent = `${pct.toFixed(1)}%`;

  const rows = Object.entries(state.conceptStats)
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([concept, values]) => {
      const cTotal = values.ok + values.ko;
      const cPct = cTotal > 0 ? ((values.ok * 100) / cTotal).toFixed(1) : "0.0";
      return `<tr><td>${concept}</td><td>${values.ok}</td><td>${values.ko}</td><td>${cPct}%</td></tr>`;
    })
    .join("");

  el.conceptStatsBody.innerHTML = rows;
}

function startQuiz() {
  const max = state.allQuestions.length;
  const requested = Number(el.questionCount.value) || 25;
  const totalTarget = Math.max(5, Math.min(max, requested));

  state.totalTarget = totalTarget;
  state.answered = 0;
  state.ok = 0;
  state.ko = 0;
  state.conceptStats = {};

  state.queue = shuffle(state.allQuestions).slice(0, totalTarget);

  el.setupCard.classList.add("hidden");
  el.resultsCard.classList.add("hidden");
  el.quizCard.classList.remove("hidden");

  updateTopScore();
  getNextQuestion();
}

async function init() {
  try {
    const response = await fetch("./clean-questions-explained.json");
    if (!response.ok) {
      throw new Error(`No se pudo cargar clean-questions-explained.json (${response.status})`);
    }
    const data = await response.json();

    // Transform from new format to quiz format
    state.allQuestions = (data.questions || [])
      .filter((q) => Array.isArray(q.correct) && q.correct.length > 0)
      .map((q) => ({
        question: q.question,
        correctAnswers: q.correct,
        choices: Object.entries(q.options).map(([id, text]) => ({ id, text })),
        concept: q.category || "General",
        explanation: q.explanation || "",
        reference: q.reference || "",
        choose: q.choose || 1
      }));

    el.questionCount.max = String(state.allQuestions.length);
    el.datasetMeta.textContent = `Banco cargado: ${state.allQuestions.length} preguntas con explicaciones detalladas.`;
    el.startBtn.disabled = false;
  } catch (error) {
    el.datasetMeta.textContent = `Error cargando datos: ${error.message}`;
    el.startBtn.disabled = true;
  }
}

el.startBtn.addEventListener("click", startQuiz);
el.restartBtn.addEventListener("click", () => {
  el.resultsCard.classList.add("hidden");
  el.setupCard.classList.remove("hidden");
});
el.nextBtn.addEventListener("click", () => {
  hideFeedback();
  getNextQuestion();
});

init();
