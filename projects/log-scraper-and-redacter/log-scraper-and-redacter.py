import os
import sys
import re

# sys.argv[0] is the script name
# sys.argv[1] is the first thing you type after the script name
if len(sys.argv) < 2:
    print("Usage: python redactor.py <path_to_log>")
    sys.exit(1)

filename = sys.argv[1]  # This takes the path from the terminal command

pattern = re.compile(r"\d{3}-\d{3}-\d{4,}")

with open(filename, "r") as f:  # 'r' -> open for reading (default)
    original_content = f.read()
print("The original content of an file: \n", original_content)
# Syntax: pattern.sub(replacement, original_string)
sanitized_content = pattern.sub("###-###-####", original_content) 

with open("sanitized.log", 'w') as f_out:
    f_out.write(sanitized_content)

print("Redaction completed. Check sanitized.log")



