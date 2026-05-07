#!/usr/bin/env bash
set -e

pip install -r requirements.txt
npm install
npm run build
flask db upgrade