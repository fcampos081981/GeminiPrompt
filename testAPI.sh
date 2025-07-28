#!/bin/bash
curl --location 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent' \
--header 'Content-Type: application/json' \
--header 'X-goog-api-key: YOUT_KEY' \
--data '{
    "contents": [
      {
        "parts": [
          {
            "text": "Explain how AI works in a few words"
          }
        ]
      }
    ]
  }'