import shutil
import signal
import subprocess
import time
from pathlib import Path

import requests

BASE_PORT = 7332  # avoid clash with dev server
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKUP_SCRIPT = PROJECT_ROOT / "scripts/backup_data.sh"
RUN_SERVER = PROJECT_ROOT / "scripts/run_mcp_server.py"


def wait_health(port: int, timeout: int = 15) -> bool:
    base = f"http://localhost:{port}"
    for _ in range(timeout):
        try:
            res = requests.get(f"{base}/health", timeout=1)
            if res.status_code == 200 and res.json().get("status") == "ok":
                return True
        except requests.RequestException:
            pass
        time.sleep(1)
    return False


def test_backup_restore_e2e(tmp_path):
    # 1. Start MCP server
    proc = subprocess.Popen(["python", str(RUN_SERVER), "--port", str(BASE_PORT)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        assert wait_health(BASE_PORT), "Server did not become healthy"
        # 2. Run backup script
        subprocess.check_call([str(BACKUP_SCRIPT)], cwd=PROJECT_ROOT)
        backup_dir = PROJECT_ROOT / "backups"
        archives = sorted(backup_dir.glob("project_backup_*.tar.gz*"))
        assert archives, "Backup archive not created"
        archive = archives[-1]

        # 3. Corrupt memory-bank and index
        shutil.rmtree(PROJECT_ROOT / "memory-bank")
        (PROJECT_ROOT / "memory-bank").mkdir()
        index_file = PROJECT_ROOT / "memory-bank/embeddings.faiss"
        if index_file.exists():
            index_file.unlink()

        # 4. Restore
        subprocess.check_call(["tar", "-xzf", str(archive)], cwd=PROJECT_ROOT)

        # 5. Rebuild index
        subprocess.check_call(["python", "scripts/retrieve_context.py", "rebuild"], cwd=PROJECT_ROOT)

        # 6. Health check again
        assert wait_health(BASE_PORT), "Server unhealthy after restore"
    finally:
        proc.send_signal(signal.SIGINT)
        proc.wait(timeout=5) 