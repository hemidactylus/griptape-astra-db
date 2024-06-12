import os

from astrapy import DataAPIClient

from griptape_astra_db_tools import AstraDBVectorStoreDriver
from griptape.drivers.embedding.openai_embedding_driver import OpenAiEmbeddingDriver  # type: ignore

TEST_COLLECTION_NAME = "griptape_test_collection"


class TestAstraDBVectorStoreDriver:
    def test_astra_db_store_driver(self):
        """
        Env vars are required, this is an integration test.
        """
        embedding_driver = OpenAiEmbeddingDriver(api_key=os.environ["OPENAI_API_KEY"])
        driver = AstraDBVectorStoreDriver(
            embedding_driver=embedding_driver,
            api_endpoint=os.environ["ASTRA_DB_API_ENDPOINT"],
            token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
            collection_name=TEST_COLLECTION_NAME,
            astra_db_namespace=os.environ.get("ASTRA_DB_KEYSPACE"),
            dimension=1536,
        )

        s1 = "A cat sits on the couch"
        s2 = "Read the manual and find out how to do it"
        sq = "You should take the instructions and peruse them, so you will know."
        v1 = embedding_driver.embed_string(s1)
        v2 = embedding_driver.embed_string(s2)

        id1 = driver.upsert_vector(vector=v1, namespace="ns", meta={"self_id": True})
        assert isinstance(id1, str)

        id2 = driver.upsert_vector(vector=v2, vector_id="id2", namespace="ns", meta={"self_id": False})
        assert id2 == "id2"

        e2 = driver.load_entry(vector_id=id2)
        assert e2.id == id2
        assert e2.vector == v2
        assert e2.meta == {"self_id": False}
        assert e2.namespace == "ns"

        entries = driver.load_entries(namespace="ns")
        ids = {e.id for e in entries}
        assert ids == {id1, id2}

        ann_entries = driver.query(sq, count=2, namespace="ns", include_vectors=True)
        assert ann_entries[0].id == id2
        assert ann_entries[1].id == id1
        assert ann_entries[1].meta == {"self_id": True}
        assert ann_entries[1].vector == v1

        driver.delete_vector(id2)

        ann_post_delete = driver.query(sq, count=2, namespace="ns", include_vectors=True)
        assert len(ann_post_delete) == 1

        driver.delete_vector(id1)

        ann_post_delete2 = driver.query(sq, count=2, namespace="ns", include_vectors=True)
        assert len(ann_post_delete2) == 0

        # cleanup (bypass Griptape and use astrapy for a hard reset)
        DataAPIClient(token=os.environ["ASTRA_DB_APPLICATION_TOKEN"]).get_database(
            os.environ["ASTRA_DB_API_ENDPOINT"], namespace=os.environ.get("ASTRA_DB_KEYSPACE")
        ).drop_collection(TEST_COLLECTION_NAME)
