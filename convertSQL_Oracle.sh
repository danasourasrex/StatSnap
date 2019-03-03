#!/bin/bash
cd db_upload
sqlite3 chat.db <<EOF
.output dump.txt
.dump
EOF

