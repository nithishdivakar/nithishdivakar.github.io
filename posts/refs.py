import re,json
from collections import Counter
import sys
import argparse
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(description="My Script Description")

# Add arguments
parser.add_argument("--input", type=str, help="Description for arg1")
parser.add_argument("--debug", action="store_true", help="")
parser.add_argument("--debug_file", type=str, default="/Users/nd/WORK/daxpy/content/posts/CITATIONS.md", help="")



# Parse the command-line arguments
args = parser.parse_args()

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


db = []

def injest_paper(lines):
    T = dict(enumerate(lines))
    return {
        "type" : T.get(0,"paper"),
        "ref_key" : T[1],
        "ref_title" : T.get(2,""),
        "ref_cite" : T.get(3,""),
        "ref_url" : T.get(4,"")
    }

def injest_link(lines):
    T = dict(enumerate(lines))
    return {
        "type" : T.get(0,"link"),
        "ref_key" : T[1],
        "ref_url" : T.get(2,"")
    }

def injest_article(lines):
    T = dict(enumerate(lines))
    return {
        "type" : T.get(0,"article"),
        "ref_key" : T[1],
        "ref_title" : T.get(2,""),
        "ref_url" : T.get(3,""),
        "ref_authors" : T.get(4,"")
    }
    
def injest_video(lines):
    T = dict(enumerate(lines))
    return {
        "type" : T.get(0,"video"),
        "ref_key" : T[1],
        "ref_title" : T.get(2,""),
        "ref_url" : T.get(3,"")
    }
    

with open("cite_db.txt","r") as F:
    items = F.read().split("==end==")
    for itm in items:
        lines = [l.strip() for l in itm.split("\n") if len(l.strip())>1]
        if len(lines)==0: continue

        if lines[0] == "paper":
            db.append(injest_paper(lines))
        elif lines[0] == "article":
            db.append(injest_article(lines))
        elif lines[0] == "link":
            db.append(injest_link(lines))
        elif lines[0] == "video":
            db.append(injest_video(lines))

SORT_ORDER = ["paper","article","link","video"]

db.sort(key=lambda k: (SORT_ORDER.index(k["type"]),k["ref_key"]))

# Sanity Check same ref key
counter = Counter(k["ref_url"] for k in db)
keys_greater_than_1 = [key for key, value in counter.items() if value > 1]
if keys_greater_than_1:
    print("Following items in db has same ref keys",file=sys.stderr)
    for key in keys_greater_than_1:
        print(key, file=sys.stderr)

# Sanity Check same url
counter = Counter(k["ref_key"] for k in db)
keys_greater_than_1 = [key for key, value in counter.items() if value > 1]
if keys_greater_than_1:
    print("Following items in db has same urls",file=sys.stderr)
    for key in keys_greater_than_1:
        print(key, file=sys.stderr)

def paper_citation_style(itm):
    # ref_cite2 = itm["ref_cite"].replace(itm["ref_title"],f"_[{itm['ref_title']}][{itm['ref_key']}]_")
    ref_cite2 = itm["ref_cite"].replace(itm["ref_title"],f"_{itm['ref_title']}_")
    return """- [{ref_key}]: {ref_cite2}""".format(ref_cite2=ref_cite2,**itm)

def article_citation_style(itm):
    # return """- _[{ref_title}][{ref_key}]_ by {ref_authors}""".format(**itm)

    return """- _[{ref_title}][{ref_key}]_ by {ref_authors}<br><small>_`{ref_url}`_</small>""".format(**itm)

def link_citation_style(itm):
    return """- _[{ref_key}]_<br><small>_`{ref_url}`_</small>""".format(**itm)

def video_citation_style(itm):
    return """- _[{ref_title}][{ref_key}]_""".format(**itm)

def paper_ref_style(itm):
    ref_cite2= itm["ref_cite"].replace('"', '\\"')
    return """[{ref_key}]:    <{ref_url}>
    "{ref_cite2}"
    """.format(ref_cite2 = ref_cite2, **itm)

def article_ref_style(itm):
    return """[{ref_key}]:    <{ref_url}>
    "{ref_title} by {ref_authors}"
    """.format(**itm)

def link_ref_style(itm):
    return """[{ref_key}]:    <{ref_url}>
        "{ref_key}"
    """.format(**itm)

def video_ref_style(itm):
    return """[{ref_key}]:    <{ref_url}>
        "{ref_title}"
    """.format(**itm)

def generate_citations(db):
    lines = []
    lines.append("<small>")
    for itm in db:
        if itm["type"]=="paper":
            lines.append(paper_citation_style(itm))
        elif itm["type"] == "article":
            lines.append(article_citation_style(itm))
        elif itm["type"] == "link":
            lines.append(link_citation_style(itm))
        elif itm["type"] == "video":
            lines.append(video_citation_style(itm))
    
    for itm in db:
        if itm["type"] == "paper":
            lines.append(paper_ref_style(itm))
        elif itm["type"] == "article":
            lines.append(article_ref_style(itm))
        elif itm["type"] == "link":
            lines.append(link_ref_style(itm))
        elif itm["type"] == "video":
            lines.append(video_ref_style(itm))
    lines.append("</small>")
    return "\n\n".join(lines)

if args.debug:
    db_filtered = db
else:
    with open(args.input,"r") as file:
        contents = file.read()
        FILTER = re.findall(r'\[(.*?)\]', contents)
    FILTER = [f.lower() for f in FILTER]
    if FILTER:
        db_filtered = [item for item in db if item["ref_key"].lower() in FILTER]
    else: 
        db_filtered = db





if args.debug:
    FILTER = []
    soup = BeautifulSoup(debug_file_content, 'html.parser')
    tag_to_replace = soup.find('reference')
    citations = generate_citations(db)
    tag_to_replace.string = citations
    print(soup.prettify(formatter=None))
    with open(args.debug_file,"w") as F:
        F.write(soup.prettify(formatter=None))

else:
    with open(args.input,"r") as file:
        contents = file.read()
        FILTER = re.findall(r'\[(.*?)\]', contents)

    FILTER = [f.lower() for f in FILTER]
    print(FILTER,file=sys.stderr)
    if FILTER:
        db = [item for item in db if item["ref_key"].lower() in FILTER]

    citations = generate_citations(db)
    soup = BeautifulSoup(contents, 'html.parser')
    tag_to_replace = soup.find('reference')
    tag_to_replace.string = citations
    print(soup.prettify(formatter=None))
    # [TODO] add a backup time indexed. 
    with open(args.input,"w") as file:
        file.write(soup.prettify(formatter=None))

# for itm in db:
#     print("{type}\n{ref_key}\n{ref_title}\n{ref_cite}\n{ref_url}\n==end==\n".format(**itm))



