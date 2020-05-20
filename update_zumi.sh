#!/bin/bash
# This script will replace the hardcoded offsets.txt file path

# If targeting known path
if sed -i 's+/home/pi/offsets.txt+/offsets.txt+g' ./usr/local/lib/python3.6/site-packages/zumi/zumi.py; then
    echo 'Updated zumi.py'
else
    echo 'Unable to update zumi.py'
fi

# Replacing target path reference in any zumi.py file
# find . -type f \( -name "zumi.py" \) \( -size +3c \
#   -exec grep -q str1 {} \; \
#   -exec sed -i 's+/home/pi/offsets.txt+/offsets.txt+g' {} \; \
#   -printf '"%p" was modified\n' \
#     -o -printf '"%p" was not modified\n"' \)