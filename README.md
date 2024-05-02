# Getting Started Guide 
## This guide will help you get up to speed with the Gemini Repo Inspection 

1. Environment Setup:

Clone the repository: Use git clone https://github.com/duboc/gemini-repo-inspection.git to clone the repository to your local machine.
Install dependencies: Navigate to the project directory and run pip install -r requirements.txt to install the required Python libraries.

Set up environment variables:
```bash 
export GCP_PROJECT="projectid" # Set this to your Google Cloud Platform project ID.
export GCP_REGION="us-central1" # Set this to the region where you want to run the application.
```

2. Codebase Overview:

**gemini-repo.py**: This is the main application file. It handles user input, interacts with the Gemini model, and displays the results.
**utils_streamlit.py**: This file contains helper functions for managing the Streamlit application state.

3. Key Libraries and Tools:

- **Streamlit**: Used for building the web application interface.
- **Vertex AI**: Used for interacting with the Gemini large language model.
- **Magika**: Used for identifying file types.
- **GitPython**: Used for cloning the GitHub repository.

4. Understanding the Workflow:

- The user inputs a GitHub repository URL.
- The application clones the repository and indexes the files.
- The user selects a question to ask about the codebase.
- The application generates a prompt based on the selected question and the codebase.
- The prompt is sent to the Gemini model.
- The model generates a response, which is displayed to the user.

5. Additional Resources:

**Streamlit documentation**: https://docs.streamlit.io/
**Vertex AI documentation**: https://cloud.google.com/vertex-ai/docs
**Magika documentation**: https://github.com/ahupp/python-magic
G**itPython documentation**: https://gitpython.readthedocs.io/

6. Tips:

Use a virtual environment to isolate the project's dependencies.
Familiarize yourself with the Streamlit framework and its capabilities.
