import re
from time import gmtime, strftime
import os
import base64
import sys

F = open(sys.argv[1], 'r').readlines()
O = open(sys.argv[2], 'w')


_title = re.findall(r"title{(.+?)}",''.join(F),re.MULTILINE)
_date = strftime("%Y-%m-%d %H:%M +05:30", gmtime())


header = '''---
layout: post
title: {title}
date: {date}
comments: true
---

'''.format(
  title= ('Not available' if len(_title)==0 else _title[0]),
  date = _date
  )


# print(m)
# print(''.join(F)[:1000])


O.write(header)
SEC = re.compile('\\\\section{(.*)}')

def handle_image(m):
  full_match = m.group(0)
  directory = m.group(1)
  file_path = m.group(2)
  type_handle = m.group(3)
  cmd       = m.group(4)
  out_file  = m.group(5)
  print(directory ,file_path ,type_handle, cmd )
  os.system(cmd)
  print(cmd,out_file)
  with open(directory+out_file,'rb') as f:
    encoded = base64.b64encode(f.read())
    encoded = encoded.decode('utf8')
    ss = '''<img src="data:image/png;base64,{}">'''.format(encoded)
  return ss

IGNORES = [
  r"^\\begin{document}.*",
  r"^\\end{document}.*",
  r"^\\documentclass.*$",
  r"^%.*$",
  r"^\\usepackage.*$",
  r"^\\maketitle.*",
  r"^\\title{.*}",
  r"^\\author{.*}",
  r"^\\date{.*}",
  r"^\\maketitle",
  r"^\\tableofcontents",
]

RULES = [
 (r"\\section{(.+?)}",r"\n# \1\n"),
 (r"\\subsection{(.+?)}",r"\n## \1\n"),
 (r"([ ,.])\$(.*?)\$([ ,.'])", r"\1<span>\\\\(\2\\\\)</span>\3"),
 (r"\\textbf{(.+?)}",r" <b>\1</b> "),
 (r"\\textit{ *(.+?) *}",r"<i>\1</i>"),
 (r"\\begin{verbatim}",r"\n```python"),
 (r"\\end{verbatim}",r"```\n" ),
 (r"\\%",r"%"),
 (r"\$\$ *\\begin{aligned}",r"<div> $$ \\begin{aligned}"),
 (r"\\end{aligned} *\$\$",r"\\end{aligned} $$ </div>"),
 (r"\\begin{center}",r"\n<center>\n"),
 (r"\\end{center}",r"\n</center>\n"),
 (r"\\import{(.+?)}{(.+?)} %%TYPE:(.+?) CMD:(.+?) OUT:(.+?)$",handle_image),
 (r"\\href{(.*?)}{(.*?)}",r"[\2](\1) "),
]
RULES = [(ign,r"") for ign in IGNORES] + RULES


print(SEC)
for inp_line in F:
  inp_line = inp_line[:-1]
  for match,action in RULES:
    inp_line = re.sub(match,action,inp_line)

  # if len(inp_line)!=0:
  O.write(inp_line)
  O.write('\n')
    # print(inp_line)
    # print(m)
  # if m:
  #   # print(m)
  #   print(m.group(1))

O.close()
