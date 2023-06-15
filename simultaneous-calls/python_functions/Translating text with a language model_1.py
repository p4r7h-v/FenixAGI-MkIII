from transformers import MarianMTModel, MarianTokenizer

def translate_text(text, src_lang="en", target_lang="fr"):
    """
    Translates the text with a pre-trained language model.
    Args:
        text (str): The text to be translated.
        src_lang (str): The source language code (e.g., "en" for English).
        target_lang (str): The target language code (e.g., "fr" for French).
    Returns:
        translated_text (str): The translated text.
    """

    # Define the model and tokenizer based on the language pair
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{target_lang}"
    
    # Initialize the tokenizer and model
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # Tokenize the text
    input_tokens = tokenizer(text, return_tensors="pt")

    # Get the translated output
    translated_tokens = model.generate(**input_tokens)

    # Decode the translation
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

    return translated_text