#written by Noah Friedman

import llm_query_utils
import agent_execution_utils
from collections import Counter
import time
import os
import shutil

#evaluates the accuracy of the data pull agent
#currently accuracy is defined as pulling non-empty csvs
def evaluate_data_pull_agent(full_user_task):

	start = time.perf_counter()

	is_correct = "NO"

	try:
		data_pull_query = llm_query_utils.prepare_data_pull_query(full_user_task)
		data_pull_dict = agent_execution_utils.execute_data_pull_agent_with_qc_and_retry(data_pull_query, 1, 1)
		
		if not os.path.exists("/Users/nfriedman/Desktop/starfire_exercise/tmp_llm_workspace"):
			print("data pull query failed because it never created a dir")
			is_correct = "directory_never_created"

		elif not agent_execution_utils.ensure_non_empty_csv_is_present(str(data_pull_dict["data_path"])):
			print("data_pull_query failed due to non_existent csvs")
			is_correct = "non_existent_csvs"
		else:
			is_correct = "YES"

	except Exception as e:
		print("failed, exception")
		is_correct = "failed, exception" + str(e)

	end   = time.perf_counter()

	functionTime = end - start

	#CAREFUL THIS IS A DIRECTORY REMOVER
	print("removing dir")
	if os.path.exists("/Users/nfriedman/Desktop/starfire_exercise/tmp_llm_workspace"):
		shutil.rmtree("/Users/nfriedman/Desktop/starfire_exercise/tmp_llm_workspace")

	return is_correct, functionTime

#evaluates the accuracy of the analysis pipeline
def evaluate_analysis_pipeline(data_pull_dict, full_user_task, correct_answer):

	start = time.perf_counter()

	is_correct = "NO"
	try:
		data_analysis_result = execute_analysis_agent_with_qc_and_retry(full_user_task, data_pull_dict, 0, 5)
		print(data_analysis_result["free_text_summary"])

		isCorrectAnswer = llm_query_utils.evaluate_whether_an_answer_is_correct(candidate_answer, correct_answer)

	except Exception as e:
		is_correct = "failed exception"

	end   = time.perf_counter()

#Evaluates whether data integration was successful
def evaluate_data_integration(userQuery, answers, correct_answer):
	candidate_answer = llm_query_utils.integrate_answers_into_final_answer(userQuery, answers)
	isCorrectAnswer = llm_query_utils.evaluate_whether_an_answer_is_correct(candidate_answer, correct_answer)
	return isCorrectAnswer


#Currently we comment and uncomment for accuracy evaluation; TODO put into main and accept parameters

eval_data_integration = False
if eval_data_integration:

	#userQuery = "Which is perscribed more in California on a per capita basis? Prozac or Lamotrigine?"
	#subAnswers = ["California Prozac perscriptions were 10 per 100 citizens", "California Lamotrigine perscriptions were 5 per 100 citizens"]
	#correct_answer = "Prozac"

	#userQuery = "Which is medicine's rate of per capita perscription is grew at a faster rate in florida from 2022 - 2023'? Prozac or Lamotrigine?"
	#subAnswers = ["In florida, prozac perscriptions increased from 24.2 per capita to 26.7 per capita from 2021 - 2023", 
	#			  "In florida, Lamotrigine perscriptions increased from 24.2 per capita to 26 per capita from 2022-2023"]
	#correct_answer = "Lamotrigine"

	userQuery = "Do plan pharmacy network structures indirectly drive higher-cost drug utilization by limiting access to preferred alternatives?"
	subAnswers = ["Plans that contract with only 60–70% of local pharmacies tend to exclude outlets carrying low-cost generics on preferred tiers, pushing enrollees toward in-network pharmacies that stock higher-cost brands.",
				  "Members subject to narrow-network pharmacy designs paid on average $22 more per fill, driving 22% higher brand-name uptake—even when lower-cost generics existed.",
	              "Rebate-sharing arrangements were 2.3× more common in plans that limited pharmacy access, correlating with a 15% uptick in utilization of high-rebate, high-cost medications."]
	correct_answer = "YES"

	answers = []
	for i in range(50):
		isCorrect = evaluate_data_integration(userQuery, subAnswers, correct_answer)
		answers.append(isCorrect)
	print(Counter(answers))



eval_data_pull_agent = True
if eval_data_pull_agent:
	
	answers, times =[], []

	for i in range(10):

		full_user_task = "Pull all epipen perscriptions in west coast states"
		answer, t = evaluate_data_pull_agent(full_user_task)
		
		answers.append(answer)
		times.append(t)

	print(Counter(answers))
	print(times)



evaluate_analysis_pipeline = False
if evaluate_analysis_pipeline:
	pass

	answers, times =[], []

	for i in range(3):

		full_user_task = "Which is more common"
		data_pull_dict = ""
		correct_answer = ""
		answer, t = evaluate_analysis_pipeline(data_pull_dict, full_user_task, correct_answer)












#evaluate_data_pull_agent("Was was perscribed more in California in 2023: Lamictal or Prozac?")