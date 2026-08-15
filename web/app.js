const $ = (selector, root = document) => root.querySelector(selector);

const EXAMPLE = {
  project_name: "Campus Cart",
  audience: "students living on campus",
  problem: "finding a ride home after late labs",
  approach: "find a ride home by matching with an open seat heading the same way",
};

const inputNames = ["project_name", "audience", "problem", "approach"];
let lastBrief = null;
let apiAvailable = false;
let toastTimer;

function formValues() {
  return Object.fromEntries(inputNames.map(name => [name, $(`[name="${name}"]`).value.trim()]));
}

function makeLocalBrief(values) {
  const { project_name, audience, problem, approach } = values;
  const problemText = problem.replace(/[ .!?]+$/, "");
  const approachText = approach.replace(/[ .!?]+$/, "");
  return {
    project_name,
    one_liner: `${project_name} tests whether ${audience} will ${approachText}.`,
    problem_statement: `A current pain to validate: ${problemText}.`,
    hypothesis: `We think ${audience} may use this to address ${problemText}. That is an assumption to test.`,
    mvp: [
      `One primary flow: help ${audience} ${approachText}.`,
      `One visible outcome connected to: ${problemText}.`,
      "One feedback step; defer integrations until a user test supports them.",
    ],
    first_test: {
      method: `Show a clickable prototype to five people from ${audience}.`,
      task: `Ask each person to try the core action: ${approachText}.`,
      success_signal: "Starting threshold: at least 3 of 5 complete the task without coaching. Adjust this before using it with real participants.",
    },
    interview_questions: [
      `What happened the last time you faced this: ${problemText}?`,
      "What did you try, and what was frustrating about that?",
      "What would need to change before you would try a solution like this?",
    ],
    assumptions_to_check: [
      "This problem happens often enough for someone to try a new approach.",
      "The named audience can be reached for a prototype test.",
    ],
    mode: "deterministic-template",
    model_used: false,
    notice: "Draft generated from the submitted text with fixed templates; no model or outside research was used.",
  };
}

function setConnection(mode) {
  const connection = $(".connection");
  connection.classList.remove("connected", "offline");
  if (mode === "api") {
    connection.classList.add("connected");
    $("#connection-label").textContent = "FastAPI · baseline";
  } else {
    connection.classList.add("offline");
    $("#connection-label").textContent = "Static fallback · offline";
  }
}

async function detectApi() {
  try {
    const response = await fetch("/api/health", { headers: { Accept: "application/json" } });
    if (!response.ok) throw new Error("API unavailable");
    const status = await response.json();
    apiAvailable = status.ok === true;
    setConnection(apiAvailable ? "api" : "static");
  } catch {
    apiAvailable = false;
    setConnection("static");
  }
}

function showBrief(brief, mode) {
  lastBrief = brief;
  $("#brief-name").textContent = brief.project_name;
  $("#one-liner").textContent = brief.one_liner;
  $("#problem-statement").textContent = brief.problem_statement;
  $("#hypothesis").textContent = brief.hypothesis;
  $("#test-method").textContent = brief.first_test.method;
  $("#test-task").textContent = brief.first_test.task;
  $("#test-signal").textContent = brief.first_test.success_signal;
  $("#output-notice").textContent = brief.notice;

  const mvpList = $("#mvp-list");
  mvpList.replaceChildren();
  brief.mvp.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    mvpList.append(li);
  });

  const questionList = $("#question-list");
  questionList.replaceChildren();
  brief.interview_questions.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    questionList.append(li);
  });

  const assumptions = $("#assumption-list");
  assumptions.replaceChildren();
  brief.assumptions_to_check.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    assumptions.append(li);
  });

  $("#output-empty").classList.add("hidden");
  $("#brief-output").classList.remove("hidden");
  const modeBadge = $("#draft-mode");
  modeBadge.classList.toggle("live", mode === "api");
  const modeDot = document.createElement("span");
  modeDot.className = "draft-mode-dot";
  modeBadge.replaceChildren(modeDot, document.createTextNode(mode === "api" ? "FASTAPI · RULE-BASED" : mode === "sample" ? "STATIC SAMPLE" : "STATIC FALLBACK"));
}

