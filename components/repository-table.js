(function () {
  function outcomeClass(outcome) {
    if (outcome === "APPROVED") return "outcome-approved";
    if (outcome === "REJECTED") return "outcome-rejected";
    return "outcome-neutral";
  }

  function mount(targetId, rows) {
    const root = document.getElementById(targetId);
    if (!root) return;

    const table = `
      <table class="repo-table" role="grid">
        <thead>
          <tr>
            <th>Decision ID</th>
            <th>Title</th>
            <th>Outcome</th>
            <th>Policy</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          ${rows
            .map(
              (r) => `
            <tr class="repo-row" data-id="${r.id}">
              <td>
                <span class="canonical-id">◢${r.short_hash || String(r.canonical_id || "").replace(/^[^0-9A-Fa-f]*/, "").slice(0, 6).toUpperCase()}</span>
                <span class="legacy-id">${r.id}</span>
              </td>
              <td>${r.title}</td>
              <td class="${outcomeClass(r.outcome)}">${r.outcome}</td>
              <td>${r.policy}</td>
              <td>${r.date}</td>
            </tr>
          `
            )
            .join("")}
        </tbody>
      </table>
    `;

    root.innerHTML = table;

    root.querySelectorAll(".repo-row").forEach((row) => {
      row.addEventListener("click", () => {
        const id = row.getAttribute("data-id");
        if (!id) return;
        window.location.href = `./decision.html?id=${encodeURIComponent(id)}`;
      });
    });
  }

  window.DeciRepoRepositoryTable = { mount };
})();
