# Data Protection Impact Assessment (DPIA) Template

*Project:* Cursor Memory Project  
*Assessment Date:* YYYY-MM-DD  
*Assessor:* <Name>

## 1. Describe Processing
| Question | Answer |
|----------|--------|
| Nature of processing | Continuous summarisation, embedding, and storage of project documentation. |
| Purpose | Provide long-term memory/context to Cursor IDE. |
| Data subjects | Developers, researchers (no personal data expected). |
| Data categories | Technical documentation; **no PII/PHI**. |
| Storage location | Local bind volumes; encrypted backups; GitHub artifact. |

## 2. Necessity & Proportionality
1. Explain why this processing is necessary for project goals.
2. Consider less intrusive alternatives.

## 3. Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Unauthorised access to backups | Low | Medium | GPG encryption, least-priv access, 30-day retention |
| Accidental personal data upload | Med | Medium | Pre-commit secret scan; Data-deletion CLI |

## 4. Consultation & Approval
* Data Protection Officer: ___________________
* Stakeholder Sign-off: ______________________

---
Attach final DPIA to `docs/compliance_records/`. 