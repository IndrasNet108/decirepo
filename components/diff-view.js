(function () {
  function changed(left, right) {
    return String(left) !== String(right);
  }

  function row(key, leftValue, rightValue) {
    const glow = changed(leftValue, rightValue) ? "changed" : "";
    return `
      <div class="diff-row ${glow}">
        <div class="diff-key">${key}</div>
        <div class="diff-left">${leftValue}</div>
        <div class="diff-arrow">→</div>
        <div class="diff-right">${rightValue}</div>
      </div>
    `;
  }

  function mount(targetId, left, right) {
    const root = document.getElementById(targetId);
    if (!root || !left || !right) return;

    root.innerHTML = `
      <section class="panel diff-panel">
        <div class="diff-head-grid">
          <div class="diff-head-card">
            <div>${left.canonical_id || left.id}</div>
            <div class="diff-head-sub">${left.id}</div>
          </div>
          <div class="diff-head-card">
            <div>${right.canonical_id || right.id}</div>
            <div class="diff-head-sub">${right.id}</div>
          </div>
        </div>

        <div class="diff-section">
          <h3 class="section-title">Input</h3>
          ${row("emergency_condition", left.input.emergency_condition, right.input.emergency_condition)}
          ${row("exception_requested", left.input.exception_requested, right.input.exception_requested)}
          ${row("estimated_amount", left.input.estimated_amount, right.input.estimated_amount)}
          ${row("risk_score", left.input.risk_score, right.input.risk_score)}
        </div>

        <div class="diff-section">
          <h3 class="section-title">Policy</h3>
          ${row("policy_version", left.policyVersion, right.policyVersion)}
          ${row("exception_rule", left.policyContext.exception_rule, right.policyContext.exception_rule)}
        </div>

        <div class="diff-section">
          <h3 class="section-title">Outcome</h3>
          ${row("decision", left.outcomeFields.decision, right.outcomeFields.decision)}
          ${row("reason_code", left.outcomeFields.reason_code, right.outcomeFields.reason_code)}
        </div>
      </section>
    `;
  }

  window.DeciRepoDiffView = { mount };
})();
