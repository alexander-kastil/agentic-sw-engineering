(function () {
  "use strict";

  const data = window.DASHBOARD_DATA;
  if (!data) {
    document.getElementById("rows").innerHTML =
      '<tr><td colspan="5" style="padding:24px;text-align:center;color:var(--planned-fg)">Dashboard data not found. Run <code>python dashboard/render-dashboard.py</code>.</td></tr>';
    return;
  }

  const repo = data.project.repo;
  const issueUrl = (n) => `https://github.com/${repo}/issues/${n}`;
  const moduleUrl = (path) => `https://github.com/${repo}/tree/master/${path}`;

  // --- Header
  document.title = `Class Progress · ${data.project.title}`;
  document.getElementById("project-title").textContent = data.project.title;
  document.getElementById("title").textContent = data.project.title;
  document.getElementById("project-link").href = `https://github.com/${repo}`;

  const s = data.summary;
  document.getElementById("summary").textContent =
    `${s.totalModules} modules · ${s.done}/${s.totalSubs} sub-items done · ${s.percent}% complete`;

  // --- Row rendering
  const rowsEl = document.getElementById("rows");
  const expanded = new Set();

  function subIcon(status) {
    const mark = status === "done" ? "✓" : "";
    return `<span class="sub-icon icon-${status}" title="${status}">${mark}</span>`;
  }
  function statusPill(status) {
    return `<span class="status-pill ${status}">${status}</span>`;
  }
  function assigneeCell(user) {
    if (!user) return `<span class="assignee-unassigned">unassigned</span>`;
    return (
      `<a class="assignee" href="https://github.com/${user}" target="_blank" rel="noopener">` +
      `<img src="https://github.com/${user}.png?size=40" alt="" loading="lazy" />` +
      `<span class="assignee-name">@${user}</span>` +
      `</a>`
    );
  }
  function contributorChips(contributors) {
    if (!contributors || !contributors.length) return "";
    return contributors.map((handle) =>
      `<a class="contrib-chip" href="https://github.com/${handle}" target="_blank" rel="noopener" title="@${handle}">` +
      `<img src="https://github.com/${handle}.png?size=40" alt="@${handle}" loading="lazy" />` +
      `<span class="contrib-name">@${handle}</span></a>`
    ).join("");
  }
  function progressCell(done, total) {
    const pct = Math.round((done / total) * 100);
    const segs = Array.from({ length: total })
      .map((_, i) => {
        const filled = i < done ? " filled" : "";
        return `<span class="bar-seg step-${i + 1}${filled}"></span>`;
      })
      .join("");
    return (
      `<span class="progress">` +
      `<span class="count">${done} / ${total}</span>` +
      `<span class="bar">${segs}</span>` +
      `<span class="pct">${pct}%</span>` +
      `</span>`
    );
  }

  function moduleMatches(mod, q, statusFilter) {
    if (statusFilter && mod.status !== statusFilter) {
      if (!mod.subItems.some((si) => si.status === statusFilter)) return false;
    }
    if (q) {
      const hay =
        `${mod.num} ${mod.name} ${mod.assignee || ""} ` +
        mod.subItems.map((si) => si.label).join(" ");
      if (!hay.toLowerCase().includes(q.toLowerCase())) return false;
    }
    return true;
  }

  function render() {
    const q = document.getElementById("filter").value.trim();
    const statusFilter = document.getElementById("status-filter").value;
    const visible = data.modules.filter((m) => moduleMatches(m, q, statusFilter));

    rowsEl.innerHTML = "";
    visible.forEach((mod, idx) => {
      const tr = document.createElement("tr");
      const isOpen = expanded.has(mod.num);
      tr.className = isOpen ? "row-module open" : "row-module";
      tr.dataset.num = mod.num;
      tr.dataset.toggle = mod.num;
      const displayName = mod.fullName || `Module ${mod.num} - ${mod.name}`;
      const titleLink = mod.path
        ? `<a class="title-text" href="${moduleUrl(mod.path)}" target="_blank" rel="noopener">${displayName}</a>`
        : `<span class="title-text">${displayName}</span>`;

      tr.innerHTML =
        `<td class="row-num">${idx + 1}</td>` +
        `<td><span class="title-cell"><span class="row-chevron"></span>${titleLink}</span></td>` +
        `<td class="assignee-cell">${assigneeCell(mod.assignee)}</td>` +
        `<td class="progress-cell">${progressCell(mod.progress.done, mod.progress.total)}</td>` +
        `<td>${statusPill(mod.status)}</td>`;

      rowsEl.appendChild(tr);

      if (isOpen) {
        const statusOf = (key) =>
          (mod.subItems.find((s) => s.key === key) || {}).status || "planned";

        const topics = mod.topics || [];
        const labs = mod.labs || [];

        if (topics.length) {
          const hdr = document.createElement("tr");
          hdr.className = "row-section";
          hdr.innerHTML =
            `<td></td>` +
            `<td colspan="3"><span class="section-label">Topics</span></td>` +
            `<td>${statusPill(statusOf("theory"))}</td>`;
          rowsEl.appendChild(hdr);

          topics.forEach((topic) => {
            const tr = document.createElement("tr");
            tr.className = "row-sub";
            const href = `https://github.com/${repo}/tree/master/${topic.path}`;
            tr.innerHTML =
              `<td></td>` +
              `<td><span class="title-cell topic-title">` +
              `<a class="title-text" href="${href}" target="_blank" rel="noopener">${topic.title}</a>` +
              `</span></td>` +
              `<td class="contrib-cell">${contributorChips(topic.contributors)}</td>` +
              `<td></td><td></td>`;
            rowsEl.appendChild(tr);
          });
        }

        const allDemos = mod.demos || [];
        if (allDemos.length) {
          const hdr = document.createElement("tr");
          hdr.className = "row-section";
          hdr.innerHTML =
            `<td></td>` +
            `<td colspan="3"><span class="section-label">Demos</span></td>` +
            `<td>${statusPill(statusOf("demos"))}</td>`;
          rowsEl.appendChild(hdr);

          allDemos.forEach((demo) => {
            const tr = document.createElement("tr");
            tr.className = "row-sub";
            const href = demo.path
              ? `https://github.com/${repo}/blob/master/${demo.path}`
              : null;
            tr.innerHTML =
              `<td></td>` +
              `<td><span class="title-cell topic-title">` +
              (href
                ? `<a class="title-text" href="${href}" target="_blank" rel="noopener">${demo.title}</a>`
                : `<span class="title-text">${demo.title}</span>`) +
              `</span></td>` +
              `<td class="contrib-cell">${contributorChips(demo.contributors)}</td>` +
              `<td></td><td></td>`;
            rowsEl.appendChild(tr);
          });
        }

        if (labs.length) {
          const labsHref = mod.path
            ? `https://github.com/${repo}/tree/master/${mod.path}/labs`
            : null;
          const labsLabel = labsHref
            ? `<a class="section-link" href="${labsHref}" target="_blank" rel="noopener">Labs</a>`
            : "Labs";
          const hdr = document.createElement("tr");
          hdr.className = "row-section";
          hdr.innerHTML =
            `<td></td>` +
            `<td colspan="3"><span class="section-label">${labsLabel}</span></td>` +
            `<td>${statusPill(statusOf("labs"))}</td>`;
          rowsEl.appendChild(hdr);

          labs.forEach((lab) => {
            const tr = document.createElement("tr");
            tr.className = "row-sub";
            const isFile = lab.path.endsWith(".md");
            const href = `https://github.com/${repo}/${isFile ? "blob" : "tree"}/master/${lab.path}`;
            const displayTitle = lab.title.replace(/^Lab \d+ — /, "");
            tr.innerHTML =
              `<td></td>` +
              `<td><span class="title-cell topic-title">` +
              `<a class="title-text" href="${href}" target="_blank" rel="noopener">${displayTitle}</a>` +
              `</span></td>` +
              `<td class="contrib-cell">${contributorChips(lab.contributors)}</td>` +
              `<td></td><td></td>`;
            rowsEl.appendChild(tr);
          });
        }

        const slidesItem = mod.subItems.find((s) => s.key === "slides");
        if (slidesItem) {
          const slidesHref = mod.path
            ? `https://github.com/${repo}/tree/master/${mod.path}/pptx`
            : null;
          const slidesLabel = slidesHref
            ? `<a class="section-link" href="${slidesHref}" target="_blank" rel="noopener">Slides</a>`
            : "Slides";
          const tr = document.createElement("tr");
          tr.className = "row-section";
          tr.innerHTML =
            `<td></td>` +
            `<td colspan="3"><span class="section-label">${slidesLabel}</span></td>` +
            `<td>${statusPill(statusOf("slides"))}</td>`;
          rowsEl.appendChild(tr);
        }
      }
    });

    document.getElementById("empty").hidden = visible.length > 0;
  }

  // --- Events
  let _mdRow = null;

  rowsEl.addEventListener("mousedown", (e) => {
    if (e.button !== 0 || e.target.closest("a")) { _mdRow = null; return; }
    _mdRow = e.target.closest("tr[data-toggle]");
  });

  rowsEl.addEventListener("click", (e) => {
    if (e.target.closest("a")) return;
    const row = e.target.closest("tr[data-toggle]");
    if (!row || row !== _mdRow) { _mdRow = null; return; }
    _mdRow = null;
    const num = row.dataset.toggle;
    if (expanded.has(num)) expanded.delete(num);
    else expanded.add(num);
    render();
  });

  document.getElementById("filter").addEventListener("input", render);
  document.getElementById("status-filter").addEventListener("change", render);
  document.getElementById("expand-all").addEventListener("click", () => {
    data.modules.forEach((m) => expanded.add(m.num));
    render();
  });
  document.getElementById("collapse-all").addEventListener("click", () => {
    expanded.clear();
    render();
  });

  render();

  // --- Contributors
  function renderContributors() {
    const list = document.getElementById("contributors-list");
    if (!list || !data.contributors || !data.contributors.length) return;
    list.innerHTML = data.contributors.map((c) => {
      const avatar = c.github
        ? `<img src="https://github.com/${c.github}.png?size=40" alt="" loading="lazy" />`
        : `<span class="contributor-avatar-placeholder"></span>`;
      const nameLink = c.github
        ? `<a href="https://github.com/${c.github}" target="_blank" rel="noopener">@${c.github}</a>`
        : `<span>${c.name}</span>`;
      return (
        `<div class="contributor-card">` +
        `<div class="contributor-avatar">${avatar}</div>` +
        `<div class="contributor-info">` +
        `<div class="contributor-name">${nameLink}</div>` +
        `<div class="contributor-meta">${c.commits} commit${c.commits !== 1 ? "s" : ""} &middot; ${c.linesAdded.toLocaleString()} lines added</div>` +
        `<div class="contributor-bar-row">` +
        `<div class="contributor-bar"><div class="contributor-bar-fill" style="width:${c.percent}%"></div></div>` +
        `<span class="contributor-pct">${c.percent}%</span>` +
        `</div>` +
        `</div>` +
        `</div>`
      );
    }).join("");
  }

  renderContributors();
})();
