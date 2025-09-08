import transformers
import torch

def create_judge():
	model_id = "meta-llama/Llama-3.1-8B-Instruct"

	system_prompt = """
	You are an expert judge of poetry. 10 CONTEXT poems labeled 1 through 10. Each CONTEXT poem has the name of the author after the label.
	The CONTEXT poems are similar to one another. You consider the CONTEXT poems examples of true poetry, and only prefer poems that share the rhyme schemes, meters, forms and content they employ.
	Respond with a list of four items of one sentence each, in the following format:

	FORM:
	RHYME:
	METER:
	CONTENT:

	FORM should be a summary of the types of poetic forms the items of CONTEXT use. RHYME should be a summary of the types of rhyme schemes the items of CONTEXT use. METER should be a summary of the metrical regularities the items of CONTEXT use. CONTENT should be a brief summary of the contents of CONTEXT.
	Respond only with this list, and do not use the word CONTEXT in your response.
	"""


	user_prompt_template = """
	CONTEXT:
	{context}

	"""

	quant = transformers.BitsAndBytesConfig(load_in_4bit=True)

	with open("context_poems.txt", "rt") as c_in:
	    context_poems = c_in.read()

	messages = [
	    {"role":"system", "content": system_prompt},
	    {"role":"user", "content": user_prompt_template.format(context=context_poems)}
	]


	pipeline = transformers.pipeline(
	    "text-generation", model=model_id, model_kwargs = {"quantization_config": quant, "device_map": "auto"} #model_kwargs={"dtype": torch.bfloat16}
	)
	output = pipeline(messages)
	print(output[0]["generated_text"][-1]["content"])
