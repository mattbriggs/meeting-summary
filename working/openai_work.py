import openai

openai.api_key = MU.get_textfromfile('../marmot.txt')

def create_tight_summary(prompt):
  '''Use the OpenAI endpoint to create a summary.'''

  response = openai.Completion.create(
      model="text-davinci-003",
      prompt="Summarize this for a fifth-grade student: {}".format(prompt),
      temperature=0.7,
      max_tokens=2000,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
      ) 
  return response["choices"][0]["text"]

prompt = '''
So we will have variation where a design pattern doesn't show up as architecture will show up as design pattern to create variety as we create the pattern library. The other area is your pattern, other architecture content, and I say that's one pattern with different varies of depth so. Everything is architecture and it's under one pattern of architecture and this is this way because we only have one yamel name that is architecture. Think maybe four of us and say from a content architecture perspective, what do we think we are lacking the most in our content sets up? Tomorrow, if we have an Uber browse UI right and someone did choose like analytics, it would show the product documentation for all product services that all under analytics and all architecture related to that particular byte. I think that the bigger chunk that we call conceptual can be kept aside for a moment, whereas we can deal with the architecture and with the three depths and the design patterns and move ahead with the patterns. A lot of our content is already in the structured content model, and if unfortunately that falls under just one gigantic pattern.
'''
print(create_tight_summary(prompt))