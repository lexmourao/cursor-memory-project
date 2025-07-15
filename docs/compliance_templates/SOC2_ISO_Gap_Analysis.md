# SOC 2 & ISO 27001 Gap Analysis Template

*Project:* Cursor Memory Project  
*Assessment Date:* YYYY-MM-DD  
*Assessor:* __________________

## How to Use
1. Review each control domain row.  
2. Mark **Status** as ✅ Met, ⚠️ Partially Met, or ❌ Not Met.  
3. For gaps, describe remediation actions and assign an owner & target date.  
4. Store the living document in `docs/compliance_records/`.

| Domain / Control (abbrev) | Framework Ref | Current Status | Evidence / Notes | Remediation Action | Owner | Target Date |
|---------------------------|---------------|----------------|------------------|-------------------|-------|-------------|
| Security Policies & Procedures | SOC 2 CC1.0 / ISO 27001 A.5 | ⚠️ | PROJECT_RULES.md covers coding rules; no formal security policy doc | Draft and approve security policy document | Sec Lead | |
| Access Control | CC6.3 / A.9 | ⚠️ | Non-root Docker user & secrets manager implemented | Document role-based access matrix; periodic access review | DevOps | |
| Change Management | CC8.1 | ✅ | Pre-commit, CI pipeline, review process | — | — | — |
| Backup & Recovery | CC3.3 / A.12 | ✅ | Encrypted backups + nightly restore validation | — | — | — |
| Monitoring & Logging | CC7.2 / A.12 | ⚠️ | Prometheus metrics, Slack alerts; no central log retention policy | Add log shipping to SIEM & retention schedule | DevOps | |
| Vendor Management | CC1.4 | ❌ | No documented process for third-party risk | Create vendor risk assessment workflow | Security | |
| Incident Response | CC7.4 / A.16 | ✅ | `INCIDENT_RESPONSE.md` | — | — | — |
| Physical Security | ISO A.11 | N/A | Cloud deployment only | — | — | — |
| Business Continuity | CC4.3 / A.17 | ❌ | No DR plan beyond backups | Draft DR/BCP with RPO/RTO objectives | PM | |
| Privacy (GDPR/LGPD) | CC6.8 / A.18 | ⚠️ | DPIA & LGPD templates exist; deletion CLI | Implement automated data-subject request process | QA | |

---
Add rows as needed.  Update roadmap tasks for each ❌ / ⚠️ item. 