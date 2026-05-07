# DeciRepo XSS Audit

Date: 2026-04-07
Scope: `/tmp/decirepo-site-clean`
Mirror checked: `/tmp/decirepo-gh-pages`

## Summary

Second-pass review focused on DOM XSS surfaces in the active DeciRepo public site.

The practical XSS risk was concentrated in dynamic pages and shared rendering components that used `innerHTML` with values originating from:

- `URLSearchParams`
- `window.DeciRepoData` records
- fetched JSON payloads under `../api/*.json`

Those dynamic surfaces were hardened with explicit HTML escaping and URL encoding.

Runtime confirmation was also performed with a local Playwright harness that injected HTML and attribute payloads into:

- `assets/data.js`
- fetched decision report JSON endpoints

Result: no payload executed and no injected payload node was created in the DOM across the reviewed dynamic pages.

No active XSS sink was found in the frozen DLX v5 demo surface on disk D during the earlier pass.

Related runtime artifacts:

- `XSS_TEST_MATRIX.md`
- `XSS_TEST_MATRIX.json`

## Fixed Dynamic Surfaces

These files contained active dynamic HTML rendering and were hardened:

- `components/decision-block.js`
  - added shared `escapeHtml(...)`
  - escaped keys and values in rendered rows/grids
- `components/context-nav.js`
  - escaped labels, metadata, hints, and link attributes before interpolation
- `components/repository-table.js`
  - escaped table cell values and `data-id` attributes
- `components/diff-view.js`
  - escaped diff keys, values, and comparison ids
- `components/header.js`
  - hardened shared menu rendering even though current call sites are static
- `pages/decision.html`
  - escaped dynamic values rendered from decision records and fetched JSON reports
  - encoded dynamic ids in generated links
- `pages/lineage.html`
  - escaped dynamic ids, titles, relations, and graph/table content
- `pages/policy-impact.html`
  - escaped row ids, outcomes, and generated `<option>` values/labels

## Dynamic Pages Reviewed

### Safe after hardening

- `pages/decision.html`
- `pages/lineage.html`
- `pages/policy-impact.html`
- `pages/verify.html`
  - relies on escaped `decision-block` output and encoded query links
- `pages/diff.html`
  - relies on escaped `diff-view` output and encoded query links

### Static or effectively static in current usage

- `index.html`
- `pages/index.html`
- `pages/about.html`
- `pages/billing.html`
- `pages/cases.html`
- `pages/disclaimer.html`
- `pages/privacy.html`
- `pages/proof.html`
- `pages/terms.html`

These pages do not currently render attacker-controlled data into HTML templates. Their shared header mount is now also escaped defensively.

## Data Flow Notes

- `assets/data.js` performs verification fetches and exposes local decision data.
- In the current site, data from `assets/data.js` and fetched JSON reports reaches the DOM through the now-hardened rendering paths above.
- No direct unsafe DOM sink was found inside `assets/data.js` itself.

## Residual Risk / Follow-up

- `innerHTML` is still used as a rendering mechanism in several places, but the reviewed dynamic values are now escaped before interpolation.
- This audit did not include browser-driven exploit automation or CSP deployment review.
- Browser-driven exploit automation is now covered for the main dynamic pages through the local Playwright matrix, but CSP and response-header hardening were not reviewed.
- If future code starts passing untrusted URLs into shared nav/header helpers, link scheme validation should be added in addition to HTML escaping.

## Operational Result

- Canonical source updated in `/tmp/decirepo-site-clean`
- Shared/public mirror should match the hardened component set in `/tmp/decirepo-gh-pages`
