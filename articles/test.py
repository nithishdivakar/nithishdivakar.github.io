import sys
from TexSoup import TexSoup,TexNode
from time import gmtime, strftime

F = open(sys.argv[1], 'r')
soup = TexSoup(F.readlines())

def section(node,name):
  S.append("\n## {}\n".format(node.args[0]))
  return True


def subsection(node,name):
  S.append("\n### {}\n".format(node.args[0]))
  return True


def subsubsection(node,name):
  S.append("\n#### {}\n".format(node.args[0]))
  return True

def math_env(node,name):
  S.append("\n<div>\n") 
  S.append("$$\n") 
  S.append("\\begin{aligned}\n")
  for element in node.contents:
    _walk(element)
  S.append("\\end{aligned}\n")
  S.append("$$\n") 
  S.append("\n</div>\n") 
 
  return True

def math_inline(node,name):
  string = str(node)[1:-1]
  tmpl = '''<span>\\\\({}\\\\)</span>'''.format(string)
  S.append(tmpl)

  return True

def textbf(node,name):
  S.append('''<span class="font-weight-bold">{}</span>'''.format(node.args[0].strip()))
  return True

def textit(node,name):
  S.append('''<span class="font-italic">{}</span>'''.format(node.args[0].strip()))
  return True

def emph(node,name):
  S.append("<emph>{}</emph>".format(node.args[0].strip()))
  return True

def center(node,name):
  S.append("\n<center>\n") 
  for element in node.contents:
    _walk(element)
  S.append("\n</center>\n")
  return True

def quote(node,name):
  
  #S.append('''<blockquote class="blockquote">\n''')
  S.append('''<p class="p-3 mb-2 bg-light">''')

  for element in node.contents:
    _walk(element)

  S.append('''</p>''')
  #S.append('''</blockquote>\n''')

  return True

def skip_continue(node,name):
  print(name)
  return False

def skip(node,name):
  return True



LUT = {
  'section':section,
  'section_star':section,
  'subsection':subsection,
  'subsection_star':subsection,
  'subsubsection':subsection,
  'subsubsection_star':subsection,
  'textbf':textbf,
  'textit':textit,
  'emph':emph,
  '$$': math_env,
  '$' :math_inline,
  'align_star':math_env,
  'center':center,
  'quote':quote,
  'document':skip_continue,
}

S = []
print(soup.find('title').args[0])
_title = soup.find('title').args[0]
print(_title)
_date = strftime("%Y-%m-%d %H:%M +05:30", gmtime())


header = '''---
layout: post
title: {title}
date: {date}
comments: true
---

'''.format(
  title= ('Not available' if len(_title)==0 else _title),
  date = _date
)
S.append(header)

def _walk(node):
  if isinstance(node, TexNode):
    name = node.name.replace('*', '_star')
    # print("F", name)
    if name in LUT:
      skip_children = LUT[name](node,name)
    else: 
      skip_children = skip(node,name)
    
    if not skip_children:
      for element in node.contents:
        _walk(element)

  elif isinstance(node, str):
    string = str(node).strip()
    if not string[0] == '%': # not a comment
      S.append(str(node))
    
_walk(soup.find('document'))

with open(sys.argv[2], 'w') as G:
  for s in S:
    G.write(s)
