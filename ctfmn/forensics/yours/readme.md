```
  - STEP 1:
    - binwalk -e base.txt.gz && cd extractions/base.txt.gz.extracted/0
  - STEP 2:
    - base64 -d -i decompressed.bin | tesseract stdin -
```

