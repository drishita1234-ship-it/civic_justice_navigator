from nlp.language_detect import detect_language
from nlp.translator import translate_to_english
from nlp.simplify_legal import simplify_legal_text

def process_user_query(text):

    language = detect_language(text)

    translated = translate_to_english(text, language)

    simplified = simplify_legal_text(translated)

    return {
        "language": language,
        "translated": translated,
        "simplified": simplified
    }