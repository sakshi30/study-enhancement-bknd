import json
import os

from algoliasearch.search.client import SearchClientSync

class AlgoliaServer:
    def __init__(self):
        self.app_id = os.getenv("ALGOLIA_APPLICATION_KEY")
        self.api_key = os.getenv("ALGOLIA_WRITE_API_KEY")
        self.index_name= os.getenv("ALGOLIA_INDEX_NAME")

    def save_record_to_server(self, record):
        client = SearchClientSync(self.app_id, self.api_key)
        save_resp = client.save_object(
            index_name=self.index_name, body=record
        )
        print(save_resp)
        return save_resp