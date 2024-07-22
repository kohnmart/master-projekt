import inquirer
import os
import re

def list_files_in_directory(directory):
    """List all files in the given directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def list_subdirectories(directory):
    """List all subdirectories in the given directory."""
    return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]


def find_highest_version(files, base_name):
    """Find the highest version of files matching the pattern base_name + version number."""
    # Compile the regex pattern to match the base name followed by a version number at the end
    version_pattern = re.compile(rf"{re.escape(base_name)}(\d+)$")
    highest_version = -1

    for file in files:
        match = version_pattern.search(file)  # Use search to find the pattern anywhere in the file name
        if match:
            version_number = int(match.group(1))
            if version_number > highest_version:
                highest_version = version_number

    return highest_version

def make_choices(path):
    # List files in the stream video directory
    file_choices = list_subdirectories(path)
    
    if not file_choices:
        print("No files found in the directory")
        return

    # Prompt the user to select a file
    file_question = [
        inquirer.List('file_choice',
                      message="Select a file",
                      choices=file_choices)
    ]
    file_answer = inquirer.prompt(file_question)

    # Prompt the user to select a rotation choice
    rotation_question = [
        inquirer.List('rotation_choice',
                      message="Applying 90-wise rotations during classification?",
                      choices=[True, False])
    ]
    rotation_answer = inquirer.prompt(rotation_question)

    decision_tree_question = [
        inquirer.List('tree_choice',
                      message="Decision Tree or Plain use?",
                      choices=[True, False])
    ]
    decision_tree_answer = inquirer.prompt(decision_tree_question)

    # Prompt the user to select a clip model
    clip_model_question = [
        inquirer.List('clip_model_choice',
                      message="Choose clip model",
                      choices=["RN50", "RN101", "RN50x4", "RN50x16", "ViT-B/14", "ViT-B/16", "ViT-B/32"])
    ]
    clip_model_answer = inquirer.prompt(clip_model_question)
    clip = clip_model_answer['clip_model_choice'].replace('/', '-')

    # Prompt the user to enter the sequence entry time start
    seq_entry_question = [
        inquirer.Text('seq_entry_choice', message="Set time start", default="0")
    ]
    seq_entry_answer = inquirer.prompt(seq_entry_question)

    # List files in the output directory
    outputs_list = list_subdirectories('./output')
    concat_output_name = f"{file_answer['file_choice'].split('.')[0]}_{decision_tree_answer['tree_choice']}_{rotation_answer['rotation_choice']}_{clip}_v"

    # Find the highest version of files matching the pattern
    highest_version = find_highest_version(outputs_list, concat_output_name)

    next_version = highest_version + 1 if highest_version != -1 else 0

    concat_output_name = concat_output_name + str(next_version)

    # Prompt the user to enter the output file name
    output_name_question = [
        inquirer.Text('output_name', message="Enter the output file name", default=concat_output_name)
    ]
    output_name_answer = inquirer.prompt(output_name_question)

    return {
        "file": file_answer['file_choice'],
        "rotation": rotation_answer['rotation_choice'],
        "clip": clip_model_answer['clip_model_choice'],
        "concat_name": output_name_answer['output_name'],
        "time_start": seq_entry_answer['seq_entry_choice'],
        "decision_tree": decision_tree_answer['tree_choice']
    }
