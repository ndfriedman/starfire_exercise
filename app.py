#main streamlit application

import streamlit as st
import sys
import pandas as pd
from PIL import Image

sys.path.append("/Users/nfriedman/Desktop/starfire_exercise")
import data_pull_agent
import data_analysis_agent
import streamlit_app_utils
import llm_query_utils
import agent_execution_utils

# File: app.py

def main():

	st.set_page_config(layout="wide")

	st.markdown(
    "<h1 style='text-align: center;'>Starfire Data Explorer</h1>",
    unsafe_allow_html=True
	)

	st.markdown(
    "<h3 style='text-align: center;'>Explore trends in medical data to guide your business decisions</h1>",
    unsafe_allow_html=True
	)

	#divide the layout into two columns with a separation in between
	col1, colSepLine, col2 = st.columns([4, 1, 4])
	
	with col1: #Step by step

		st.markdown(
    		"<h5 style='text-align: center;'>CO-PILOT MODE: Perform analysis step by step.</h1>",
    		unsafe_allow_html=True
		)
		#DATA PULL STEP

		col1a, col2a = st.columns([4, 1])

		user_query_data_pull = col1a.text_input(
			label="",
			placeholder="What data would you like to pull?"
		)

		col2a.write("")  
		col2a.write("")

		if col2a.button("Pull data"):
			with st.spinner("Pulling data…"):
				data_pull_query = llm_query_utils.prepare_data_pull_query(user_query_data_pull)

				st.session_state.data_pull_dict = data_pull_agent.data_pull_agent(data_pull_query)

		if "data_pull_dict" in st.session_state:
			st.write(st.session_state.data_pull_dict["data_summary"])

		#ANALYSIS STEP

		col1b, col2b = st.columns([4, 1])

		#ALIGN Buttons
		col1b.write("")  
		col2b.write("")
		col2b.write("")
		col2b.write("")

		user_analysis_request = col1b.text_input(
			label="",
			placeholder="What would you like to learn about your data?"
		)

		if col2b.button("Run analysis"):
			with st.spinner("Performing analysis on data..."):

				print("this is the data pull dict to be used:", st.session_state.data_pull_dict)

				st.session_state.data_analysis_result = data_analysis_agent.data_analysis_agent(user_analysis_request, st.session_state.data_pull_dict)

		if "data_analysis_result" in st.session_state:
			st.write(st.session_state.data_analysis_result["free_text_summary"])

		col1c, col2c = st.columns([4, 1])

		col2c.write("")  
		col2c.write("")

		user_analysis_request = col1c.text_input(
			label="",
			placeholder="Optional: Provide details about the plots you would like to make"
		)

		st.write("")
		st.write("")

		if col2c.button("Generate plots"):
			with st.spinner("Generating plots..."):

				st.session_state.plot_paths = data_analysis_agent.plotting_agent(user_analysis_request, "", data_pull_dict)
				
		if "plot_paths" in st.session_state:

			#CAROUSEL TO DISPLAY IMAGES
			streamlit_app_utils.render_carousel(col2c)

	#full analysis mode
	with col2:

		st.markdown(
    		"<h5 style='text-align: center;'>AUTONOMOUS MODE:\nDelegate your analysis to our AI agent.</h1>",
    		unsafe_allow_html=True
		)

		fullAnalysisModeA, fullAnalysisModeB = st.columns([4, 1])
		st.session_state.user_query_full = fullAnalysisModeA.text_input(
			label="",
			placeholder="Provide a detailed description of the analysis you'd like to perform."
		)

		fullAnalysisModeA.write("")
		fullAnalysisModeA.write("")
		fullAnalysisModeA.write("")
		fullAnalysisModeA.write("")
		fullAnalysisModeA.write("")
		fullAnalysisModeA.write("")
		fullAnalysisModeA.write("")

		fullAnalysisModeB.write("")
		fullAnalysisModeB.write("")

		if fullAnalysisModeB.button("Run Query"):
			agent_execution_utils.execute_full_analysis_pipeline(st.session_state.user_query_full, col2)

if __name__ == "__main__":
	main()


	