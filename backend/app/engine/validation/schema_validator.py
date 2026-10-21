import re
from typing import Any, Dict, List, Tuple


class SchemaValidator:
    def parse_array_constraints(self, constraints: List[str]) -> Tuple[int, int, int, int]:
        """
        Extract min_len, max_len, min_val, max_val from constraints list.
        Example: '1 <= nums.length <= 10^5' or '-10^9 <= nums[i] <= 10^9'
        """
        min_len, max_len = 1, 100000
        min_val, max_val = -1000000000, 1000000000

        for c in constraints:
            c_clean = c.replace(" ", "").replace("10^5", "100000").replace("10^4", "10000").replace("10^9", "1000000000")
            # Length pattern: e.g. 1<=nums.length<=100000
            m_len = re.search(r'(\d+)<=[\w\.]*length<=(\d+)', c_clean)
            if m_len:
                min_len = int(m_len.group(1))
                max_len = int(m_len.group(2))

            # Value pattern: e.g. -1000000000<=nums[i]<=1000000000
            m_val = re.search(r'(-?\d+)<=[\w\[\]]*<=(-?\d+)', c_clean)
            if m_val:
                min_val = int(m_val.group(1))
                max_val = int(m_val.group(2))

        return min_len, max_len, min_val, max_val

    def validate_input(
        self,
        structured_input: Dict[str, Any],
        input_schema: List[Dict[str, Any]],
        constraints: List[str]
    ) -> Tuple[bool, List[str]]:
        violations: List[str] = []
        min_len, max_len, min_val, max_val = self.parse_array_constraints(constraints)

        for param in input_schema:
            name = param.get("name")
            p_type = param.get("type", "")
            if not name or name not in structured_input:
                violations.append(f"Missing required parameter '{name}' in input payload.")
                continue

            val = structured_input[name]

            if "[]" in p_type or "array" in p_type:
                if not isinstance(val, list):
                    violations.append(f"Parameter '{name}' must be a list/array.")
                    continue
                # Size check
                if len(val) < min_len:
                    violations.append(f"Array '{name}' length {len(val)} is below minimum constraint {min_len}.")
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

            elif "integer" in p_type or "int" in p_type:
                if not isinstance(val, int) or isinstance(val, bool):
                    violations.append(f"Parameter '{name}' must be an integer.")
                    continue
                if val < min_val or val > max_val:
                    violations.append(f"Integer '{name}'={val} is out of bounds [{min_val}, {max_val}].")

        return len(violations) == 0, violations
