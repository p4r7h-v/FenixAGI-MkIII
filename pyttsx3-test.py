import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)
   engine.say("""
   The stratGPT.py file is a Python script leveraging the OpenAI API to generate goal-oriented strategies. Key features include multiple library imports, strategy extraction, and user interaction functions for defining tasks, generating strategies, and selecting the optimal strategy.

Visualizer.py, on the other hand, visualizes data in 3D. It employs various libraries, includes functions to load and process CSV data, applies dimensionality reduction using TSNE, and generates a 3D scatter plot. It defaults to a dark mode visualization and handles FileNotFoundError exceptions.
   """"")
engine.runAndWait()