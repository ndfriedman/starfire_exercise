#written by Noah Friedman
#Tools to do text LLM only queries

from huggingface_hub import InferenceClient
import prompt_reference_strs
import re
import ast

#query the llm text completion endpoint with a prompt
def query_llm(prompt):

	client = InferenceClient(
		provider="cerebras"
	)

	completion = client.chat.completions.create(
		model="meta-llama/Llama-3.3-70B-Instruct",
		messages=[
			{
				"role": "user",
				"content": prompt
				#"content": data_harmonize_prompt
			}
		],
	)

	result = completion.choices[0].message.content
	return result

#Takes the overall user analysis query and expresses it as a concise data pull query
def prepare_data_pull_query(user_analysis_query):
	
	medicare_dataset_description = prompt_reference_strs.get_val("dataset_description")

	prompt = (
		"Your job is to turn a user request into clear descriptions of data that needs to be pulled from the following datasets, described below:\n"
		f"{medicare_dataset_description}\n"
		"The user's request is:\n"
		f"{user_analysis_query}\n"
		"Return a concise sentence describing the characteristics of the data needed to be pulled\n"
		"Make sure to capture the years needed.  If none are specified, request 2023 data only\n"
		)

	resp = query_llm(prompt)
	return resp


def break_up_complex_query_into_subqueries(userQuery):

	prompt = (
		"Your job is to turn a complex user analyses into the subanalyses required to solve it\n"
		"A subanalysis consists of a single data pull from a database and associated analysis that can be performed based on the results of the data pull\n"
		"Return a python list of strings. \n" 
		"Each entry in the python list is a string describing the subanalyses necessary to perform the task\n"
		"Minimize the total number of subanalyses you prepare\n"
		"Do not list as a subtask the final task of comparing prepared analyses after all data has been pulled\n"
		"Your answer must begin with [ and end with ]\n"
		f"The analysis request you will be decomposing is:{userQuery}"
		) 

	res = query_llm(prompt)

	analysis_list = re.search(r'\[.*?\]', res, flags=re.DOTALL).group(0)
	analysis_list = ast.literal_eval(analysis_list)

	if not isinstance(analysis_list, list):
		analysis_list = list(analysis_list)

	return analysis_list

def integrate_answers_into_final_answer(userQuery, answers):
	prompt = (
		f"Your job is to answer the following query{userQuery}\n"
		f"You will based your answer to the query on the following subresults relevant to the query. The subaresults are:{answers}"
		)	

	res = query_llm(prompt)
	return res

def evaluate_whether_an_answer_is_correct(candidate_answer, correct_answer):
	prompt = (
		"You will evaluate whether a candidate answer is equal to the correct answer\n"
		f"The candidate answer is: {candidate_answer}\n"
		f"The correct answer is: {correct_answer}\n"
		"Return YES if the candidate answer is conceptually equal to the correct answer"
		"Return NO if the candidate answer is not conceptually equal to the correct answer"
		"Return only a single word: YES or NO\n"
		)

	res = query_llm(prompt)
	return res






