import re
import textwrap


def extract_text(docstring: str) -> tuple[str, str, dict[str, str]]:
    docstring = textwrap.dedent(docstring or "").strip()
    lines = docstring.splitlines()

    # Find code block (robust to any indentation, blank lines, and multiple code blocks)
    code_block = ""
    code_block_lines = []
    in_code_block = False
    code_block_indent = None
    for i, line in enumerate(lines):
        if not in_code_block and re.match(r"\..\s*code-block", line.strip(), re.IGNORECASE):
            # Find the first non-blank, indented line after the marker
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == "":
                    continue
                indent = len(lines[j]) - len(lines[j].lstrip())
                if indent > 0:
                    code_block_indent = indent
                    in_code_block = True
                    start = j
                    break
            if in_code_block:
                # Collect all lines with at least this indent (or blank)
                for k in range(start, len(lines)):
                    line_k = lines[k]
                    if line_k.strip() == "":
                        code_block_lines.append("")
                        continue
                    if len(line_k) - len(line_k.lstrip()) >= code_block_indent:
                        code_block_lines.append(line_k[code_block_indent:])
                    else:
                        break
            break
    if code_block_lines:
        # Remove leading/trailing blank lines in code block
        while code_block_lines and code_block_lines[0].strip() == "":
            code_block_lines.pop(0)
        while code_block_lines and code_block_lines[-1].strip() == "":
            code_block_lines.pop()
        code_block = "\n".join(code_block_lines)

    # Extract parameter lines that start with ':param' (allow for type or not)
    parameters = {}
    for line in lines:
        m = re.match(r":param(?:\s+\w+)?\s+(\w+)\s*:\s*(.*)", line.strip())
        if m:
            param_name, param_desc = m.groups()
            parameters[param_name] = param_desc.strip()

    # Build the description by excluding the code block and param lines
    description_lines = []
    in_code_block = False
    for line in lines:
        stripped = line.strip()
        if re.match(r"\..\s*code-block", stripped, re.IGNORECASE):
            in_code_block = True
            continue
        if in_code_block:
            if line.strip() == "":
                continue
            indent = len(line) - len(line.lstrip())
            if indent >= (code_block_indent or 1):
                continue
            in_code_block = False
        if re.match(r":param(?:\s+\w+)?\s+\w+\s*:", stripped):
            continue
        if not in_code_block:
            stripped = stripped.lstrip()
            if stripped:
                description_lines.append(stripped)
    description = "\n\n".join(description_lines).strip()

    return description, code_block, parameters
