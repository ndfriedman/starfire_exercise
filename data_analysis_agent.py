#written by Noah Friedman
#an agent that performs data analysis

from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel, tool, HfApiModel, PythonInterpreterTool
from langchain.agents import load_tools
from smolagents import CodeAgent, InferenceClientModel, Tool, HfApiModel
import sys
sys.path.append("/Users/nfriedman/Desktop/starfire_exercise")
import llm_query_utils


#This runs the web search agent, implemented via serpapi
def run_web_search_agent(web_search_query_text):
	model = HfApiModel(
		model_id="meta-llama/Llama-3.3-70B-Instruct",
	)

	search_tool = Tool.from_langchain(load_tools(["serpapi"])[0])

	agent = CodeAgent(tools=[search_tool], model=model)

	res = agent.run(web_search_query_text)
	return res

@tool
def web_search_tool(web_search_query_text: str) -> str:

	"""
	This tool searches the internet to get specific information that may be relevant to an analysis.  

	Args:
		web_search_query_text: the question to query the web about		
		returns: a free text summary of the results of the web query.  If the web query contains PHI it will not execute a web search
	"""

	is_phi_prompt = (
						"Assess whether the following text contains PHI\n"
						f"Text:{web_search_query_text}\n"
						"Answer either YES or NO"
					)

	contains_phi = llm_query_utils.query_llm(is_phi_prompt)
	
	if contains_phi == "NO":
		return run_web_search_agent(web_search_query_text)

	else:
		return "sorry, unable to execute web search due to PHI in the query"



MAX_STEPS = 30 #the maximum number of steps the agent is allowed to execute
def data_analysis_agent(
	user_query: str,
	data_pull_dict: dict,
	max_steps: int = MAX_STEPS,   # ← now a keyword‐only parameter
) -> str:

	"""
	Pull the appropriate data from the api endpoint to answer the user query

	Args:
		user_query: the question the user seeks to have answered
		data_pull_dict: a dictionary capturing key information about data from the data pull
		max_steps: the maximum number of steps the agent is allow to use

	Returns:
		A natural‐language summary of the DataFrame’s columns,
		basic statistics, and any notable patterns.
	"""

	data_location = data_pull_dict["data_path"]

	prompt = (
		"Perform data analysis to answer the following user query\n"
		f"{user_query}\n"
		"The data necessary to execute the analysis can be found here:\n"
		f"{data_location}\n"
		"If you need trend information or general reference data you can search the internet for it using the web_search_tool\n"
		"Please perform analyses, and then return a dictionary with the following information:\n" 
		"1. free_text_summary: write a one paragraph summary describing the result of your analyses\n"
		"2. analysis path: path to the results of your analysis\n"
	)

	model = HfApiModel(
		model_id="meta-llama/Llama-3.3-70B-Instruct",
	)

	# 3) Instantiate the agent (with Python code execution enabled)
	agent = CodeAgent(
		tools=[web_search_tool, PythonInterpreterTool()],               
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
	data_analysis_result = agent.run(prompt)

	#MAKE SURE THE RESULT RETURNED IS THE CORRECT TYPE
	if not isinstance(data_analysis_result, dict):
		data_analysis_result = dict(str(data_analysis_result))

	return data_analysis_result


def plotting_agent(user_query: str,
				   user_plot_specifications: str,
				   data_pull_dict: dict,
				   max_steps: int = MAX_STEPS
	) -> str:


	"""
	Pull the appropriate data from the api endpoint to answer the user query

	Args:
		user_query: the question the user seeks to have answered
		user_plot_specifications: extra specifications for the plotting from the user
		data_pull_dict: a dictionary capturing key information about data from the data pull
		max_steps: the maximum number of steps the agent is allow to use

	Returns:
		A python list of paths to the plots the agent has created
	"""

	
	save_dir_location = "tmp_llm_workspace/plotting_workspace"
	data_location = data_pull_dict["data_path"]

	prompt = (
		"Make plots that support the following analysis request:\n"
		f"{user_query}\n"
		"The data necessary to make the plots can be found in the directory specified below.  Consult the description to see what is contained in the directory\n"
		f"{data_location}\n"
		"Examples of plots you can make include comparative line plots, histograms etc\n"
		f"Please save your plots as pngs in the following directory{save_dir_location}\n"
		"Each plot you make should be accompanied by a bullet point description of the key takeaways of the plot\n"
		"Please user matplotlib to make your plots\n"
		f"You must make at 1-5 matplotlib plots and save them to {save_dir_location}\n"
		"Once complete, return a python list of lists.  Each entry in the list should be a path to the plot you created, and a bullet point summary of the key takeaways of the plot\n"
	)

	model = HfApiModel(
		model_id="meta-llama/Llama-3.3-70B-Instruct",
	)

	agent = CodeAgent(
		tools=[PythonInterpreterTool()],               
		model=model,  
		add_base_tools=False,     # includes PythonInterpreterTool for executing code
		additional_authorized_imports=["pandas", "io", "requests", "pathlib", "os", "requests", 
									   "posixpath", "json", "matplotlib.*"],
		max_steps=MAX_STEPS,
		executor_kwargs={
		"additional_functions": {
			"open": open
		}}
	)

	plotting_results = agent.run(prompt)

	if not isinstance(plotting_results, list):
		plotting_results = list(str(plotting_results))

	return plotting_results


