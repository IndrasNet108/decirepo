(function () {
  function toRows(obj) {
    return Object.entries(obj || {}).map(([k, v]) => ({ key: k, value: String(v) }));
  }

  function renderTwoColumnGrid(rows) {
    return `
      <div class="kv-two-column">
        ${rows
          .map(
            (r) => `
          <div class="kv-item">
            <div class="kv-key">${r.key}</div>
            <div class="kv-value">${r.value}</div>
          </div>
        `
          )
          .join("")}
      </div>
    `;
  }

  function renderStack(rows, monoKeys) {
    const mono = new Set(monoKeys || []);
    return `
      <div class="kv-stack">
        ${rows
          .map(
            (r) => `
          <div class="kv-line">
            <div class="kv-key">${r.key}</div>
            <div class="kv-value ${mono.has(r.key) ? "mono" : ""}">${r.value}</div>
          </div>
        `
          )
          .join("")}
      </div>
    `;
  }

  window.DeciRepoDecisionBlock = {
    toRows,
    renderTwoColumnGrid,
    renderStack
  };
})();
