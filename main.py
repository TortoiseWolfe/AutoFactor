print("Script started")

from dotenv import load_dotenv
from your_repo.example import example_function
# from test import test_example_function
import glob
import openai
import os
import re
import shutil
import sys
import test

# Load environment variables from the .env file
load_dotenv()

# Load the API key from an environment variable
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing API key. Set the OPENAI_API_KEY environment variable to your API key.")
# Add the following line to print the API key
# print(f"API key: {api_key}")
# Set up the API key
openai.api_key = api_key

def test_openai_api():
    try:
        prompt = "What is the capital of France?"
        response = gpt35_prompt(prompt)
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
    except Exception as e:
        print("An error occurred while calling the OpenAI API:")
        print(e)


# Initialize GPT-3.5 with your API key
def gpt35_prompt(prompt):
    print(f"Executing gpt35_prompt with prompt: {prompt}")  # Add this print statement
    response = openai.Completion.create(
        engine="text-davinci-003",  # Update the engine to GPT-3.5 (Davinci)
        prompt=prompt,
        max_tokens=4090,
        n=1,
        stop=None,
        temperature=0.9,
    )
    # Add this print statement to log the raw JSON response from the GPT-3.5 engine
    print(f"GPT-3.5 raw JSON response:\n{response}\n")

    return response.choices[0].text.strip()
def gpt35_refactor_code(language, code):
    prompt = f"Please refactor the following {language} code:\n\n{code}\n\nRefactored code:"
    response = gpt35_prompt(prompt)
    return response.strip()
def gpt35_summarize_changes(language, original_code, refactored_code):
    prompt = f"Please provide a summary of the changes made to the following {language} code:\n\nOriginal code:\n{original_code}\n\nRefactored code:\n{refactored_code}\n\nSummary of changes:"
    response = gpt35_prompt(prompt)
    return response.strip()

def refactor_code(language, code):
    refactored_code = gpt35_refactor_code(language, code)
    summary = gpt35_summarize_changes(language, code, refactored_code)
    return refactored_code, summary

# def refactor_code(language, code):
#     prompt = f"Please refactor the following {language} code and provide a summary of the changes made:\n\n{code}\n\nRefactored code:\n{{{{code}}}}\n\nSummary of changes:\n{{{{summary}}}}"
#     # ... (rest of the code)
#     response = gpt35_prompt(prompt)
    
#     # Add this print statement to log the raw response from the GPT-3.5 engine
#     print(f"GPT-3.5 response:\n{response}\n")

#     refactored_code_marker = "{{{code}}}\n\n"
#     refactored_code_start = response.find(refactored_code_marker) + len(refactored_code_marker)
#     refactored_code_end = response.find("\n\n", refactored_code_start)
#     summary_start = refactored_code_end + 2

#     refactored_code = response[refactored_code_start:refactored_code_end].strip()
#     summary = response[summary_start:].strip()
    
#     return refactored_code, summary

def get_file_extension(filename):
    return re.search(r'\.(\w+)$', filename).group(1)

def extension_to_language(extension):
    languages_map = {
        "cs": "C#",
        "js": "JavaScript",
        "py": "Python",
        # Add more file extensions and languages as needed
    }
    return languages_map.get(extension.lower())

def process_files():
    # Create a new folder to store the original code
    original_code_folder = "./original_code"
    os.makedirs(original_code_folder, exist_ok=True)

    for file in glob.glob("./your_repo/**/*.*", recursive=True):
        print(f"Processing file: {file}")  # Add this print statement

        extension = get_file_extension(file)
        language = extension_to_language(extension)
        
        if not language:
            print(f"Skipping file with unsupported extension: {file}")  # Add this print statement
            continue

        print(os.listdir("./your_repo"))

        if not os.path.exists(file):
            with open(file, "w") as code_file:
                code_file.write("")

        with open(file, "r") as code_file:
            code = code_file.read()
            print(f"Calling refactor_code with language: {language} and code: {code}")  # Add this print statement
            refactored_code, summary = refactor_code(language, code)

            # Add the following print statement to log the refactored code and summary
            print(f"Refactored code for {file}:\n{refactored_code}\n")
            print(f"Summary of changes for {file}:\n{summary}\n")

            # Copy the original code file to the new folder
            destination_path = os.path.join(original_code_folder, os.path.relpath(file, "./your_repo"))
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            shutil.copy2(file, destination_path)

            # Overwrite the original code file with the refactored code
            with open(file, "w") as code_file:
                code_file.write(refactored_code)

            # Optionally, you can print or save the refactored code and summary of changes.
            print(f"Original code ({language}):\n{code}\n")
            print(f"Refactored code ({language}):\n{refactored_code}\n")
            print(f"Summary of changes ({language}):\n{summary}\n")

if __name__ == "__main__":
    log_directory = "logs"
    os.makedirs(log_directory, exist_ok=True)
    log_file = os.path.join(log_directory, "output.log")

    with open(log_file, "w") as f:
        sys.stdout = f
        sys.stderr = f

        print("Script started")

        # Add the following line to call the test function
        test_openai_api()
        
        # Run the test_example_function
        example_function()

        # Process all files in the repo
        process_files()
