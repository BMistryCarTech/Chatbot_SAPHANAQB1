from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm import get_llm
from hana import query_hana

llm = get_llm()

general_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer truthfully. If you don't know, say so."),
    ("user", "{question}")
])
general_chain = general_prompt | llm | StrOutputParser()

@tool
def general_qa_tool(question: str) -> str:
    """Handles general non-database-related questions."""
    return general_chain.invoke({"question": question})

@tool
def hana_query_tool(query: str) -> str:
    """Handles SAP HANA DB queries."""
    return query_hana(query)

tools = [general_qa_tool, hana_query_tool]
