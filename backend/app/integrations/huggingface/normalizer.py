import re
from typing import Any, Dict, List, Optional
from app.core.security import sanitize_input_string


class HuggingFaceNormalizer:
    @staticmethod
    def extract_constraints(description: str) -> List[str]:
        constraints = []
        if not description:
            return constraints

        c_match = re.search(r'Constraints?:?(.*?)(?:Follow-up|Example|$)', description, re.DOTALL | re.IGNORECASE)
        section = c_match.group(1) if c_match else description

        lines = section.split("\n")
        for line in lines:
            line = re.sub(r'<[^>]+>', '', line).strip()
            line = line.lstrip("*-•").strip()
            if any(op in line for op in ["<=", ">=", "<", ">"]) or "consists of" in line.lower() or "length" in line.lower():
                cleaned = sanitize_input_string(line)
                if len(cleaned) > 3 and cleaned not in constraints:
                    constraints.append(cleaned)

        return constraints

    @staticmethod
    def infer_input_schema(metadata: Dict[str, Any], description: str) -> List[Dict[str, Any]]:
        schema = []
        # Check canonical_parameter_names in metadata first
        if isinstance(metadata, dict) and "canonical_parameter_names" in metadata:
            for name in metadata["canonical_parameter_names"]:
                p_type = "integer[]" if "num" in name or "arr" in name else ("string" if name in ["s", "str", "word"] else "integer")
                schema.append({"name": name, "type": p_type})
            return schema

        # Infer from description
        input_match = re.search(r'Input:\s*([^\n]+)', description)
        if input_match:
            params_str = input_match.group(1)
            assignments = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=', params_str)
            for name in assignments:
                p_type = "integer[]" if "num" in name or "arr" in name else ("string" if name in ["s", "str"] else "integer")
                schema.append({"name": name, "type": p_type})

        if not schema:
            schema = [{"name": "nums", "type": "integer[]"}]
        return schema

    @classmethod
    def normalize_row(cls, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Already normalized fixture format
        if "slug" in row and "title" in row and "source_id" in row:
            return row

        q_id = row.get("question_id") or row.get("id") or row.get("frontend_question_id")
        slug = row.get("task_id") or row.get("title_slug") or row.get("slug")
        title = row.get("question_title") or row.get("title")
        desc = row.get("problem_description") or row.get("content") or ""
        diff = str(row.get("difficulty") or "EASY").upper()
        meta = row.get("metadata") or {}

        if slug and not title:
            # e.g. "two-sum" -> "Two Sum"
            title = " ".join(word.capitalize() for word in slug.split("-"))

        if not q_id or not slug or not title:
            return None

        constraints = cls.extract_constraints(desc)
        schema = cls.infer_input_schema(meta, desc)

        return {
            "source": "leetcode",
            "source_id": int(q_id),
            "slug": slug,
            "title": title,
            "difficulty": diff if diff in ["EASY", "MEDIUM", "HARD"] else "MEDIUM",
            "content": sanitize_input_string(desc),
            "constraints": constraints,
            "input_schema": schema,
            "support_status": "SUPPORTED" if "[]" in str(schema) or "string" in str(schema) else "PARTIAL"
        }
