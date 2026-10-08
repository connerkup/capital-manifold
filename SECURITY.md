# Security Policy

## Supported Versions

The Capital Manifold project maintains security updates for the following release lines:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

---

## Reporting a Vulnerability

The Capital Manifold maintainers take the integrity and confidentiality of macro-financial infrastructure software with the utmost gravity. If you discover a security vulnerability or exploit vector within Capital Manifold, please do **NOT** open a public GitHub issue.

Instead, please report your findings responsibly via one of the following channels:

* **Primary Security Contact:** Conner Kupferberg
* **Encrypted Security Email:** `security@capitalmanifold.org` or `conner@capitalmanifold.org`
* **Subject Format:** `[SECURITY DISCLOSURE] Capital Manifold - <Component>`

### What to Include

To facilitate rapid triage and mitigation, please provide:
1. **Description:** A detailed explanation of the vulnerability and its potential systemic or infrastructure impact.
2. **Component Affected:** Specific module, CLI subcommand, REST API endpoint, or DuckDB ingestion pipeline.
3. **Reproduction Steps:** Minimal proof-of-concept (PoC) script, HTTP request, or sample malformed payload.
4. **Environment:** Python version, OS architecture, DuckDB version, and commit hash.
5. **Mitigation:** Any proposed patches or temporary workarounds, if available.

---

## Response & Disclosure Timeline

| Phase | Target SLA |
| ----- | ---------- |
| **Initial Acknowledgement** | Within 48 hours |
| **Triage & Risk Assessment** | Within 5 business days |
| **Fix Development & Testing** | Within 14 to 30 days (depending on severity) |
| **Public Release & CVE Assignment** | Coordinated with reporter upon fix deployment |

---

## Scope & Threat Model

### In Scope
* **Injection & Storage Vulnerabilities:** SQL injection vectors against DuckDB storage engines or malformed Parquet ingestion exploits.
* **REST API & Web Vulnerabilities:** Remote code execution, privilege escalation, cross-site scripting (XSS), or denial-of-service (DoS) against the FastAPI / Uvicorn server (`/api/*`).
* **Deserialization & Parser Vulnerabilities:** Unsafe JSON/XBRL/SDMX deserialization in statutory harvesters (`harvesters/*`).
* **Algorithmic Integrity Breaches:** Undetected systemic bypasses in double-entry conservation invariants or unauthorized state manipulation in the Procedural Graph Engine bridge.

### Out of Scope
* Disagreements with macro-financial theory, economic modeling conventions, or statutory reporting standards.
* Downtime or API schema shifts from external statutory data dissemination endpoints (ECB SDMX, Banque de France, US Treasury DTS, NY Fed, SEC EDGAR).
* Attacks requiring physical access to the host machine or non-standard local execution environments without user privileges.

---

## Responsible Disclosure & Bug Bounty

We are committed to coordinated, responsible disclosure. If you act in good faith and allow us reasonable time to remediate before public disclosure, the project maintainers commit to:
* Not initiating legal action against researchers acting within scope.
* Publicly crediting your discovery in release notes and security advisories (unless you request anonymity).
