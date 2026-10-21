import json
from typing import Any, Dict, List
from app.engine.formatters.base import BaseFormatter


class LeetCodeRawFormatter(BaseFormatter):
    def _format_value(self, val: Any, val_type: str = "") -> str:
        if isinstance(val, str):
            # LeetCode expects string inputs wrapped in double quotes
            # Handle quotes escaping if necessary
            escaped = val.replace('"', '\\"')
            return f'"{escaped}"'
        elif isinstance(val, bool):
            return "true" if val else "false"
        elif isinstance(val, (int, float)):
            return str(val)
        elif isinstance(val, (list, tuple)):
            # Formats list as [1,2,3] without unnecessary spacing
            return json.dumps(val, separators=(',', ':'))
        elif isinstance(val, dict):
            return json.dumps(val, separators=(',', ':'))
        return str(val)

    def format_input(self, structured_input: Dict[str, Any], input_schema: List[Dict[str, Any]]) -> str:
        lines = []
        if input_schema:
            for param in input_schema:
                name = param.get("name")
                p_type = param.get("type", "")
                if name and name in structured_input:
                    val = structured_input[name]
                    lines.append(self._format_value(val, p_type))
                else:
                    # Fallback if name not found directly
                    pass
        else:
            # If no schema defined, format values in dict order
            for val in structured_input.values():
                lines.append(self._format_value(val))

        return "\n".join(lines)

    def format_batch(self, raw_inputs: List[str]) -> str:
        """LeetCode parses consecutive test cases sequentially by parameter count."""
        cleaned = [r.strip() for r in raw_inputs if r.strip()]
        return "\n".join(cleaned)
