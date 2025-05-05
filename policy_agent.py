from crewai import Crew, Task, Agent, LLM
from crewai_tools import PDFSearchTool,RagTool
from dotenv import load_dotenv
load_dotenv()

from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Context, RunYield, RunYieldResume, Server


llm = LLM(
    model="ollama_chat/qwen2.5:14b", 
    base_url="http://localhost:11434", 
)

config=dict(
    llm=dict(
    provider="ollama",
    config=dict(
        model="qwen2.5:14b",
        ),
    ),
    embedder=dict(
        provider="google",
        config=dict(
            model="models/embedding-001",
            task_type="retrieval_document",
        ),
    ),
)

rag_tool = PDFSearchTool(config=config,pdf="./data/Cloud-Computing-Theory-And-Practice.pdf")


"Cloud-Computing-Theory-And-Practice.pdf"
# rag_tool = RagTool(config=config)
# rag_tool.add("data",data_type = "file")

insurance_agent = Agent(
    role="Senior Cloud Computing Engineer", 
    goal="Answer Queries about Cloud Computing",
    backstory="You are an expert cloud computing engineer designed to assist with user queries",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[rag_tool], 
    max_retry_limit=5
)
    
server = Server()

@server.agent()
async def cloud_engineer(input: list[Message], context: Context) -> AsyncGenerator[RunYield, RunYieldResume]:
    task = Task(
        description=input[0].parts[0].content,
        expected_output= "A comprehensive response as to the users question",
        agent=insurance_agent
    )

    crew = Crew(
        agents=[insurance_agent],
        tasks=[task],
        verbose=True
    )

    task_output = await crew.kickoff_async()
    yield Message(parts=[MessagePart(content =str(task_output))])

if __name__ == "__main__":
    server.run(port=8001)