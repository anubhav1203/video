# -*- coding: utf-8 -*-
"""video.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Zvt0hiTTrzjDBHcZ5jjXrwfMg1Blmlm2
"""

from google.cloud import speech_v1 as speech

def transcribe_audio(audio_file):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=audio_file)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    transcription = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcription

import openai

openai.api_key = "YOUR_AZURE_OPENAI_KEY"

def correct_transcription(transcription):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Correct the following transcription: '{transcription}'"}
        ]
    )
    corrected_transcription = response.choices[0].message.content.strip()
    return corrected_transcription

from google.cloud import texttospeech

def generate_audio(text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
    )
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)

from moviepy.editor import VideoFileClip, AudioFileClip

def replace_audio(video_file, new_audio_file):
    video = VideoFileClip(video_file)
    audio = AudioFileClip(new_audio_file)
    final_video = video.set_audio(audio)
    final_video.write_videofile("final_output.mp4")

import streamlit as st

st.title("Video Audio Replacement with AI Voice")
video_file = st.file_uploader("Upload a Video", type=["mp4", "avi"])

if video_file:
    # Extract and transcribe audio
    transcription = transcribe_audio(video_file)
    corrected_transcription = correct_transcription(transcription)
    generate_audio(corrected_transcription)

    # Replace audio in video
    replace_audio(video_file, "output.mp3")
    st.success("Audio replaced successfully!")

