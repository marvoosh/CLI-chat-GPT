from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
import fire

import os
os.environ["OPENAI_API_KEY"] ="YOUR API KEY"


def main(path: str, query: str):
    loader = PyPDFLoader(path)

    pages = loader.load_and_split()
    embeddings = OpenAIEmbeddings()

    db = FAISS.from_documents(pages, embeddings)
    docs = db.similarity_search(query)

    llm = OpenAI(temperature=0.9)  # model_name="gpt-3.5-turbo"
    chain = load_qa_chain(llm, chain_type='stuff')
    response = chain.run(input_documents=docs, question=query)
    print(response)

if __name__ == "__main__":
    fire.Fire({
        "query": main
    })
