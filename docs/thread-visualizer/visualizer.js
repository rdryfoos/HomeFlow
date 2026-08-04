/* Thread Visualizer — renders walker JSON only. No ID truth stored here. */

const state = {
  intact: null,
  broken: null,
  mode: "intact", // intact | broken
  selectedId: null,
};

const $ = (id) => document.getElementById(id);

async function loadJson(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Failed to load ${path}: ${res.status}`);
  return res.json();
}

function currentPayload() {
  return state.mode === "broken" ? state.broken : state.intact;
}

function threadById(id) {
  return currentPayload().threads.find((t) => t.id === id);
}

function renderTotals(payload) {
  const t = payload.totals;
  const gateOk = t.gate2Passed && state.mode === "intact";
  $("totals").innerHTML = `
    <div class="stat"><span class="n">${t.registryIds}</span><span class="l">Registry IDs</span></div>
    <div class="stat"><span class="n">${t.acs}</span><span class="l">Acceptance criteria</span></div>
    <div class="stat ${gateOk ? "is-ok" : ""}"><span class="n">${t.acsWithTests}</span><span class="l">ACs with tests</span></div>
    <div class="stat ${gateOk ? "is-ok" : "is-bad"}"><span class="n">${gateOk ? "PASS" : (state.mode === "broken" ? "GAP" : "FAIL")}</span><span class="l">Gate 2 lens</span></div>
  `;
}

function fillSelect(payload) {
  const select = $("threadSelect");
  const preferred =
    state.selectedId ||
    payload.defaultDescentId ||
    payload.demoBreakId ||
    payload.threads[0]?.id;
  select.innerHTML = payload.threads
    .map((t) => {
      const label = `${t.id} — ${t.status}`;
      return `<option value="${t.id}">${label}</option>`;
    })
    .join("");
  if (preferred && [...select.options].some((o) => o.value === preferred)) {
    select.value = preferred;
  }
  state.selectedId = select.value;
}

function moduleList(modules) {
  if (!modules.length) {
    return `<p>No <code>@covers</code> modules found for this ID in <code>ios/HomesFlow</code>.</p>`;
  }
  return `<ul>${modules
    .map((m) => `<li><code>${m.path}</code></li>`)
    .join("")}</ul>`;
}

function proofList(tests, isGap) {
  if (!tests.length) {
    return isGap
      ? `<p><strong>No named proof.</strong> Gate&nbsp;2 would fail the build on this silent gap.</p>`
      : `<p>No <code>test_AC_*</code> yet — tracked as debt if a pending task exists.</p>`;
  }
  return `<ul>${tests
    .map((t) => {
      const where = t.path ? ` <span class="muted">in <code>${t.path}</code></span>` : "";
      return `<li><code>${t.name}</code>${where}</li>`;
    })
    .join("")}</ul>`;
}

function renderDescent() {
  const payload = currentPayload();
  const thread = threadById(state.selectedId);
  const root = $("descent");
  if (!thread) {
    root.innerHTML = `<p>Thread not found.</p>`;
    return;
  }

  const broken = thread.status === "GAP";
  root.classList.toggle("is-broken", broken);

  const reqText =
    thread.requirement.text ||
    "(AC text not found in PRD — check HomesFlow.prd.md formatting.)";

  root.innerHTML = `
    <article class="tier requirement">
      <p class="eyebrow">Requirement</p>
      <span class="id-chip">${thread.id}</span>
      <h2>${escapeHtml(reqText)}</h2>
      <p>Source: <code>${thread.requirement.source}</code></p>
      ${
        thread.requirement.doneTasks.length
          ? `<p>Done tasks: <code>${thread.requirement.doneTasks.join(", ")}</code></p>`
          : ""
      }
    </article>
    <div class="connector" aria-hidden="true"></div>
    <article class="tier implementation">
      <p class="eyebrow">Implementation</p>
      <span class="id-chip">@covers ${thread.id}</span>
      <h2>${thread.implementation.covered ? "Authorized in source" : "No @covers yet"}</h2>
      ${moduleList(thread.implementation.modules)}
    </article>
    <div class="connector proof-link" aria-hidden="true"></div>
    <article class="tier proof ${broken ? "is-gap" : ""}">
      <p class="eyebrow">Proof</p>
      <span class="id-chip">test_AC_*</span>
      <h2>${broken ? "Thread broken" : "Named tests verify this AC"}</h2>
      ${proofList(thread.proof.tests, broken)}
      <span class="status-pill ${thread.status}">${thread.status}</span>
    </article>
    ${
      broken
        ? `<p class="pitch">Watch — when the proof disappears, the thread shows it, and the build fails. You cannot quietly break this.</p>`
        : ""
    }
  `;
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderScale() {
  const payload = currentPayload();
  $("scaleList").innerHTML = payload.threads
    .map((t) => {
      const text = escapeHtml(t.requirement.text || "");
      return `<div class="scale-row" data-id="${t.id}" role="button" tabindex="0">
        <span class="sid">${t.id}</span>
        <span class="stext" title="${text}">${text}</span>
        <span class="sstatus status-pill ${t.status}">${t.status}</span>
      </div>`;
    })
    .join("");

  $("scaleList").querySelectorAll(".scale-row").forEach((row) => {
    const go = () => {
      state.selectedId = row.dataset.id;
      $("threadSelect").value = state.selectedId;
      renderDescent();
      window.scrollTo({ top: $("descent").offsetTop - 24, behavior: "smooth" });
    };
    row.addEventListener("click", go);
    row.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        go();
      }
    });
  });
}

function renderMeta(payload) {
  const demoNote =
    state.mode === "broken" && payload.demo?.note
      ? ` · Demo: ${payload.demo.note}`
      : "";
  $("meta").textContent =
    `Generated ${payload.generatedAt} @ ${payload.commit}` + demoNote;
}

function renderAll() {
  const payload = currentPayload();
  renderTotals(payload);
  fillSelect(payload);
  renderDescent();
  renderScale();
  renderMeta(payload);
}

function setMode(mode) {
  state.mode = mode;
  $("btnIntact").classList.toggle("is-active", mode === "intact");
  $("btnBreak").classList.toggle("is-active", mode === "broken");
  if (mode === "broken") {
    state.selectedId = state.broken.demoBreakId || state.broken.defaultDescentId;
  }
  renderAll();
}

async function boot() {
  try {
    const [intact, broken] = await Promise.all([
      loadJson("data/thread.json"),
      loadJson("data/thread-broken.json"),
    ]);
    state.intact = intact;
    state.broken = broken;
    state.selectedId = intact.defaultDescentId || intact.demoBreakId;

    // Sanity: walker totals must echo Gate 2 on the intact snapshot.
    const t = intact.totals;
    console.info(
      `[thread-visualizer] Gate 2 lens: ${t.registryIds} IDs, ${t.acs} ACs, ${t.acsWithTests} with tests, passed=${t.gate2Passed}`
    );

    $("threadSelect").addEventListener("change", (e) => {
      state.selectedId = e.target.value;
      renderDescent();
    });
    $("btnIntact").addEventListener("click", () => setMode("intact"));
    $("btnBreak").addEventListener("click", () => setMode("broken"));

    setMode("intact");
  } catch (err) {
    document.body.insertAdjacentHTML(
      "afterbegin",
      `<p style="margin:2rem;color:#a33b2b;font-family:sans-serif">
        Failed to load thread data. Run
        <code>bash scripts/thread-visualizer-refresh.sh</code>
        then reopen this page. (${escapeHtml(err.message)})
      </p>`
    );
    console.error(err);
  }
}

boot();
