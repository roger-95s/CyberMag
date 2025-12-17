"""
How to solve a complex problem? 
Problem: AI response format is not as expected
Expected response should be a JSON format following file: cyberattack_analysis_prompt.json


Possible solutions approuches: 
1. Save ai response output into text file and then convert it into JSON, save JSON in to sql database.
    steps: 
    a) Enforce llm to output: exactly like the json structure of /cyberattack_analysis_prompt.json  
    b) Output verifyier 
    c) save verified ouput into the db 
    d) Final test if data was save     

"""

from ollama import chat
from pydantic import BaseModel

class Pet(BaseModel):
  name: str
  animal: str
  age: int
  color: str | None
  favorite_toy: str | None

class PetList(BaseModel):
  pets: list[Pet]

response = chat(
  messages=[
    {
      'role': 'user',
      'content': '''
        I have two pets.
        A cat named Luna who is 5 years old and loves playing with yarn. She has grey fur.
        I also have a 2 year old black cat named Loki who loves tennis balls.
      ''',
    }
  ],
  model='llama3.1',
  format=PetList.model_json_schema(),
)

pets = PetList.model_validate_json(response.message.content)
print(pets)
