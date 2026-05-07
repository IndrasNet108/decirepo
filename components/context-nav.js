(function () {
  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function renderLink(item) {
    const label = escapeHtml(item.label || "Link");
    if (!item.href || item.active) {
      const cls = item.active ? "btn btn-gold small disabled" : "btn small disabled";
      return `<span class="${cls}" aria-current="${item.active ? "page" : "false"}">${label}</span>`;
    }
    const href = escapeHtml(item.href);
    const attrs = item.external ? ` target="_blank" rel="noopener noreferrer"` : "";
    const cls = item.primary ? "btn btn-gold small" : "btn small";
    return `<a class="${cls}" href="${href}"${attrs}>${label}</a>`;
  }

  function mount(targetId, options) {
    const root = document.getElementById(targetId);
    if (!root) return;

    const current = escapeHtml(options && options.current ? options.current : "Context");
    const meta = escapeHtml(options && options.meta ? options.meta : "");
    const hint = escapeHtml(options && options.hint ? options.hint : "");
    const links = options && Array.isArray(options.links) ? options.links : [];

    root.innerHTML = `
      <section class="panel context-nav-panel">
        <div class="context-nav-head">
          <div class="context-nav-title">Workflow Navigation</div>
          <div class="context-nav-meta">Current: ${current}${meta ? ` · ${meta}` : ""}</div>
          ${hint ? `<div class="context-nav-hint">${hint}</div>` : ""}
        </div>
        <div class="context-nav-row">
          ${links.map(renderLink).join("")}
        </div>
      </section>
    `;
  }

  window.DeciRepoContextNav = { mount };
})();
