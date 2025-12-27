#!/bin/bash

set -e
npm run build

if ! git diff --quiet -- assets/build/main.css; then
  echo "build/main.css has changes. Please commit the updated build file."
  exit 1
fi
