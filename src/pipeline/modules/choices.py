import inquirer
import os
import re

def list_files_in_directory(directory):
    """List all files in the given directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def find_highest_version(files, base_name):
    """Find the highest version of files matching the pattern base_name + version number."""
    version_pattern = re.compile(rf"{re.escape(base_name)}(\d+)$")
    highest_version = -1

    for file in files:
        match = version_pattern.search(file)
        if match:
            version_number = int(match.group(1))
            if version_number > highest_version:
                highest_version = version_number

    return highest_version

def make_choices():
    # Define the choices for file selection
    file_choices = list_files_in_directory('./stream_video')
    
    if not file_choices:
        print("No files found in the directory: ./stream_video")
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
                      choices=['True', 'False'])
    ]
    rotation_answer = inquirer.prompt(rotation_question)

    # Prompt the user to select a clip model
    clip_model_question = [
        inquirer.List('clip_model_choice',
                      message="Choose clip model",
                      choices=["RN50", "RN101", "RN50x4", "RN50x16", "ViT-B/14", "ViT-B/16", "ViT-B/32"])
    ]
    clip_model_answer = inquirer.prompt(clip_model_question)
    clip = clip_model_answer['clip_model_choice'].replace('/', '-')


    seq_entry_question = [
        inquirer.Text('seq_entry_choice', message="Set time start")
    ]
    seq_entry_answer = inquirer.prompt(seq_entry_question)


    ### CONFIG OUTPUT NAME AND VERSIONING ####

    outputs_list = list_files_in_directory('./output')
    concat_output_name = f"{file_answer['file_choice'].split('.')[0]}_{rotation_answer['rotation_choice']}_{clip}_v"

    highest_version = find_highest_version(outputs_list, concat_output_name)
    next_version = highest_version + 1 if highest_version is not None else 0

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
        "time_start": seq_entry_answer['seq_entry_choice']
    }

