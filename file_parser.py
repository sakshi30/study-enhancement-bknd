import pdfplumber
import json
import re
from io import BytesIO
from prompts_dict import prompts_dict
from ai_generator import AIGenerator

class FileParser:
    def __init__(self):
        self.processed_files = []
        self.ai_generator = AIGenerator()

    def read_files(self, files, id):
        for file in files:
            file_data = file.read()
            with pdfplumber.open(BytesIO(file_data)) as pdf:
                text_content = ""
                # tables = []
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"
                    # page_tables = page.extract_tables()
                    # if page_tables:
                    #     tables.extend(page_tables)
                summary_prompt = prompts_dict["SUMMARY_PROMPT"] + text_content
                response_text = self.ai_generator.generate_response(summary_prompt)
                clean_text = re.sub(r"^```(?:json)?|```$", "", response_text.strip(), flags=re.MULTILINE).strip()

                response  = json.loads(clean_text)
                self.processed_files.append({
                    "user_id": id,
                    'filename': file.filename,
                    'pages': len(pdf.pages),
                    'title': response["title"],
                    'type': response["type"],
                    'source': response["source"],
                    'summary': response["summary"],
                    'key_points': response["key_points"],
                    'size': len(file_data)
                })
