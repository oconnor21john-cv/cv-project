const form = document.getElementById("searchForm");
const input = document.getElementById("q");
const grid = document.getElementById("grid");
const meta = document.getElementById("meta");
const pill = document.getElementById("statusPill");
const message = document.getElementById("message");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const pageInfo = document.getElementById("pageInfo");

const modal = document.getElementById("modal");
const backdrop = document.getElementById("backdrop");
const closeBtn = document.getElementById("closeBtn");
const modalTitle = document.getElementById("modalTitle");
const modalSub = document.getElementById("modalSub");
const modalBody = document.getElementById("modalBody");

const state = {
  q: "pasta",
  offset: 0,
  number: 12,
  totalResults: null,
};

function setLoading(isLoading) {
  grid.setAttribute("aria-busy", String(isLoading));
  pill.hidden = !isLoading;
  if (isLoading) pill.textContent = "Loading…";
}

function showMessage(text) {
  message.textContent = text;
  message.hidden = !text;
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function updatePager() {
  const page = Math.floor(state.offset / state.number) + 1;
  pageInfo.textContent = `Page ${page}`;

  prevBtn.disabled = state.offset <= 0;
  const total = typeof state.totalResults === "number" ? state.totalResults : null;
  const hasMore =
    total === null ? true : state.offset + state.number < total;
  nextBtn.disabled = !hasMore;
}

function renderResults(data) {
  const results = Array.isArray(data?.results) ? data.results : [];
  const total = typeof data?.totalResults === "number" ? data.totalResults : null;
  state.totalResults = total;

  meta.textContent =
    total === null
      ? `Showing ${results.length} results for “${state.q}”.`
      : `Showing ${results.length} of ${total} results for “${state.q}”.`;

  updatePager();

  if (!results.length) {
    grid.innerHTML = "";
    showMessage("No results. Try a different search.");
    return;
  }

  showMessage("");
  grid.innerHTML = results
    .map((r) => {
      const title = escapeHtml(r.title ?? "Untitled");
      const img = r.image ? `<img class="thumb" src="${escapeHtml(r.image)}" alt="${title}" loading="lazy" />` : `<div class="thumb" aria-hidden="true"></div>`;
      const id = r.id ?? "";
      return `
        <article class="card">
          <button class="card-btn" type="button" data-recipe-id="${escapeHtml(id)}" aria-label="Open details for ${title}">
            ${img}
            <div class="card-body">
              <p class="title">${title}</p>
              <p class="sub">
                <span>Recipe ID</span>
                <span>${escapeHtml(id)}</span>
              </p>
            </div>
          </button>
        </article>
      `;
    })
    .join("");
}

function openModal() {
  modal.hidden = false;
  document.body.style.overflow = "hidden";
}

function closeModal() {
  modal.hidden = true;
  document.body.style.overflow = "";
  modalTitle.textContent = "Recipe";
  modalSub.textContent = "";
  modalBody.innerHTML = "";
}

function stripHtml(html) {
  // Spoonacular summary is HTML
  const tmp = document.createElement("div");
  tmp.innerHTML = String(html ?? "");
  return tmp.textContent || tmp.innerText || "";
}

function buildFact(k, v) {
  return `
    <div class="fact">
      <p class="k">${escapeHtml(k)}</p>
      <p class="v">${escapeHtml(v)}</p>
    </div>
  `;
}

async function loadDetails(id) {
  openModal();
  modalTitle.textContent = "Loading…";
  modalSub.textContent = `Recipe ID ${id}`;
  modalBody.innerHTML = "";

  try {
    const res = await fetch(`/api/recipes/${encodeURIComponent(id)}`);
    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      modalTitle.textContent = "Couldn’t load details";
      modalSub.textContent = data?.error ? String(data.error) : `Error (${res.status})`;
      return;
    }

    const title = data?.title ?? `Recipe ${id}`;
    modalTitle.textContent = title;
    modalSub.textContent = data?.sourceName ? String(data.sourceName) : "Spoonacular";

    const img = data?.image
      ? `<img class="modal-img" src="${escapeHtml(data.image)}" alt="${escapeHtml(title)}" loading="lazy" />`
      : `<div class="modal-img" aria-hidden="true"></div>`;

    const facts = [
      ["Ready in", data?.readyInMinutes ? `${data.readyInMinutes} mins` : "—"],
      ["Servings", data?.servings ?? "—"],
      ["Vegetarian", data?.vegetarian ? "Yes" : "No"],
      ["Vegan", data?.vegan ? "Yes" : "No"],
    ];

    const sourceUrl = data?.sourceUrl
      ? `<a href="${escapeHtml(data.sourceUrl)}" target="_blank" rel="noreferrer">Open full recipe</a>`
      : "";

    const summaryText = stripHtml(data?.summary);

    modalBody.innerHTML = `
      <div>
        ${img}
      </div>
      <div>
        <div class="facts">
          ${facts.map(([k, v]) => buildFact(k, v)).join("")}
        </div>
        ${sourceUrl ? `<p class="muted" style="margin-top:10px">${sourceUrl}</p>` : ""}
        ${summaryText ? `<p class="summary">${escapeHtml(summaryText)}</p>` : ""}
      </div>
    `;
  } catch (e) {
    modalTitle.textContent = "Network error";
    modalSub.textContent = String(e);
  }
}

async function runSearch(query, offset = 0) {
  const q = (query ?? "").trim() || "pasta";
  state.q = q;
  state.offset = Math.max(0, Number(offset) || 0);

  setLoading(true);
  showMessage("");
  meta.textContent = "Searching…";
  updatePager();

  try {
    const params = new URLSearchParams();
    params.set("q", q);
    params.set("offset", String(state.offset));
    params.set("number", String(state.number));

    const res = await fetch(`/api/recipes?${params.toString()}`);
    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      const errMsg = data?.error ? String(data.error) : `Request failed (${res.status})`;
      showMessage(errMsg);
      meta.textContent = "Couldn’t load results.";
      grid.innerHTML = "";
      return;
    }

    renderResults(data);
  } catch (e) {
    showMessage(`Network error: ${String(e)}`);
    meta.textContent = "Couldn’t load results.";
    grid.innerHTML = "";
  } finally {
    setLoading(false);
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  runSearch(input.value, 0);
});

prevBtn.addEventListener("click", () => {
  runSearch(state.q, Math.max(0, state.offset - state.number));
});

nextBtn.addEventListener("click", () => {
  runSearch(state.q, state.offset + state.number);
});

grid.addEventListener("click", (e) => {
  const btn = e.target.closest("[data-recipe-id]");
  if (!btn) return;
  const id = btn.getAttribute("data-recipe-id");
  if (!id) return;
  loadDetails(id);
});

closeBtn.addEventListener("click", closeModal);
backdrop.addEventListener("click", closeModal);
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && !modal.hidden) closeModal();
});

// Initial load
runSearch("pasta", 0);

