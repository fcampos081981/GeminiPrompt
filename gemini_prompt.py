import os
import sys
import argparse
import google.generativeai as genai

class GeminiService:
    """
    A service class to interact with the Google Gemini API.
    """
    def __init__(self, api_key):
        """
        Initializes the Gemini service with the provided API key.

        Args:
            api_key (str): The Google AI API key.
        """
        genai.configure(api_key=api_key)
        self.model = model = genai.GenerativeModel('gemini-1.5-pro')

    def ask_question(self, question):
        """
        Sends a question to the Gemini model and returns the response.

        Args:
            question (str): The question to ask the model.

        Returns:
            str: The text response from the model.
        """
        try:
            response = self.model.generate_content(question)
            return response.text
        except Exception as e:
            return f"An error occurred: {e}"

def main():
    """
    The main function to parse arguments and run the Gemini service.
    """
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