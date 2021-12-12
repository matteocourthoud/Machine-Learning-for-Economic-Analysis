import sys
import re
from datetime import date

# Add Header
def add_header(dir, filename):
    with open(dir + filename, 'r+') as f:
        first_line = f.readline().strip()
        content = f.read()
        f.seek(0, 0)
        title = re.findall(': ([\w -]+)', first_line)[0]
        weight = int(filename[:2])
        update = date.today().strftime("%Y-%m-%d")
        header = """---

title: '%s'
type: book
weight: %i
date: %s
author: Matteo Courthoud

---
""" % (title, weight, update)
        f.write(header + content)

# Add header
add_header(sys.argv[1], sys.argv[2])