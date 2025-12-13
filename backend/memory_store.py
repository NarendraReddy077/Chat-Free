import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def get_chat_history(session_id: str) -> List[Dict[str, str]]:
    file = DATA_DIR / f"{session_id}.json"
    if not file.exists():
        return []

    try:
        return json.loads(file.read_text(encoding="utf-8"))
    except Exception:
        # Corrupt file; reset history
        return []


def add_message(session_id: str, role: str, content: str) -> None:
    file = DATA_DIR / f"{session_id}.json"
    history = get_chat_history(session_id)

    history.append(
        {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )

    # Cap history size
    if len(history) > 50:
        history = history[-50:]

    file.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
