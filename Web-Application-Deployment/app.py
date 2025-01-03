# -*- coding: utf-8 -*-
"""App.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cOSBC8HgqdwROWmFtg3yTgEQySq2ePfx
"""

import gradio as gr
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import pickle
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

tokenizer = AutoTokenizer.from_pretrained('/content/drive/MyDrive/saved_mental_status_bert')
model = AutoModelForSequenceClassification.from_pretrained('/content/drive/MyDrive/saved_mental_status_bert')
label_encoder = pickle.load(open('/content/drive/MyDrive/label_encoder.pkl','rb'))

stop_words = set(stopwords.words('english'))

def clean_statement(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

def detect_anxiety(text):
    cleaned_text = clean_statement(text)
    inputs = tokenizer(cleaned_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return label_encoder.inverse_transform([predicted_class])[0]

with gr.Blocks(theme=gr.themes.Soft()) as interface:
    gr.Markdown("# Mental Health Status Detector")
    gr.Markdown("Enter how you are feeling today, and this tool will predict your mental health status.")
    with gr.Row():
        input_text = gr.Textbox(placeholder="Describe your feelings here...", label="Your Input")
        output_text = gr.Textbox(label="Predicted Status", interactive=False)
    submit_button = gr.Button("Detect")

    submit_button.click(fn=detect_anxiety, inputs=input_text, outputs=output_text)

interface.launch()