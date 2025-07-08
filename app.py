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

#VALIDATION_MODES

ANALYSIS_QUERY_MULTIPLE = True #whether we run the LLM more than once to execute the analysis query and pick the best answer
ANALYSIS_QUERY_N_MULTIPLE = 4 #how many times we run the same LLM over and over again to get a 

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

	col1, colSepLine, col2 = st.columns([4, 1, 4])
	
	with col1: #Step by step

		st.markdown(
    		"<h5 style='text-align: center;'>CO-PILOT MODE: Perform analysis step by step.</h1>",
    		unsafe_allow_html=True
		)
		#DATA PULL STEP

		col1a, col2a = st.columns([4, 1])

		#st.markdown(
		#    app_markdown.vertical_line_element(),
		#    unsafe_allow_html=True
		#)

		user_query_data_pull = col1a.text_input(
			label="",
			placeholder="What data would you like to pull?"
		)

		col2a.write("")  
		col2a.write("")

		if col2a.button("Pull data"):
			with st.spinner("Building directory and running summary…"):
				data_pull_query = llm_query_utils.prepare_data_pull_query(user_query_data_pull)

				st.session_state.data_pull_dict = data_pull_agent.data_pull_agent(data_pull_query)


		#ANALYSIS STEP

		#st.markdown(
		#    app_markdown.vertical_line_element(),
		#    unsafe_allow_html=True
		#)

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

				#TEMP FIXED ANALYSIS
				st.session_state.data_pull_dict = {'data_path': 'tmp_llm_workspace/data_pull_workspace/medicare_part_d_prescribers_prozac_2022.csv', 'data_summary': 'Total data entries: 215\nNumber of unique geographic levels: 61\nTotal claims for Prozac/Fluoxetine: 14108250\nTotal drug cost: $303,222,479.72\nNumber of beneficiaries: 2863432.0'}
				#TEMP TEMP TEMP

				print("this is the data pull dict to be used:", st.session_state.data_pull_dict)

				st.session_state.data_analysis_result = data_analysis_agent.data_analysis_agent(user_analysis_request, st.session_state.data_pull_dict)

				col1b.write(st.session_state.data_analysis_result["free_text_summary"])

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


				#TEMP FIXED INFO!
				userQuery = "tell me which state has the most prozac perscriptions"
				data_pull_dict = {'data_path': 'tmp_llm_workspace/data_pull_workspace/medicare_part_d_prescribers_prozac_2022.csv', 'data_summary': 'Total data entries: 215\nNumber of unique geographic levels: 61\nTotal claims for Prozac/Fluoxetine: 14108250\nTotal drug cost: $303,222,479.72\nNumber of beneficiaries: 2863432.0'}
				st.session_state.plot_paths = data_analysis_agent.plotting_agent(userQuery, "", data_pull_dict)

				#st.session_state.plot_paths = data_analysis_agent.plotting_agent(user_analysis_request, data_pull_dict)
				

				#st.session_state.plot_paths = [
				#	'tmp_llm_workspace/plotting_workspace/prozac_prescriptions_by_state.png',
				#	'tmp_llm_workspace/plotting_workspace/matrix_stuff.png'
				#]

		if "plot_paths" in st.session_state:

			#CAROUSEL TO DISPLAY IMAGES

			#TEMP
			#st.session_state.plot_paths = [x[0] for x in st.session_state.plot_paths]


			# 2. Initialize the index exactly once
			if "idx" not in st.session_state:
				st.session_state.idx = 0

			# 3. Build three columns: prev-button, image, next-button
			prev_col, img_col, next_col = st.columns([1, 8, 1])

			# 4. In the left column, bump the index backward
			prev_col.write("")
			prev_col.write("")
			prev_col.write("")
			prev_col.write("")
			prev_col.write("")
			prev_col.write("")
			prev_col.write("")
			prev_col.write("")
			prev_col.write("")
			prev_col.write("")
			prev_col.write("")
			prev_col.write("")
			prev_col.write("")
			prev_col.write("")
			prev_col.write("")

			if prev_col.button("◀️", key="prev"):
				st.session_state.idx = (st.session_state.idx - 1) % len(st.session_state.plot_paths)

			next_col.write("")
			next_col.write("")
			next_col.write("")
			next_col.write("")
			next_col.write("")
			next_col.write("")
			next_col.write("")
			next_col.write("")
			next_col.write("")
			next_col.write("")
			next_col.write("")
			next_col.write("")
			next_col.write("")
			next_col.write("")
			next_col.write("")
			

			# 5. In the right column, bump the index forward
			if next_col.button("▶️", key="next"):
				st.session_state.idx = (st.session_state.idx + 1) % len(st.session_state.plot_paths)

			# 6. Finally, re-open and render the “current” image in the middle column
			print("the index is:", st.session_state.idx)
			current_img = Image.open(st.session_state.plot_paths[st.session_state.idx][0])
			img_col.image(
				current_img,
				use_column_width=True,
				caption=st.session_state.plot_paths[st.session_state.idx][1]
			)

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