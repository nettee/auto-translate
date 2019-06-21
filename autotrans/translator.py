import os
from pathlib import Path
from urllib.parse import urlparse

import requests
import googletrans

from autotrans.document import Document

current_path = os.path.realpath(__file__)
workspace = Path(current_path).parent / 'workspace'
Path.mkdir(workspace, exist_ok=True)


class AutoTranslator:

    def __init__(self, src):
        self.translator = googletrans.Translator()
        self.parse_src(src)

    def parse_src(self, src):
        file = Path(src)
        if not file.exists():
            file = self.download_to_workspace(src)
        document = Document(file)

    @staticmethod
    def download_to_workspace(url):
        r = requests.get(url)
        r.raise_for_status()
        filename = os.path.basename(urlparse(url).path)
        file = workspace / filename
        if file.exists:
            print(file.name, 'already exists, and will be overwritten')

        with file.open('wb') as of:
            of.write(r.content)
        print('Saved content to file', filename)
        return file

    def translate(self, text):
        trans = self.translator.translate(text, dest='zh-CN')
        return trans.text
