# AutoFactor

## GPT-3.5 Code Refactor

This repository contains a Python application that uses GPT-3.5, an AI language model by OpenAI, to automatically refactor code in a given repository. The application processes code files in various languages, refactors them using the GPT-3.5 API, and saves the refactored code along with a summary of the changes.

## Prerequisites

- Docker
- Docker Compose
- An OpenAI API key

## Setup

1. Clone the repository:

``` bash
git clone https://github.com/TortoiseWolfe/AutoFactor
cd AutoFactor
```

2. Create a `.env` file in the root directory of the project and add your OpenAI API key:

``` bash
OPENAI_API_KEY=your_actual_api_key_here
```

Replace `your_actual_api_key_here` with your actual API key.

## Usage

1. Copy the code you want to refactor into the `your_repo` directory.

2. Build the Docker container:

``` bash
docker-compose build
```

3. Run the container:

```bsh
docker-compose up -d
```

4. The refactored code will replace the original code in the `your_repo` directory. The original code will be backed up in the `original_code` directory.

5. Check the logs for the summary of changes:

```bash
cat your_repo/logs/output.log
```

## Customization

To add support for more languages, update the extension_to_language function in the main.py file with the desired file extension and language name.

```python
def extension_to_language(extension):
    languages_map = {
        "cs": "C#",
        "js": "JavaScript",
        "py": "Python",
        # Add more file extensions and languages as needed
    }
    return languages_map.get(extension.lower())
```

## License

This project is open source under the MIT License. See the LICENSE file for details.
