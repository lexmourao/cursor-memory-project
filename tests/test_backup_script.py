import subprocess
import tarfile
from pathlib import Path

def test_backup_creation(tmp_path, monkeypatch):
    """Run backup script and ensure archive created and valid tar."""
    # Work in isolated tmp dir
    proj = tmp_path
    (proj / "memory-bank").mkdir()
    (proj / "logs" / "errors").mkdir(parents=True)
    (proj / "status").mkdir()

    # Create dummy file inside memory-bank
    (proj / "memory-bank" / "dummy.md").write_text("test", encoding="utf-8")

    script = Path(__file__).resolve().parents[1] / "scripts" / "backup_data.sh"
    subprocess.check_call([str(script)], cwd=proj)

    backups = list((proj / "backups").glob("project_backup_*.tar.gz"))
    assert backups, "Backup archive not found"
    archive = backups[0]
    # Verify tar integrity
    with tarfile.open(archive, "r:gz") as tar:
        names = tar.getnames()
        assert any(name.endswith("dummy.md") for name in names) 