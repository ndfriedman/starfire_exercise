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


#x = llm_query_utils.query_llm("what are the 5 largest metro areas in korea?")
#print(x)


#url = "https://data.cms.gov/data-api/v1/dataset/c8ea3f8e-3a09-4fea-86f2-8902fb4b0920/data"

#url = "https://data.cms.gov/data-api/v1/dataset/7dda2a9d-034a-446a-b4b3-e1254e0127b2/data"

url = "https://data.cms.gov/data-api/v1/dataset/7dda2a9d-034a-446a-b4b3-e1254e0127b2/data"

#params = {'filter[Gnrc_Name]': 'rosuvastatin', 'filter[Prscrbr_Geo_Lvl]': 'State'}
#params = {'filter[Brnd_Name]': 'Zoloft'}
params = {'filter[drug_name]': 'rosuvastatin', 'filter[geography]': 'state'}


resp = requests.get(url, params=params)
try:
	resp.raise_for_status()
	data = resp.json()

	print(len(data))

except Exception as e:
	print(e)