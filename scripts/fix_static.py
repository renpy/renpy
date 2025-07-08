#!/usr/bin/env python3
"""
Helper script to fix static module names for Python 3.12
"""

import sys
import re

def fix_static_module(input_file: str, output_file: str, module_name: str):
    with open(input_file, 'r') as f:
        content = f.read()

    # Split module name
    parts = module_name.split('.')
    if len(parts) > 1:
        parent_module = '.'.join(parts[:-1])
        parent_module_identifier = parent_module.replace('.', '_')

        # Fix module definitions for Python 3.12
        content = re.sub(
            r'(__pyx_moduledef.*?"){}(".*?)'.format(re.escape(parts[-1])),
            r'\1' + module_name + r'\2',
            content,
            count=1,
            flags=re.DOTALL
        )

        # Fix init function names
        content = re.sub(
            r'^__Pyx_PyMODINIT_FUNC PyInit_',
            f'__Pyx_PyMODINIT_FUNC PyInit_{parent_module_identifier}_',
            content,
            flags=re.MULTILINE
        )

    with open(output_file, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    fix_static_module(sys.argv[1], sys.argv[2], sys.argv[3])
