"""Hash computation for plan proposals.

Origin: S08 agent/gateway.py plan_hash
"""

import hashlib
import json


def compute_plan_hash(op: str, path_args: dict | None = None, target=None) -> str:
    """Return the first 12 hex-characters of the SHA-256 of the plan payload.

    The payload is a JSON object with:
      - ``op``: the operation string.
      - ``path``: a dict mapping path segments to values (empty dict for creates).
      - ``target``: the target dict to operate on.

    For ``*_destroy`` ops the path includes ``{"id": <target_id>}``.
    For ``*_create`` ops the path is an empty dict.

    Returns the first 12 hex characters of the SHA-256 digest.
    """
    if path_args is None:
        path_args = {}

    payload = {
        "op": op,
        "path": path_args,
        "target": target,
    }

    json_str = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha256(json_str.encode("utf-8")).hexdigest()
    return digest[:12]