function showError(message) {
  $("#form-error").textContent = message;
}

async function draftBrief() {
  const form = $("#brief-form");
  if (!form.reportValidity()) return;
  const values = formValues();
  const button = $("#build-button");
  button.disabled = true;
  button.textContent = "Drafting…";
  showError("");
  try {
    if (apiAvailable) {
      try {
        const response = await fetch("/api/brief", {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(values),
        });
        if (response.status === 404) {
          apiAvailable = false;
          setConnection("static");
        } else if (!response.ok) {
          const error = await response.json();
          const first = error.detail?.[0]?.msg;
          throw new Error(first || "The API could not make this draft.");
        } else {
          showBrief(await response.json(), "api");
          return;
        }
      } catch (error) {
        if (error instanceof TypeError) {
          apiAvailable = false;
          setConnection("static");
        } else {
          throw error;
        }
      }
    }
    showBrief(makeLocalBrief(values), "fallback");
  } catch (error) {
    showError(error.message || "Could not draft this brief.");
  } finally {
    button.disabled = false;
    button.innerHTML = 'Draft my brief <span aria-hidden="true">→</span>';
  }
}

function plainText(brief) {
  return [
    brief.project_name,
    brief.one_liner,
    "",
    `Problem to test: ${brief.problem_statement}`,
    `Hypothesis: ${brief.hypothesis}`,
    "",
    "First MVP cut:",
    ...brief.mvp.map(item => `- ${item}`),
    "",
    "First test:",
    brief.first_test.method,
    brief.first_test.task,
    brief.first_test.success_signal,
    "",
    "Ask before you build:",
    ...brief.interview_questions.map(item => `- ${item}`),
    "",
    "Assumptions to check:",
    ...brief.assumptions_to_check.map(item => `- ${item}`),
    "",
    brief.notice,
  ].join("\n");
}

async function copyBrief() {
  if (!lastBrief) return;
  const text = plainText(lastBrief);
  try {
    await navigator.clipboard.writeText(text);
    toast("Brief copied.");
  } catch {
    const area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.className = "clipboard-fallback";
    document.body.append(area);
    area.select();
    const copied = document.execCommand("copy");
    area.remove();
    toast(copied ? "Brief copied." : "Clipboard access was unavailable.");
  }
}

function toast(message) {
  const note = document.createElement("div");
  note.className = "toast";
  note.setAttribute("role", "status");
  note.textContent = message;
  document.body.append(note);
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => note.remove(), 2300);
}

document.addEventListener("DOMContentLoaded", async () => {
  if (localStorage.getItem("hack-starter-banner-dismissed") === "1") $("#preview-banner").classList.add("dismissed");
  const textarea = $("#approach");
  const count = () => { $("#input-count").textContent = `${textarea.value.length} / 240`; };
  textarea.addEventListener("input", count);
  $("#brief-form").addEventListener("submit", event => { event.preventDefault(); draftBrief(); });
  $("#sample-button").addEventListener("click", () => {
    inputNames.forEach(name => { $(`[name="${name}"]`).value = EXAMPLE[name]; });
    count();
    draftBrief();
  });
  $("#copy-button").addEventListener("click", copyBrief);
  $("#banner-close").addEventListener("click", () => {
    $("#preview-banner").classList.add("dismissed");
    localStorage.setItem("hack-starter-banner-dismissed", "1");
  });

  inputNames.forEach(name => { $(`[name="${name}"]`).value = EXAMPLE[name]; });
  count();
  showBrief(makeLocalBrief(EXAMPLE), "sample");
  await detectApi();
  if (apiAvailable && lastBrief) {
    try {
      const response = await fetch("/api/brief", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(EXAMPLE),
      });
      if (response.ok) showBrief(await response.json(), "api");
    } catch { /* The visible local sample remains usable if the API drops. */ }
  }
});
