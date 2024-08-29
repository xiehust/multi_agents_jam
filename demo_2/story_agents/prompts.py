fc_desc = """
You will ALWAYS follow the below guidelines when you are answering a question:
<guidelines>
- Think through the user's question, extract all data from the question and the previous conversations before creating a plan.
- Your response must be follow the pydantic schema as:
<schema>
{schema}
</shema>
- output your answer in json markdown format, so that the user can use pydantic basemodel.parse_obj() to parse the json string into an object which defined as:
 <schema>
 {schema}
 </shema>
- Avoid quotation mark within a quotation mark, if encountering a quotation mark within a quotation mark, it needs to be single quotation mark instead
- if the content has quotation mark, please change to single quotation mark instead
</guidelines>
"""