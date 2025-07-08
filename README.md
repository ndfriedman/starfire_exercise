# starfire_exercise
Agentic AI Workflow for Starfire

Usage: streamlit run app.py

versioning: Python 3.9.13

Installation and set up
1. Create a virtual environment: source .venv/bin/activate
2. Huggingface:
 i. huggingface token: https://huggingface.co/settings/tokens
 ii. request access to Meta Llama 3.3: https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct
 iii. once access is granted, export your huggingface token as an environment variable: export HUGGING_FACE_HUB_TOKEN=XXXXXXX
3. Serapi.  Crete a token at https://serpapi.com/, and set it as an environmental variable.  export SERPAPI_API_KEY=XXXXX
4. Install required packages:

pip install smolagents
pip install 'smolagents[transformers]
Pip install openpyxl
pip install markdownify requests
Pip install matplotlib
Pip install langchain
pip install -U langchain-community
pip install google-search-results
pip install serpapi

Notes: 
This program will not work if you have a vpn on; disable it.  Both huggingface and serpapi will stop working if you exhaust your allocation of free tokens.
