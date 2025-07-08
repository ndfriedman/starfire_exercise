#written by Noah Friedman

import llm_query_utils
import data_pull_agent
import data_analysis_agent
import ast


#from langchain.agents import load_tools
#from smolagents import CodeAgent, InferenceClientModel, Tool, HfApiModel


#from huggingface_hub import InferenceClient
#client = InferenceClient(timeout=120)  # wait up to 2 minutes
#result = client.text_generation("Hello world")



import requests
import prompt_reference_strs

data_key = "medicare-part-d-prescribers-by-geography-and-drug"
year = "2023"
medicare_data_dict = prompt_reference_strs.get_val("medicare_data_api_links")
guid = medicare_data_dict[data_key][year]

resp = requests.get(f"https://data.cms.gov/data-api/v1/dataset/{guid}/data", params={"size":1})
resp.raise_for_status()
columns = resp.json()[0].keys()

print(columns)

#x = llm_query_utils.query_llm("what are the 5 largest metro areas in korea?")
#print(x)




