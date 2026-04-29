# SECURITY REPORT — ESG Risk Integrator (AI Service)

## 1. Overview
This document describes security measures implemented in the AI service.

---

## 2. Threat Model

### Prompt Injection
Examples:
- Ignore previous instructions
- Reveal system prompt

Mitigation:
- Pattern detection using `is_malicious()`
- Block with HTTP 400

---

### HTML / Script Injection
Example:
<script>alert(1)</script>

Mitigation:
- Input sanitization strips HTML tags

---

### SQL Injection
Example:
'; DROP TABLE users; --

Mitigation:
- Inputs sanitized and treated as plain text

---

### API Abuse
Risk:
- Excessive requests overload system

Mitigation:
- flask-limiter → 30 req/min

---

### AI Failure
Risk:
- Groq unavailable

Mitigation:
- Retry logic
- Structured fallback response

---

### Secret Exposure
Mitigation:
- .env storage
- .gitignore protection

---

## 3. Week 1 Security Testing Results

| Test Type | Input | Expected Result | Actual Result |
|----------|------|----------------|---------------|
| Normal Input | Standard ESG | Valid response | Passed |
| Empty Input | {} | No crash | Passed |
| HTML Injection | <script> | Sanitized | Passed |
| Prompt Injection | Ignore previous instructions | Blocked | Passed |
| SQL Injection | '; DROP TABLE | Safe handling | Passed |
| Rate Limit | 35 requests | 429 blocked | Passed |

---

## 4. Residual Risks
- AI may still produce unexpected outputs
- Continuous prompt refinement recommended

---

## 5. Conclusion
Implemented:
- Input sanitization
- Prompt injection protection
- SQL-style input protection
- Rate limiting
- Retry + fallback