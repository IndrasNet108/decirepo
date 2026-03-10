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
          ${item("Repository", "./index.html", activeItem === "repository")}
          ${item("About", "./about.html", activeItem === "about")}
          ${item("Publish", "./publisher.html", activeItem === "publisher")}
          ${item("Policy Impact", "./policy-impact.html", activeItem === "policy-impact")}
          ${item("Lineage", "./lineage.html", activeItem === "lineage")}
          ${item("Precedents", "./precedents.html", activeItem === "precedents")}
          ${item("Feed", "./feed.html", activeItem === "feed")}
          ${item("Verify", "./verify.html", activeItem === "verify")}
          ${item("Network", "./network.html", activeItem === "network")}
          ${item("Trust", "./trust.html", activeItem === "trust")}
          ${item("Root of Trust", "./root-of-trust.html", activeItem === "root-of-trust")}
          ${item("Protocol", "./protocol.html", activeItem === "protocol")}
          ${item("API", "../api/feed.json", activeItem === "api", true)}
        </nav>
      </header>
      <div class="header-divider"></div>
    `;
  }

  window.DeciRepoHeader = { mount };
})();
