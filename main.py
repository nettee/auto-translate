from googletrans import Translator

if __name__ == '__main__':

    translator = Translator()
    trans = translator.translate('Hello, world.', dest='zh-CN')
    print(trans.origin, '->', trans.text)
