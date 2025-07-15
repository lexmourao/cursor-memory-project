# Release Checklist

> Use this checklist before tagging a new version or deploying to production.

## Code & Tests
- [ ] All unit, integration, and performance tests passing in CI (green)
- [ ] Coverage ≥ 85% gate satisfied
- [ ] `ruff`, `black`, `mypy`, `bandit` show no errors

## Documentation
- [ ] Update `CHANGELOG.md` with new features / fixes
- [ ] Bump version string in `README.md` (if applicable)
- [ ] Verify `docs/` and checklists reflect new changes

## Memory & Data Integrity
- [ ] Run `make summarize` and `make rebuild` to ensure memory-bank is current
- [ ] Run `scripts/backup_data.sh` and verify archive integrity (`tar -tzf`)
- [ ] Validate MCP `/memory` endpoint returns expected record count

## Security
- [ ] Secret scan (TruffleHog) shows no new leaks
- [ ] Review `docs/SECURITY.md` for any required updates

## Deployment
- [ ] Systemd service file version bumped if script path changed
- [ ] Nightly backup cron confirmed active on prod host
- [ ] Health-check monitoring dashboard green

## Sign-off
- [ ] Product owner approval
- [ ] QA lead approval
- [ ] DevOps lead approval

---

*After all items are checked, tag the release:*
```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z" && git push --tags
``` 