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
    def infer_input_schema(metadata: Dict[str, Any], description: str, constraints: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        schema = []
        constraints = constraints or []

        # Infer from description Input: line first
        input_match = re.search(r'Input:\s*([^\n]+)', description)
        if input_match:
            params_str = input_match.group(1)
            tokens = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(\[.*?\]|"(?:\\.|[^"\\])*"|\'.*?\'|[^,]+)', params_str)
            for name, val_str in tokens:
                val_str = val_str.strip()
                has_arr_c = any(f"{name}.length" in c or f"{name}[i]" in c for c in constraints)
                has_mat_c = any(f"{name}[i][j]" in c or f"{name}[row][col]" in c for c in constraints)

                if val_str.startswith("[[") or has_mat_c:
                    p_type = "integer[][]"
                elif val_str.startswith("["):
                    if '"' in val_str or "'" in val_str:
                        p_type = "string[]"
                    else:
                        p_type = "integer[]"
                elif val_str.startswith('"') or val_str.startswith("'"):
                    p_type = "string"
                elif val_str.lower() in ["true", "false"]:
                    p_type = "boolean"
                elif has_arr_c:
                    p_type = "string[]" if name in ["words", "strs"] else "integer[]"
                elif f"integer array {name}" in description.lower() or f"array {name}" in description.lower():
                    p_type = "integer[]"
                elif f"string {name}" in description.lower():
                    p_type = "string"
                else:
                    p_type = "integer"
                schema.append({"name": name, "type": p_type})

        # Check canonical_parameter_names in metadata if no schema extracted
        if not schema and isinstance(metadata, dict) and "canonical_parameter_names" in metadata:
            for name in metadata["canonical_parameter_names"]:
                has_arr_c = any(f"{name}.length" in c or f"{name}[i]" in c for c in constraints)
                if has_arr_c or "num" in name or "arr" in name or name.endswith("s"):
                    p_type = "string[]" if name in ["words", "strs"] else "integer[]"
                elif name in ["s", "str", "word"]:
                    p_type = "string"
                else:
                    p_type = "integer"
                schema.append({"name": name, "type": p_type})

        if not schema:
            schema = [{"name": "nums", "type": "integer[]"}]
        return schema

    @staticmethod
    def extract_example_cases(description: str) -> List[Dict[str, Any]]:
        import json
        blocks = re.findall(r'Example\s+\d+:?\s*(.*?)(?=Example\s+\d+:?|Constraints?:?|$)', description, re.DOTALL | re.IGNORECASE)
        examples = []
        for i, b in enumerate(blocks, 1):
            inp_m = re.search(r'Input:\s*([^\n]+)', b)
            out_m = re.search(r'Output:\s*([^\n]+)', b)
            exp_m = re.search(r'Explanation:\s*([^\n]+)', b)
            if inp_m:
                params_str = inp_m.group(1).strip()
                tokens = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(\[.*?\]|"(?:\\.|[^"\\])*"|\'.*?\'|[^,]+)', params_str)
                struct = {}
                for name, val_str in tokens:
                    val_str = val_str.strip()
                    try:
                        struct[name] = json.loads(val_str)
                    except Exception:
                        if val_str.lower() == "true":
                            struct[name] = True
                        elif val_str.lower() == "false":
                            struct[name] = False
                        elif val_str.isdigit() or (val_str.startswith("-") and val_str[1:].isdigit()):
                            struct[name] = int(val_str)
                        else:
                            struct[name] = val_str.strip("\"'")
                if struct:
                    out_val = out_m.group(1).strip() if out_m else None
                    exp_val = exp_m.group(1).strip() if exp_m else f"Standard LeetCode example {i}."
                    examples.append({
                        "category": "basic",
                        "structured_input": struct,
                        "expected_output": out_val,
                        "explanation": exp_val
                    })
        return examples

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
