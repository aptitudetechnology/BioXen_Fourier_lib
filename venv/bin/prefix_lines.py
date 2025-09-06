#!/home/chris/BioXen_jcvi_vm_lib/venv/bin/python3

"""
Simple script to add a prefix to every line in a file.
"""

import sys

for line in sys.stdin:
    print(sys.argv[1] + line, end=" ")
