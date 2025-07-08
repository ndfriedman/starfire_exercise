#written by Noah Friedman
#implements the data pull agent, charged with pulling the necessary data from the db

import requests
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel, tool, HfApiModel, PythonInterpreterTool
from huggingface_hub import InferenceClient
from difflib import get_close_matches
import prompt_reference_strs
import ast
import sys


def get_all_distinct_values_for_column(data_key: str, year: str, colName: str) -> str:

	"""Gets all distinct values for a column in a database"""

	medicare_data_dict = prompt_reference_strs.get_val("medicare_data_api_links")
	guid = medicare_data_dict[data_key][year]

	#Build your base URLs
	base_url  = f"https://data.cms.gov/data-api/v1/dataset/{guid}/data"
	stats_url = f"{base_url}/stats"

	#Fetch total row count
	stats_resp = requests.get(stats_url)
	stats_resp.raise_for_status()
	total_rows = stats_resp.json()["total_rows"]

	#Choose a page size (max 5,000 per request) and loop with offset
	size = 5000
	distinct_names = set()

	print("Figuring out unique entries")

	for offset in range(0, total_rows, size):

		resp = requests.get(base_url, params={"size": size, "offset": offset})
		resp.raise_for_status()
		page = resp.json()
		for row in page:
			# add each value (if present) to our set
			if colName in row:
				distinct_names.add(row[colName])
		# when fewer than `size` rows are returned, we’ve hit the end :contentReference[oaicite:1]{index=1}

	return distinct_names


#########HF TOOLS

@tool 
def harmonize_query_with_column_values(data_key: str, year: str, column_name: str, query: str) -> str:
	"""
	This tool looks at the user query and ensures that they are using the proper name to extract data from the db 

	Args:
		data_key: the data set to access.  Options: medicare-part-d-prescribers-by-geography-and-drug, medicare-part-d-prescribers-by-provider, medicare-part-d-prescribers-by-provider-and-drug
		year: the year to access the data set.  Options: 2021, 2022, 2023
		column_name: the name of the column that we are seeking to to harmonize
		query: the value the user is searching for

		returns the columns in the database, must return a string
	"""

	medicare_data_dict = prompt_reference_strs.get_val("medicare_data_api_links")
	guid = medicare_data_dict[data_key][year]

	columnValues = get_all_distinct_values_for_column(data_key, year, column_name)

	candidates = list(columnValues)

	# find the single best fuzzy match for “clyndamycin”
	match = get_close_matches(query, candidates, n=1, cutoff=0.3)

	return match



@tool
def inspect_database_columns(data_key: str, year: str) -> str:
	"""
	This tool returns the columns in the dataframe so the llm knows how to use them for a datapull 

	Args:
		data_key: the data set to access.  Options: medicare-part-d-prescribers-by-geography-and-drug, medicare-part-d-prescribers-by-provider, medicare-part-d-prescribers-by-provider-and-drug
		year: the year to access the data set.  Options: 2021, 2022, 2023

		returns the columns in the database.  Must return a string
	"""

	medicare_data_dict = prompt_reference_strs.get_val("medicare_data_api_links")
	guid = medicare_data_dict[data_key][year]

	resp = requests.get(f"https://data.cms.gov/data-api/v1/dataset/{guid}/data", params={"size":1})
	resp.raise_for_status()
	columns = resp.json()[0].keys()

	return columns

@tool
def medicare_data_query_tool(data_key: str, year: str, filter_params: dict) -> dict:
	"""
	This tool returns medicare data pulled from the cms api to be used for analysis.

	Args:
		data_key: the data set to access.  Options: medicare-part-d-prescribers-by-geography-and-drug, medicare-part-d-prescribers-by-provider, medicare-part-d-prescribers-by-provider-and-drug
		year: the year to access the data set.  Options: 2021, 2022, 2023
		filter_params: a dictionary of columns to filter on and variables to filter on.  Only filter on specifications requested by the user (if any)

	Returns:
		a dict containing the json results from the database
	"""

	params = {}
	for key, value in filter_params.items():
		params[f"filter[{key}]"] = value


	medicare_data_dict = prompt_reference_strs.get_val("medicare_data_api_links")

	guid = medicare_data_dict[data_key][year]
	url  = f"https://data.cms.gov/data-api/v1/dataset/{guid}/data"
	
	resp = requests.get(url, params=params)

	try:
		resp.raise_for_status()
		data = resp.json()

		return data

	except Exception as e:
		return "The request returned an exception, try again"


MAX_STEPS = 30 #the maximum number of steps the agent is allowed to execute
def data_pull_agent(
	user_query: str,
	max_steps: int = MAX_STEPS,   # ← now a keyword‐only parameter
) -> str:

	"""
	Pull the appropriate data from the api endpoint to answer the user query

	Args:
		user_query: the question the user seeks to have answered
		max_steps: the maximum number of steps the agent is allow to use

	Returns:
		A natural‐language summary of the DataFrame’s columns,
		basic statistics, and any notable patterns.
	"""

	save_dir_location = "tmp_llm_workspace/data_pull_workspace"

	# 2) Build a prompt guiding the agent
	prompt = (
		"Here is a user's data pull query:\n\n"
		f"{user_query}\n\n"
		"You will access data by querying from medicare data using cms's medicare api using the medicare_data_query_tool\n"
		"Before pulling, you can inspect the data (columns) by using the inspect_database_columns function"
		"Ensure that all necessary data is pulled\n"
		"The requests you get will always be able to pull data.  If you don't pull data its because your query is malformed, try again\n"
		f"Data should be saved to the directory {save_dir_location}\n"
		"Data itself should be saved as a csv\n"
		"Make sure to distinguish between brand and generic names when creating the parameters for the data pull query.  Only include necessary filter params in your data pull query.\n"
		"Retry the medicare_data_query_tool if it doesn't return an answer\n"
		"Return to the user the following items as a string in python dictionary format:\n"
		"1.data_path: a single path to where the data was stored.\n"
		"2.data_summary: A free text summary of the data pulled including amount of data and number of files etc.\n"
	)

	model = HfApiModel(
		model_id="meta-llama/Llama-3.3-70B-Instruct",
	)

	# 3) Instantiate the agent (with Python code execution enabled)
	agent = CodeAgent(
		tools=[medicare_data_query_tool, inspect_database_columns, harmonize_query_with_column_values, PythonInterpreterTool()],                
		model=model,
		add_base_tools=False,     # includes PythonInterpreterTool for executing code
		additional_authorized_imports=["pandas", "io", "requests", "pathlib", "os", "requests", "posixpath", "json"],
		max_steps=MAX_STEPS,
		executor_kwargs={
		"additional_functions": {
			"open": open
		}}
	)


	# 4) Run the agent on our prompt
	res = agent.run(prompt)

	d = ast.literal_eval(str(res))

	#MAKE SURE THE RESULT RETURNED IS THE CORRECT TYPE
	if not isinstance(d, dict):
		d = dict(str(d))


	return d 




