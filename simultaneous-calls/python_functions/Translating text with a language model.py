from transformers import MarianMTModel, MarianTokenizer

def translate_text(text, src_lang="en", trg_lang="es"):
    """
    Translates text using Hugging Face's Transformers library and pretrained MarianMT model.
    
    Args:
        text (str): The text to translate.
        src_lang (str, optional): Source language code (default is "en").
        trg_lang (str, optional): Target language code (default is "es").

    Returns:
        str: Translated text.
    """

    # Define the model name
    model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{trg_lang}'

    # Load the tokenizer and model
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # Tokenize the input text
    inputs = tokenizer.encode(text, return_tensors="pt")

    # Generate the translated text
    outputs = model.generate(inputs, max_length=512, num_beams=4, early_stopping=True)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return translated_text

# Example usage:
text = "Hello, world!"
translated_text = translate_text(text, src_lang="en", trg_lang="es")
print(f"Original text: {text}\nTranslated text: {translated_text}")