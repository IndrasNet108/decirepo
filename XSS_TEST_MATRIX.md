# XSS Test Matrix

Date: 2026-04-07
Base URL: http://127.0.0.1:8123
Payload HTML: `<img data-xss-payload="1" src="x" onerror="window.__xss.push('HTML_PAYLOAD')">`
Payload attribute: `DR-XSS" data-xss-attr="1" onclick="window.__xss.push('ATTR_PAYLOAD')`

| Page | Verdict | XSS fired | Payload nodes | Escaped literal present |
| --- | --- | --- | --- | --- |
| decision | PASS | no | 0 | yes |
| lineage | PASS | no | 0 | yes |
| policy-impact | PASS | no | 0 | no |
| verify | PASS | no | 0 | yes |
| diff | PASS | no | 0 | yes |

## Notes

- `PASS` means no injected payload executed and no injected payload node was created in the DOM.
- `escaped_literal_present = yes` means the payload survived only as escaped text, which is acceptable for this test.
- Decision-page report endpoints were route-mocked to inject payloads into fetched JSON.
