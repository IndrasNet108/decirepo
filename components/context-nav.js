(function () {
  function renderLink(item) {
    const label = item.label || "Link";
    if (!item.href || item.active) {
      const cls = item.active ? "btn btn-gold small disabled" : "btn small disabled";
      return `<span class="${cls}" aria-current="${item.active ? "page" : "false"}">${label}</span>`;
    }
    const attrs = item.external ? ` target="_blank" rel="noopener noreferrer"` : "";
    const cls = item.primary ? "btn btn-gold small" : "btn small";
    return `<a class="${cls}" href="${item.href}"${attrs}>${label}</a>`;
  }

  function mount(targetId, options) {
    const root = document.getElementById(targetId);
    if (!root) return;

    const current = options && options.current ? options.current : "Context";
    const meta = options && options.meta ? options.meta : "";
    const hint = options && options.hint ? options.hint : "";
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
