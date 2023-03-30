from dotenv import load_dotenv
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

# Set up the API key
openai.api_key = api_key

# Initialize GPT-3.5 with your API key
def gpt35_prompt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",  # Update the engine to GPT-3.5 (Davinci)
        prompt=prompt,
        max_tokens=4150,
        n=1,
        stop=None,
        temperature=0.2,
    )

    return response.choices[0].text.strip()

def refactor_code(language, code):
    prompt = f"Refactor the following {language} code:\n\n{code}\n\nRefactored code:\n{{{{code}}}}\n\nSummary of changes:"
    response = gpt35_prompt(prompt)
    
    refactored_code_marker = "{{{code}}}\n\n"
    refactored_code_start = response.find(refactored_code_marker) + len(refactored_code_marker)
    refactored_code_end = response.find("\n\n", refactored_code_start)
    summary_start = refactored_code_end + 2

    refactored_code = response[refactored_code_start:refactored_code_end].strip()
    summary = response[summary_start:].strip()
    
    return refactored_code, summary

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
        extension = get_file_extension(file)
        language = extension_to_language(extension)
        
        if not language:
            continue

        with open(file, "r") as code_file:
            code = code_file.read()
            refactored_code, summary = refactor_code(language, code)

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

# Process all files in the repo
process_files()

if __name__ == "__main__":
    log_directory = "/app/your_repo/logs"
    os.makedirs(log_directory, exist_ok=True)
    log_file = os.path.join(log_directory, "output.log")

    with open(log_file, "w") as f:
        sys.stdout = f
        sys.stderr = f

        # Run the test_example_function
        test.test_example_function()

        # Process all files in the repo
        # process_files()