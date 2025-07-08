#written by Noah Friedman
#code that runs LLM prompts, retries them, and ensures they work

#executes an agent with retry if it fails
#this is a recursive function

import llm_query_utils
import data_pull_agent
import data_analysis_agent
import os
import csv
import streamlit as st
import streamlit_app_utils


#Ensures that at least one non-empty csv is present in the target directory
def ensure_non_empty_csv_is_present(directory_path):
	for fname in os.listdir(directory_path):
		if not fname.lower().endswith('.csv'):
			continue

		full_path = os.path.join(directory_path, fname)
		with open(full_path, newline='', encoding='utf-8') as f:
			reader = csv.reader(f)
			# Count rows as you go, but stop as soon as you hit 2
			count = 0
			for _ in reader:
				count += 1
				if count > 1:
					# Found a CSV with more than one row
					return True
	return False

	
#Runs a series of QC checks on data pull agent.  If it fails returns false
def execute_data_pull_agent_with_qc_and_retry(data_pull_query, n_retries_current, n_retries_max=5):
	
	print("Executing Data Pull Agent With Retry", n_retries_current)
	
	if n_retries_current > n_retries_max:
		print("Could not execute data pull agent, max retries exceeded")
		return "Could not execute data pull agent, max retries exceeded"

	try:
		data_pull_dict = data_pull_agent.data_pull_agent(data_pull_query)
		print("this is the data pull dict", data_pull_dict)

		#Checks 
		if not os.path.exists(str(data_pull_dict["data_path"])):
			print("data_pull_query failed due to non_existent data")
			return execute_data_pull_agent_with_qc_and_retry(data_pull_query, n_retries_current + 1, n_retries_max)
		print("Passed data directory exists check")

		if not ensure_non_empty_csv_is_present(str(data_pull_dict["data_path"])):
			print("data_pull_query failed due to non_existent csvs")
			return execute_data_pull_agent_with_qc_and_retry(data_pull_query, n_retries_current + 1, n_retries_max)
		print("Passed non empty csv check")

		print("Data Sucessfully Pulled")
		return data_pull_dict

	except Exception as e:
		#raise(e)

		print("data_pull_query failed due to exception: ", e)
		if n_retries_current < n_retries_max:
			return execute_data_pull_agent_with_qc_and_retry(data_pull_query, n_retries_current + 1, n_retries_max)

#TODO write the data analysis agent retry / execution logic
def execute_analysis_agent_with_qc_and_retry(user_analysis_request, data_pull_dict, n_retries_current, n_retries_max=5):
	print("Executing Analysis Agent With Retry", n_retries_current)
	
	if n_retries_current > n_retries_max:
		print("Could not execute data pull agent, max retries exceeded")
		return "Could not execute data pull agent, max retries exceeded"

	try:
		data_analysis_result = data_analysis_agent.data_analysis_agent(user_analysis_request, data_pull_dict)

		print("this is the data analysis result", data_analysis_result)
		return data_analysis_result

	except Exception as e:
		print("data_pull_query failed due to exception: ", e)
		if n_retries_current < n_retries_max:
			return execute_analysis_agent_with_qc_and_retry(user_analysis_request, data_pull_dict, n_retries_current + 1, 5)


def execute_full_analysis_pipeline(full_user_task, streamlitWriteColumn, breakupQueries=False):

	subtasks = []
	if breakupQueries:
		subtasks = llm_query_utils.break_up_complex_query_into_subqueries(full_user_task)
	else:
		subtasks = [full_user_task]

	print("the analysis subtasks are: ", subtasks)

	st.session_state.analysis_results = []
	for subtask in subtasks:
		print("working on subtask: ", subtask)

		with st.spinner("Pulling relevant data..."):
			data_pull_query = llm_query_utils.prepare_data_pull_query(subtask)
			st.session_state.data_pull_dict = execute_data_pull_agent_with_qc_and_retry(data_pull_query, 1, 5)

		with st.spinner("Performing data analysis..."):
			streamlitWriteColumn.write("DATA HAS BEEN PULLED.  SUMMARY: " + st.session_state.data_pull_dict["data_summary"])
			data_analysis_result = execute_analysis_agent_with_qc_and_retry(subtask, st.session_state.data_pull_dict, 1, 5)
			streamlitWriteColumn.write("ANALYSIS HAS BEEN COMPLETED:" + data_analysis_result["free_text_summary"])
			st.session_state.analysis_results.append(data_analysis_result["free_text_summary"])
		
		with st.spinner("Making analysis plots..."):
			streamlitWriteColumn.write("ANALYSIS PLOTS:")
			st.session_state.plot_paths = data_analysis_agent.plotting_agent(subtask, "", st.session_state.data_pull_dict)
			streamlit_app_utils.render_carousel(streamlitWriteColumn)

	finalAnswer = ""
	if len(st.session_state.analysis_results) > 0:
		finalAnswer = llm_query_utils.integrate_answers_into_final_answer(full_user_task, st.session_state.analysis_results)
	streamlitWriteColumn.write("FINAL ANSWER: " + finalAnswer)
	
	return 0
	

