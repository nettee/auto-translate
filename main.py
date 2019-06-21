from autotrans.auto_translator import AutoTranslator

if __name__ == '__main__':

    translator = AutoTranslator()
    text = 'Hello, world.'
    trans = translator.translate(text)
    print(text, '->', trans)
