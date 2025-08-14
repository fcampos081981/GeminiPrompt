import os
import sys
import argparse
import google.generativeai as genai

class GeminiService:

    def __init__(self, api_key):

        genai.configure(api_key=api_key)
        self.model = model = genai.GenerativeModel('gemini-1.5-pro')

    def ask_question(self, question):

        try:
            response = self.model.generate_content(question)
            return response.text
        except Exception as e:
            return f"An error occurred: {e}"

def main():

    parser = argparse.ArgumentParser(description="Ask a question to the Gemini API.")
    parser.add_argument("question", type=str, help="The question you want to ask Gemini.")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: The GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)

    gemini_service = GeminiService(api_key)
    answer = gemini_service.ask_question(args.question)
    print(answer)

if __name__ == "__main__":
    main()