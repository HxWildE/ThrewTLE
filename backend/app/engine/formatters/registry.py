from app.engine.formatters.base import BaseFormatter
from app.engine.formatters.leetcode_raw import LeetCodeRawFormatter

_DEFAULT_FORMATTER = LeetCodeRawFormatter()

_FORMATTERS: dict[str, BaseFormatter] = {
    "leetcode_raw": _DEFAULT_FORMATTER,
}


def get_formatter(format_name: str = "leetcode_raw") -> BaseFormatter:
    return _FORMATTERS.get(format_name, _DEFAULT_FORMATTER)
