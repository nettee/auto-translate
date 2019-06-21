import googletrans


class AutoTranslator:

    def __init__(self):
        self.translator = googletrans.Translator()

    def translate(self, text):
        trans = self.translator.translate(text, dest='zh-CN')
        return trans.text
