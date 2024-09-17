import os

def read_client_record(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Creating a new file with default content.")
        default_content = """
# Client Record

## Client Information
**Name:** Sophia Feng

## Suggestions
_No suggestions yet._
"""
        with open(file_path, "w") as file:
            file.write(default_content)
        return default_content

    with open(file_path, "r") as file:
        return file.read()

def write_client_record(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)

def format_client_record(client_info, suggestions):
    record = "# Client Record\n\n## Client Information\n"
    for key, value in client_info.items():
        record += f"**{key}:** {value}\n"
    
    record += "\n## Suggestions\n"
    for key, value in suggestions.items():
        record += f"- **{key}:** {value}\n"
    
    return record

def parse_client_record(markdown_content):
    client_info = {}
    suggestions = {}
    
    current_section = None
    lines = markdown_content.split("\n")
    
    for line in lines:
        line = line.strip()  # Strip leading/trailing whitespace
        if line.startswith("## "):
            current_section = line[3:].strip()
        elif current_section == "Client Information" and line.startswith("**"):
            if ":** " in line:
                key, value = line.split(":** ", 1)
                key = key.strip("**").strip()
                value = value.strip()
                client_info[key] = value
        elif current_section == "Suggestions" and line.startswith("- **"):
            if ":** " in line:
                key, value = line.split(":** ", 1)
                key = key.strip("- **").strip()
                value = value.strip()
                suggestions[key] = value
    
    final_record = {
        "Client Information": client_info,
        "Suggestions": suggestions
    }
    print(f"Final parsed record: {final_record}")
    return final_record