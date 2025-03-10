from crewai import LLM
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class Dog(BaseModel):
    name: str
    age: int
    breed: str


llm = LLM(model="gpt-4o-mini",api_key=os.environ["OPENAI_API_KEY"],response_format=Dog)

response = llm.call(
    "Analyze the following messages and return the name, age, and breed. "
    "Meet Jonawww! She is 3 years old and is a black german shepherd."
)

print(response)

# Output:
# Dog(name='Kona', age=3, breed='black german shepherd')
