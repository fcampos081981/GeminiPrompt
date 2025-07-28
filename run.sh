#!/bin/bash


export GEMINI_API_KEY="AIzaSyDDtdAmjQzWpSeEFZqx4se-hEzlxso34z4"


QUESTION="$1"

if [ -z "$QUESTION" ]; then
    echo "Usage: ./run.sh \"<your question>\""
    exit 1
fi

python3 gemini_prompt.py "$QUESTION"