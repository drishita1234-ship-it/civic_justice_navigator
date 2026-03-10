from translator import translate_to_english
from language_detect import detect_language

text = "இந்த வழக்கு எவ்வளவு நாள் ஆகும்?"

lang = detect_language(text)

translated = translate_to_english(text, lang)

print("Original:", text)
print("Translated:", translated)