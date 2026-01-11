#!/bin/bash
# Run this script on Tower (root@Tower) to fix the Maxwell PDF using Paperless container's ocrmypdf

PDF_PATH="/mnt/user/continuum/downloads/2002-ROBERT-MAXWELL-ISRAELS-SUPERSPY-THOMAS.pdf"
OUTPUT_PATH="/mnt/user/continuum/downloads/2002-ROBERT-MAXWELL-ISRAELS-SUPERSPY-THOMAS-FIXED.pdf"

echo "Processing Maxwell PDF with ocrmypdf..."

# Run ocrmypdf in the Paperless container with --skip-text to avoid re-OCRing
docker exec paperless-ngx ocrmypdf \
  --skip-text \
  --output-type pdf \
  --optimize 1 \
  "/usr/src/paperless/consume/2002-ROBERT-MAXWELL-ISRAELS-SUPERSPY-THOMAS.pdf" \
  "/usr/src/paperless/consume/2002-ROBERT-MAXWELL-ISRAELS-SUPERSPY-THOMAS-FIXED.pdf"

if [ $? -eq 0 ]; then
    echo "✓ PDF processed successfully!"
    echo "Output: $OUTPUT_PATH"
else
    echo "✗ Processing failed"
fi
