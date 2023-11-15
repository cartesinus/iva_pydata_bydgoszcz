#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for generating and executing Python code using OpenAI's GPT model.

This CLI tool prompts users for a command, uses OpenAI's GPT model to generate corresponding Python
code, and offers the option to execute the generated code. It includes functions to execute code
and read file contents. The script loops to allow continuous interaction, with an option to exit.

Before running the script, ensure that a .env file is present with the OpenAI API key specified
like this:
OPENAI_API_KEY="your key here"

Usage:
Run the script, enter commands at the prompt, review the generated code, and choose to execute.
Type 'exit' to quit the script.
"""

import sys
import click
from openai import OpenAI
from dotenv import load_dotenv
from iva_calendar import *

load_dotenv()

def execute_python_code(code):
    """
    Executes given Python code using exec().

    Parameters:
    code (str): Python code to execute.

    Does not return anything; handles and displays exceptions.
    """
    try:
        exec(code)
    except Exception as e:
        click.echo(f"Error executing code: {e}")


def read_file_content(file_path):
    """
    Reads and returns the content of a specified file.

    Parameters:
    file_path (str): Path to the file to read.

    Returns:
    Content of the file as a string, or None if the file is not found.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        click.echo(f"Error: File {file_path} not found.")
        return None


def extract_code(gpt_response):
    """
    Extracts Python code from a GPT response enclosed within markdown code blocks.

    Parameters:
    gpt_response (str): The GPT response string containing the code block.

    Returns:
    str: The extracted Python code, or an empty string if no code block is found.
    """
    if '```python' in gpt_response and '```' in gpt_response:
        # Splitting at the start of the code block and taking the second part
        code_start = gpt_response.split('```python', 1)[1]
        # Splitting at the end of the code block and taking the first part
        code = code_start.split('```', 1)[0]
        return code.strip()
    else:
        return ""


@click.command()
def query_gpt():
    """
    This script continuously asks for commands to send to GPT, then generates and optionally
        executes Python code based on the responses.
    Enter 'exit' to stop the script.
    """
    iva_calendar_code = read_file_content('iva_calendar.py')
    if iva_calendar_code is None:
        click.echo("Exiting due to file read error.")
        sys.exit(1)

    while True:
        prompt = click.prompt("Please enter your command or type 'exit' to quit")

        if prompt.lower() == 'exit':
            click.echo("Exiting the script.")
            break

        client = OpenAI()
        prompt = (
            f"Convert the following command to code: '{prompt}', "
            "and available functions are:\n"
            f"{iva_calendar_code}."
        )
        response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[{"role": "system", "content": "Generate Python code for the following task:"},
                    {"role": "user", "content": prompt}]
        )

        generated_code = response.choices[0].message.content
        extracted_code = extract_code(generated_code)

        click.echo("Generated Python Code:")
        click.echo(extracted_code)

        if click.confirm('Do you want to execute this code?'):
            execute_python_code(extracted_code)
        else:
            click.echo("Execution cancelled.")

if __name__ == '__main__':
    query_gpt()
