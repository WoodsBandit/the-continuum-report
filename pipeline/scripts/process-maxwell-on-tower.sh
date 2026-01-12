#!/bin/bash
#
# Run this script on Tower (as root) to process the Maxwell PDF
# using the Paperless container's ocrmypdf tool
#
# Usage: ./process-maxwell-on-tower.sh
#

SOURCE="/mnt/user/continuum/downloads/2002-ROBERT-MAXWELL-ISRAELS-SUPERSPY-THOMAS.pdf"
OUTPUT="/mnt/user/continuum/downloads/2002-ROBERT-MAXWELL-ISRAELS-SUPERSPY-THOMAS-OCR.pdf"

echo "=== Maxwell PDF Processing Script ==="
echo "Source: $SOURCE"
echo "Output: $OUTPUT"
echo ""

# Check if source exists
if [ ! -f "$SOURCE" ]; then
    echo "ERROR: Source file not found!"
    exit 1
fi

# Copy to Paperless container's working directory
echo "Copying file to Paperless container..."
docker cp "$SOURCE" paperless-ngx:/tmp/maxwell-input.pdf

# Run ocrmypdf inside the container with various repair options
echo "Running ocrmypdf with repair options..."
docker exec paperless-ngx ocrmypdf \
    --skip-text \
    --output-type pdf \
    --pdf-renderer hocr \
    --optimize 0 \
    --force-ocr \
    /tmp/maxwell-input.pdf \
    /tmp/maxwell-output.pdf 2>&1

if [ $? -eq 0 ]; then
    echo "OCR processing succeeded!"
    docker cp paperless-ngx:/tmp/maxwell-output.pdf "$OUTPUT"
    echo "Output saved to: $OUTPUT"
    
    # Clean up
    docker exec paperless-ngx rm -f /tmp/maxwell-input.pdf /tmp/maxwell-output.pdf
    
    echo ""
    echo "Now upload to Paperless with:"
    echo "  curl -X POST 'http://192.168.1.139:8040/api/documents/post_document/' \\"
    echo "    -H 'Authorization: Token da99fe6aa0b8d021689126cf72b91986abbbd283' \\"
    echo "    -F 'document=@$OUTPUT' \\"
    echo "    -F 'title=Robert Maxwell, Israels Superspy - Gordon Thomas'"
else
    echo "ERROR: OCR processing failed!"
    
    # Try alternative approach - just copy through gs
    echo ""
    echo "Trying Ghostscript repair..."
    docker exec paperless-ngx gs \
        -sDEVICE=pdfwrite \
        -dCompatibilityLevel=1.4 \
        -dNOPAUSE \
        -dBATCH \
        -dSAFER \
        -sOutputFile=/tmp/maxwell-output.pdf \
        /tmp/maxwell-input.pdf 2>&1
    
    if [ $? -eq 0 ]; then
        echo "Ghostscript repair succeeded!"
        docker cp paperless-ngx:/tmp/maxwell-output.pdf "$OUTPUT"
        echo "Output saved to: $OUTPUT"
    else
        echo "Ghostscript also failed. The PDF may be corrupted or encrypted."
    fi
    
    docker exec paperless-ngx rm -f /tmp/maxwell-input.pdf /tmp/maxwell-output.pdf
fi
