from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

import os
from langserve import add_routes
from dotenv import load_dotenv


# Import and patch the broken model
#from langserve.validation import chainBatchRequest

# Patch Pydantic model
#chainBatchRequest.model_rebuild()

GROQ_API_KEY="yu"
#groq_api_key=os.getenv("GROQ_API_KEY")

model=ChatGroq(model="llama-3.1-8b-instant",groq_api_key=GROQ_API_KEY)


#1. Create Prompt Template

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

parser = StrOutputParser()

#Create Chain 

chain=prompt_template|model|parser

#App definition 

app=FastAPI(title="This is my Langchain server",
            version="1.0",
            description="A Simple API server")

#Langserve : Adding Chain route

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1", port=8000)