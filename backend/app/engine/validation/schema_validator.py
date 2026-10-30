import re
from typing import Any, Dict, List, Tuple


def safe_eval_bound(expr: str, default: int) -> int:
    try:
        expr_clean = expr.replace(" ", "").replace("^", "**")
        # Ensure only allowed characters for safety
        if not re.match(r'^[0-9\+\-\*\/\(\)]+$', expr_clean):
            return default
        return int(eval(expr_clean, {"__builtins__": {}}, {}))
    except Exception:
        return default


class SchemaValidator:
    def parse_array_constraints(self, constraints: List[str]) -> Tuple[int, int, int, int]:
        """
        Extract min_len, max_len, min_val, max_val from constraints list.
        Example: '1 <= nums.length <= 10^5' or '-10^9 <= nums[i] <= 10^9'
        """
        min_len, max_len = 1, 100000
        min_val, max_val = -1000000000, 1000000000

        for c in constraints:
            c_clean = c.replace(" ", "")
            # Length pattern: e.g. 1<=nums.length<=100000
            m_len = re.search(r'(-?[\d\*\^\+\-]+)<=[\w\.]*length<=(-?[\d\*\^\+\-]+)', c_clean)
            if m_len:
                min_len = safe_eval_bound(m_len.group(1), min_len)
                max_len = safe_eval_bound(m_len.group(2), max_len)

            # Value pattern: e.g. -1000000000<=nums[i]<=1000000000
            m_val = re.search(r'(-?[\d\*\^\+\-]+)<=[\w\[\]]*<=(-?[\d\*\^\+\-]+)', c_clean)
            if m_val:
                min_val = safe_eval_bound(m_val.group(1), min_val)
                max_val = safe_eval_bound(m_val.group(2), max_val)

        return min_len, max_len, min_val, max_val

    def parse_param_constraints(self, constraints: List[str], input_schema: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
        """
        Extract constraints specifically matched to each parameter in input_schema.
        """
        result = {}
        for param in input_schema:
            name = param.get("name", "")
            p_type = param.get("type", "integer")

            is_arr = "[]" in p_type or "array" in p_type
            is_str = "string" in p_type

            # Default bounds
            min_len = 1
            max_len = 100000 if (is_arr or is_str) else 1
            min_val = -1000000000
            max_val = 1000000000

            for c in constraints:
                c_clean = c.replace(" ", "")

                # Check array/string length for this parameter: e.g. 1<=coins.length<=12 or s.length<=10^5
                m_len = re.search(r'(-?[\d\*\^\+\-]+)<=[\w\.]*' + re.escape(name) + r'[\w\.]*length<=(-?[\d\*\^\+\-]+)', c_clean, re.I)
                if not m_len and len(input_schema) == 1 and (is_arr or is_str):
                    m_len = re.search(r'(-?[\d\*\^\+\-]+)<=[\w\.]*length<=(-?[\d\*\^\+\-]+)', c_clean, re.I)
                if m_len:
                    min_len = safe_eval_bound(m_len.group(1), min_len)
                    max_len = safe_eval_bound(m_len.group(2), max_len)

                # Check element bounds for array: e.g. 1<=coins[i]<=2^31-1
                if is_arr:
                    m_elem = re.search(r'(-?[\d\*\^\+\-]+)<=' + re.escape(name) + r'\[i\]<=(-?[\d\*\^\+\-]+)', c_clean, re.I)
                    if not m_elem and len(input_schema) == 1:
                        m_elem = re.search(r'(-?[\d\*\^\+\-]+)<=[\w\[\]]*<=(-?[\d\*\^\+\-]+)', c_clean, re.I)
                    if m_elem:
                        min_val = safe_eval_bound(m_elem.group(1), min_val)
                        max_val = safe_eval_bound(m_elem.group(2), max_val)

                # Check scalar bounds: e.g. 0<=amount<=10^4 or -10^9<=target<=10^9
                if not is_arr and not is_str:
                    m_val = re.search(r'(-?[\d\*\^\+\-]+)<=' + re.escape(name) + r'<=(-?[\d\*\^\+\-]+)', c_clean, re.I)
                    if m_val:
                        min_val = safe_eval_bound(m_val.group(1), min_val)
                        max_val = safe_eval_bound(m_val.group(2), max_val)

            result[name] = {
                "min_len": min_len,
                "max_len": max_len,
                "min_val": min_val,
                "max_val": max_val
            }
        return result

    def validate_input(
        self,
        structured_input: Dict[str, Any],
        input_schema: List[Dict[str, Any]],
        constraints: List[str]
    ) -> Tuple[bool, List[str]]:
        violations: List[str] = []
        param_bounds = self.parse_param_constraints(constraints, input_schema)

        for param in input_schema:
            name = param.get("name")
            p_type = param.get("type", "")
            if not name or name not in structured_input:
                violations.append(f"Missing required parameter '{name}' in input payload.")
                continue

            val = structured_input[name]
            bounds = param_bounds.get(name, {
                "min_len": 1,
                "max_len": 100000,
                "min_val": -1000000000,
                "max_val": 1000000000
            })
            min_len, max_len = bounds["min_len"], bounds["max_len"]
            min_val, max_val = bounds["min_val"], bounds["max_val"]

            if "[]" in p_type or "array" in p_type:
                if not isinstance(val, list):
                    violations.append(f"Parameter '{name}' must be a list/array.")
                    continue
                # Size check
                if len(val) < min_len:
                    violations.append(f"Array '{name}' length {len(val)} is below minimum constraint {min_len}.")
                elif len(val) > max_len:
                    violations.append(f"Array '{name}' length {len(val)} exceeds maximum constraint {max_len}.")
                # Numeric element bound check
                for i, elem in enumerate(val):
                    if isinstance(elem, (int, float)):
                        if elem < min_val or elem > max_val:
                            violations.append(f"Element {name}[{i}]={elem} exceeds constraint bounds [{min_val}, {max_val}].")
                            break  # Avoid spamming

            elif "string" in p_type:
                if not isinstance(val, str):
                    violations.append(f"Parameter '{name}' must be a string.")
                    continue
                if len(val) < min_len:
                    violations.append(f"String '{name}' length {len(val)} is below minimum constraint {min_len}.")
                elif len(val) > max_len:
                    violations.append(f"String '{name}' length {len(val)} exceeds maximum constraint {max_len}.")

            elif "integer" in p_type or "int" in p_type:
                if not isinstance(val, int) or isinstance(val, bool):
                    violations.append(f"Parameter '{name}' must be an integer.")
                    continue
                if val < min_val or val > max_val:
                    violations.append(f"Integer '{name}'={val} is out of bounds [{min_val}, {max_val}].")

        return len(violations) == 0, violations

