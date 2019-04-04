import re
import yaml
import pytest

def strip_empty_lines(output):
    lines = []
    for line in output.strip().split('\n'):
        line = line.strip()
        if line:
            lines.append(re.sub(' +', ' ', line.strip()))
    return '\n'.join(lines)


