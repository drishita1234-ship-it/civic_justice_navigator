from language_detect import detect_language

text = "இந்த வழக்கு எவ்வளவு நாள் ஆகும்?"

lang = detect_language(text)

print("Detected Language:", lang)