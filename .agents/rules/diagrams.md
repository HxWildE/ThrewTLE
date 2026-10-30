# Diagram & Visualization Rules

1. **In-Chat Direct Rendering (ASCII / Unicode):**
   - In chat responses, always render workflows and architectural paths using clean, high-contrast **ASCII / Unicode box diagrams** (e.g., `┌───┐`, `│`, `└───┘`, `──►`).
   - This ensures diagrams render **visually and directly as graphics** inside the chat panel without displaying as raw code blocks.

2. **Mermaid in Files & Artifacts:**
   - Whenever Mermaid code is generated, place it inside persistent markdown files (`.md`) or Mermaid files (`.mmd`) in `diagrams/` or `learning/`, or in Antigravity Artifacts.
   - This allows the user's installed VS Code Mermaid extension (`bierner.markdown-mermaid`) to render interactive graphical SVG diagrams in the side preview.
