import streamlit as st
import random
import time
import requests
import vertexai
import os
import shutil
from pathlib import Path

import git
import magika
from requests_html import HTMLSession

from vertexai.preview.generative_models import GenerativeModel

PROJECT_ID = os.environ.get('GCP_PROJECT', '-')
LOCATION = os.environ.get('GCP_REGION', '-')

m = magika.Magika()
vertexai.init(project=PROJECT_ID, location=LOCATION)

MODEL_ID = "gemini-1.5-pro-preview-0409" 

model = GenerativeModel(
    MODEL_ID,
    system_instruction=[
        "You are a coding expert.",
        "Your mission is to answer all code related questions with given context and instructions.",
    ],
)

def sendPrompt(input):
    prompt_response = model.generate_content(input,
        generation_config={
            "max_output_tokens": 4096,
            "temperature": 0.4,
            "top_p": 1
        },
    )
    return prompt_response

def get_code_prompt(question):
    """Generates a prompt to a code related question."""

    prompt = f"""
    Questions: {question}

    Context:
    - The entire codebase is provided below.
    - Here is an index of all of the files in the codebase:
      \n\n{code_index}\n\n.
    - Then each of the files is concatenated together. You will find all of the code you need:
      \n\n{code_text}\n\n

    Answer:
  """

    return prompt

sess = HTMLSession()

st.title('Gemini Repo Inspection')

repo_dir = "./repo"

def clone_repo(repo_url, repo_dir):
    """Clone a GitHub repository."""

    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    os.makedirs(repo_dir)
    git.Repo.clone_from(repo_url, repo_dir)
    st.write(f"Repo {repo_url} foi clonado com sucesso!")
    return True


def extract_code(repo_dir):
    """Create an index, extract content of code/text files."""

    code_index = []
    code_text = ""
    for root, _, files in os.walk(repo_dir):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, repo_dir)
            code_index.append(relative_path)

            file_type = m.identify_path(Path(file_path))
            if file_type.output.group in ("text", "code"):
                try:
                    with open(file_path, "r") as f:
                        code_text += f"----- File: {relative_path} -----\n"
                        code_text += f.read()
                        code_text += "\n-------------------------\n"
                except Exception:
                    pass

    return code_index, code_text

repo_url = st.text_input("Cole um repositório para ser analisado:", """https://github.com/GoogleCloudPlatform/microservices-demo""")


if st.button('Clonar repo'):
    repo = clone_repo(repo_url, repo_dir)

    if repo: 
        st.button('Indexar Repo')
        code_index, code_text = extract_code(repo_dir)
        st.write('Repo indexado com sucesso')
    

# code_index, code_text = extract_code(repo_dir)

with st.form('my_repo'):

    prompt = st.selectbox('Selecione um prompt:', [
        'Give me a summary of this codebase, and tell me the top 3 things that I can learn from it.',
        'Provide a getting started guide to onboard new developers to the codebase.',
        'Find the top 3 most severe issues in the codebase.',
        'Find the most severe bug in the codebase that you can provide a code fix for.',
        'Provide a troubleshooting guide to help resolve common issues.' 
    ])
    gerar = st.form_submit_button('Generate')

if gerar:
    st.write(sendPrompt(prompt))