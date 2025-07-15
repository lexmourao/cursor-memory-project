# HIPAA Risk Assessment Template

*Project:* Cursor Memory Project  
*Assessment Date:* YYYY-MM-DD  
*Assessor:* <Name>

> NOTE: The project currently stores **no ePHI**. This assessment is preparatory—complete only if PHI processing is planned.

## 1. ePHI Inventory
| Data Element | Source | Storage Location | Transmission Path | Retention |
|--------------|--------|------------------|-------------------|-----------|
| — | — | — | — | — |

## 2. Threat & Vulnerability Analysis
| Threat/Vulnerability | Likelihood | Impact | Existing Safeguards | Additional Controls |
|----------------------|-----------|--------|---------------------|---------------------|
| Unauthorized access to backups | Low | High | GPG encryption, TLS proxy, non-root container | Off-site key management, SIEM alerts |
| API vendor compromise | Medium | High | Weekly real-API smoke test, vendor monitoring | BAA with vendor, vendor SOC 2 report |

## 3. Security Measures Evaluation (45 CFR §164.308 & §164.312)
| Safeguard | Implemented | Notes |
|-----------|-------------|-------|
| Access control (unique ID, emergency access) | Partial | Basic-auth proxy; no emergency access procedure |
| Audit controls | Partial | Prometheus metrics; need detailed audit logs |
| Integrity controls (hashing) | Not yet | — |
| Transmission security (TLS) | Yes | Nginx TLS proxy |

## 4. Risk Determination
Summarize high residual risks and justify.

## 5. Risk Mitigation Plan
Outline tasks, owners, deadlines to reduce high risks.

## 6. Documentation & Approval
* Security Officer: ______________________  
* Privacy Officer: _______________________  
* CEO / Owner: __________________________

---
Completed assessments go to `docs/compliance_records/`. 