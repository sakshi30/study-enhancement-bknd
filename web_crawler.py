import os
import requests
import json
from prompts_dict import prompts_dict
from ai_generator import AIGenerator

class WebCrawler:
    def __init__(self):
        self.jina_base_url = "https://r.jina.ai/"
        self.headers = {
            "Authorization": "Bearer "+os.getenv("JINA_PARSER")
        }
        self.ai_generator = AIGenerator()
        self.extracted_content = {}

    def parse_link(self, link, id):
        jina_url = f"{self.jina_base_url}{link}"
        response = requests.get(jina_url, headers=self.headers)
        summary_prompt = prompts_dict["CRAWLER_PROMPT"] + response.text

        response_text = self.ai_generator.generate_response(summary_prompt)
        output = json.loads(response_text)
        self.extracted_content = {
            "user_id": id,
            'pages': 1,
            'title': output["title"],
            'type': "url",
            'source': output["url"],
            'summary': output["summary"],
            'key_points': output["key_points"],
            'size': len(response.text)
        }