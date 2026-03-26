(function () {
  function item(label, href, active, external = false) {
    const cls = active ? "menu-link active" : "menu-link";
    const attrs = external ? ` target="_blank" rel="noopener noreferrer"` : "";
    return `<a class="${cls}" href="${href}"${attrs}>${label}</a>`;
  }

  function mount(targetId, activeItem) {
    const root = document.getElementById(targetId);
    if (!root) return;

    root.innerHTML = `
      <header class="site-header">
        <div class="brand-stack">
          <div class="brand-top">
            <img class="brand-logo-dr" src="../assets/brand/dr-logo-header.png" alt="DeciRepo logo" />
            <span class="brand-registry">DeciRepo</span>
          </div>
        <div class="brand-subline">
          <span class="brand-sub">Powered by DLX deterministic engine</span>
        </div>
        </div>
        <nav class="header-menu" aria-label="Primary">
          ${item("Home", "./index.html", activeItem === "repository" || activeItem === "home")}
          ${item("About", "./about.html", activeItem === "about")}
          ${item("Cases", "./cases.html", activeItem === "cases")}
          ${item("Proof", "./proof.html", activeItem === "proof")}
          ${item("Request Pilot", "./billing.html#request-pilot", activeItem === "request-pilot" || activeItem === "billing")}
        </nav>
      </header>
      <div class="header-divider"></div>
    `;
  }

  window.DeciRepoHeader = { mount };
})();
