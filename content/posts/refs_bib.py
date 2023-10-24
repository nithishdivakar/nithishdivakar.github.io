import bibtexparser
import jinja2
import sys
import argparse
import re,json
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="bib file processor for markdown")

# Add arguments
parser.add_argument("--input", type=str, help="")
parser.add_argument("--debug", action="store_true", help="")
parser.add_argument("--silent", action="store_true", help="")
parser.add_argument("--debug_file", type=str, default="CITATIONS.md", help="")
parser.add_argument("--bib_file", type=str, default="bibfile.bib", help="")

# Parse the command-line arguments
args = parser.parse_args()

LIBRARY = bibtexparser.parse_file(args.bib_file)

print(f"Parsed {len(LIBRARY.blocks)} blocks, including: {len(LIBRARY.entries)} entries, {len(LIBRARY.comments)} comments, {len(LIBRARY.strings)} strings, {len(LIBRARY.preambles)} preambles, {len(LIBRARY.failed_blocks)} failed entries", file=sys.stderr)
if LIBRARY.failed_blocks:
  for blk in LIBRARY.failed_blocks:
    print(blk.error, f"at line no {blk.start_line}"  file=sys.stderr)

debug_file_content = """
---
title: Citations
tags : []
date: 1900-01-01T10:21:00+05:30
draft: true
---
# Citations
<reference>

</reference>
"""

environment = jinja2.Environment()
LISTING_STYLE = {
  "article": environment.from_string("""
- [{{key}}]: {{author}} "_{{title}}_" In {{journal}} {{volume}}, ({{year}})
"""),
  "inproceedings": environment.from_string("""
- [{{key}}]: {{author}} "_{{title}}_" In {{booktitle}} pp. {{pages}}, ({{year}})
"""),
  "online": environment.from_string("""
- _[{{key}}]_<br><small>_`{{url}}`_ {{note}}</small>
"""),
}

LINKING_STYLE = {
  "article": environment.from_string("""
[{{key}}]:    <{{url}}>
    "{{author}} \\"{{title}}\\" In {{journal}} {{volume}}, ({{year}})"
"""),
  "inproceedings": environment.from_string("""
[{{key}}]:    <{{url}}>
    "{{author}} \\"{{title}}\\" In {{booktitle}} pp.{{pages}}, ({{year}})"
"""),
  "online": environment.from_string("""
[{{key}}]:    <{{url}}>
    "{{title}}"
"""),
}

def find_entry(key):
  for entry in LIBRARY.entries:
    if entry.key.lower()==key.lower():
      return entry
  return None

def listing_render(entry):
  if entry.entry_type in LISTING_STYLE:
    return LISTING_STYLE[entry.entry_type].render(key=entry.key,**{k:v.value for k,v in entry.fields_dict.items()})
  else:
    print(f"[WARNING]: Entry type {entry.entry_type} not a defined in listing type", file=sys.stderr)
    return None

def linking_render(entry):
  if entry.entry_type in LINKING_STYLE:
    return LINKING_STYLE[entry.entry_type].render(key=entry.key,**{k:v.value for k,v in entry.fields_dict.items()})
  else:
    print(f"[WARNING]: Entry type {entry.entry_type} not a defined in linking type", file=sys.stderr)
    return None

def generate_citations(keys):
  lines = []
  keys = sorted(set(keys))
  entries = []
  for key in keys:
    entry = find_entry(key) 
    if entry:
      entries.append(entry)
    else:
      print(f"[WARNING]: Entry `{key}` not found", file=sys.stderr)

  entries = sorted(entries, key=lambda x:(x.entry_type,x.key))

  lines.append("<small>")
  for itm in entries:
    lines.append(listing_render(itm))

  for itm in entries:
    lines.append(linking_render(itm))

  lines.append("</small>")
  return "\n\n".join(lines)

if args.debug:
  soup = BeautifulSoup(debug_file_content, 'html.parser')
  tag_to_replace = soup.find('reference')
  citations = generate_citations([entry.key for entry in LIBRARY.entries])
  tag_to_replace.string = citations
  if not args.silent:
    print(soup.prettify(formatter=None))
  with open(args.debug_file,"w") as F:
    F.write(soup.prettify(formatter=None))

else:
  with open(args.input,"r") as file:
    contents = file.read()
    FILTER = re.findall(r'\[(.*?)\]', contents)

  FILTER = [f.lower() for f in FILTER]
  print(FILTER, file=sys.stderr)

  citations = generate_citations(FILTER)
  soup = BeautifulSoup(contents, 'html.parser')
  tag_to_replace = soup.find('reference')
  tag_to_replace.string = citations
  if not args.silent:
    print(soup.prettify(formatter=None))
  # [TODO] add a backup time indexed. 
  with open(args.input,"w") as file:
    file.write(soup.prettify(formatter=None))
