## Day 7 Advanced Security Review

| Test Type | Input | Result |
|----------|------|--------|
| Large Payload | Long strings | Passed |
| Special Character Injection | <>[]{};-- | Passed |
| Invalid HTTP Method | GET request | 405 Method Not Allowed |
| Missing Content-Type | No JSON header | 415 Unsupported Media Type |
| Null/Object Abuse | Arrays/null | Passed |

### Key Findings:
- API safely handles malformed requests
- Flask protections validated
- No endpoint crashes detected
- Fallback system ensures stability

### Recommendations:
- Add ESG numeric range validation
- Consider JWT auth for production
- Add centralized logging
- Add schema validation for stronger input controls

## Day 8 Input Validation Enhancements

### Added Protections:
- ESG inputs must be numeric
- ESG values restricted to 0–100
- Invalid strings blocked
- Out-of-range values blocked

### Validation Results:
| Test Type | Result |
|----------|--------|
| Invalid string input | Passed |
| Out-of-range values | Passed |
| Malformed data | Passed |

### Security Improvement:
Strengthened schema validation significantly improves API production readiness.