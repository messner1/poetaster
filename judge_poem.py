import transformers
import torch
import json
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)
transformers.logging.disable_progress_bar()

def judge_poem(judge_desc, submitted_poem):
    model_id = "meta-llama/Llama-3.1-8B-Instruct"

    #system_prompt = """
    #You are an expert judge of poetry. You are given a SUBMITTED poem and 10 CONTEXT poems labeled 1 through 10. Each CONTEXT poem has the name of the author after the label.
    #The CONTEXT poems are similar to one another. The SUBMITTED poem may be similar to or different from the CONTEXT poems.
    #You like the CONTEXT poems the best. You consider the CONTEXT poems examples of true poetry. 
    #Using this preference rate the SUBMITTED poem on a scale of 1 to 10. Do not rely on prior knowledge of the SUBMITTED poem to aid your rating.
    #Return only your numerical rating and a one sentence declaration of how SUBMITTED could be improved by changing its form, rhyme scheme, or meter. Do not refer to the CONTEXT poems.
    #"""


    system_prompt = """You are an expert judge of poetry. You are given a SUBMITTED poem and CRITERIA in which to judge the SUBMITTED poem.
    CRITERIA has four headings, FORM, RHYME, METER and CONTENT. FORM describes the type of poetic forms you prefer. RHYME describes the type of rhyme schemes you prefer.
    METER describes the metrical schemes you prefer. CONTENT describes the types of content you prefer. Use only these criteria to guide your judgement.
    Return a valid JSON object with two elements. The first, SCORE is a numeric grading from 1-10 of SUBMITTED in light of CRITERIA.
    The second FEEDBACK is a one sentence summary of how SUBMITTED could change to fit the descriptions in CRITERIA. Do not refer to CONTEXT in FEEDBACK. Only respond only with this JSON object.
    
    CRITERIA:
    FORM: {form}
    RHYME: {rhyme}
    METER: {meter}
    CONTENT: {content}

    """

    user_prompt_template = """
    SUBMITTED:
    {submitted}
    """

    quant = transformers.BitsAndBytesConfig(load_in_4bit=True)

    #with open("context_poems.txt", "rt") as c_in:
    #    context_poems = c_in.read()

    #with open("test.txt", "rt") as s_in:
    #    submitted_poem = s_in.read()

    messages = [
        {"role":"system", "content": system_prompt.format(form=judge_desc["FORM"], rhyme=judge_desc["RHYME"], meter=judge_desc["METER"], content=judge_desc["CONTENT"])},
        {"role":"user", "content": user_prompt_template.format( submitted=submitted_poem)}
    ]



    for attempt in range(3):
        try:
            pipeline = transformers.pipeline(
                "text-generation", model=model_id, model_kwargs = {"quantization_config": quant, "device_map": "auto"} #model_kwargs={"dtype": torch.bfloat16}
            )
            output = pipeline(messages)
            raw = output[0]["generated_text"][-1]["content"]
            js = json.loads(raw)

            return int(js["SCORE"]), js["FEEDBACK"]
        except json.JSONDecodeError:
            continue