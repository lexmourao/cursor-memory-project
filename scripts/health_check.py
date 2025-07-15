import sys
import requests

def main():
    base_url = "http://localhost:7331"
    try:
        h = requests.get(f"{base_url}/health", timeout=5)
        m = requests.get(f"{base_url}/memory", timeout=10)
    except requests.RequestException as exc:
        print(f"[health_check] Request failed: {exc}")
        sys.exit(1)
    if h.status_code != 200 or h.json().get("status") != "ok":
        print("[health_check] /health endpoint unhealthy")
        sys.exit(1)
    mem_count = len(m.json().get("memory", []))
    if mem_count == 0:
        print("[health_check] memory list empty")
        sys.exit(1)
    print(f"[health_check] OK – {mem_count} memory records served")

if __name__ == "__main__":
    main() 