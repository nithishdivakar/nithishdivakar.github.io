import sys, re
from pathlib import Path

file_path=sys.argv[1]
contents = Path(file_path).read_text()

# matches = re.findall(r'(!.*]\()(.*_files/)',contents)
mod_content = re.sub(r'(!.*]\()(.*_files/)',r'\1/images/\2',contents)
with open(file_path,'w') as F:
    F.write(mod_content)
