import transformers
import torch

model_id = "meta-llama/Llama-3.1-8B-Instruct"

system_prompt = """
You are an expert judge of poetry. You are given a SUBMITTED poem and 10 CONTEXT poems labeled 1 through 10. Each CONTEXT poem has the name of the author after the label.
The CONTEXT poems are similar to one another. The SUBMITTED poem may be similar to or different from the CONTEXT poems.
You like the CONTEXT poems the best. You consider the CONTEXT poems examples of true poetry. 
Using this preference rate the SUBMITTED poem on a scale of 1 to 10. Do not rely on prior knowledge of the SUBMITTED poem to aid your rating.
Return only your numerical rating and a one sentence declaration of how SUBMITTED could be improved by changing its form, rhyme scheme, or meter. Do not refer to the CONTEXT poems.
"""


user_prompt_template = """
CONTEXT:
{context}

SUBMITTED:
{submitted}
"""

quant = transformers.BitsAndBytesConfig(load_in_4bit=True)

with open("context_poems.txt", "rt") as c_in:
    context_poems = c_in.read()

with open("test.txt", "rt") as s_in:
    submitted_poem = s_in.read()

messages = [
    {"role":"system", "content": system_prompt.format(form_desc="sonnet")},
    {"role":"user", "content": user_prompt_template.format(context=context_poems, submitted=submitted_poem)}
]


pipeline = transformers.pipeline(
    "text-generation", model=model_id, model_kwargs = {"quantization_config": quant, "device_map": "auto"} #model_kwargs={"dtype": torch.bfloat16}
)
output = pipeline(messages)
print(output[0]["generated_text"][-1]["content"])