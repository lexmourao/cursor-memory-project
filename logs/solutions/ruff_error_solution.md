# Ruff CI Error Log

**Date:** 2024-06-09

**Error:**
```
error: unrecognized subcommand '.'
Usage: ruff [OPTIONS] <COMMAND>
```

**Context:**
This error occurred during the CI 'Run linters' step when running `ruff .`.

**Root Cause:**
The version of ruff installed in the CI environment does not recognize `.` as a valid subcommand. The correct usage for this version is likely `ruff check .` instead of `ruff .`.

**Rule:**
When running ruff in CI, always verify the correct command syntax for the installed ruff version. If you see "unrecognized subcommand '.'", use `ruff check .` instead of `ruff .`.

**Action:**
Update the CI workflow to use `ruff check .`. 