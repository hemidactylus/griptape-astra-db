import os

from griptape.structures import Agent  # type: ignore
from griptape.tools import VectorStoreClient, TaskMemoryClient  # type: ignore
from griptape.loaders import WebLoader  # type: ignore
from griptape.engines import VectorQueryEngine  # type: ignore
from griptape.drivers import OpenAiEmbeddingDriver, OpenAiChatPromptDriver  # type: ignore

from griptape_astra_db_tools import AstraDBVectorStoreDriver


engine = VectorQueryEngine(
    prompt_driver=OpenAiChatPromptDriver(model="gpt-3.5-turbo"),
    vector_store_driver=AstraDBVectorStoreDriver(
        embedding_driver=OpenAiEmbeddingDriver(),  # type: ignore[call-arg]
        api_endpoint=os.environ["ASTRA_DB_API_ENDPOINT"],
        token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
        collection_name="griptape_test_collection",
        astra_db_namespace=os.environ.get("ASTRA_DB_KEYSPACE"),
        dimension=1536,
    ),
)

engine.upsert_text_artifacts(WebLoader().load("https://en.wikipedia.org/wiki/Uloboridae"), namespace="uloboridae")

vector_db = VectorStoreClient(
    description="This is a brief account on the Uloboridae family.", query_engine=engine, namespace="uloboridae"
)

agent = Agent(tools=[vector_db, TaskMemoryClient(off_prompt=False)])

agent.run("How do Uloboridae stand out compared to other families?")
