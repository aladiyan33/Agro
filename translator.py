from googletrans import Translator

translator = Translator()

def translate_text(text, lang="ta"):
    try:
        return translator.translate(text, dest=lang).text
    except:
        return "Translation failed"
