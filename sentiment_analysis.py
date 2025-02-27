import os
import subprocess
import whisper
import nltk
from textblob import TextBlob
import re

nltk.download("punkt")

def extract_audio(video_path, output_audio="output.wav"):
    command = f"ffmpeg -i {video_path} -vn -acodec pcm_s16le -ar 16000 -ac 1 {output_audio} -y"
    subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_audio

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

def analyze_text(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    fillers = ["uh", "um", "like", "you know", "so", "actually", "basically", "literally"]
    hesitation_count = sum(len(re.findall(rf"\b{filler}\b", text, re.IGNORECASE)) for filler in fillers)
    grammar_errors = [sentence for sentence in blob.sentences if sentence.sentiment.polarity < -0.3]
    return {
        "sentiment": "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral",
        "sentiment_score": sentiment_score,
        "hesitation_count": hesitation_count,
        "grammar_issues": [str(sentence) for sentence in grammar_errors]
    }

def analyze_video(video_path):
    audio_path = extract_audio(video_path)
    transcript = transcribe_audio(audio_path)
    analysis = analyze_text(transcript)
    
    print("\nTRANSCRIPTION\n")
    print(transcript)
    print("\nANALYSIS\n")
    print(f"Sentiment: {analysis['sentiment']} (Score: {analysis['sentiment_score']:.2f})")
    print(f"Hesitations (Filler Words Used): {analysis['hesitation_count']}")
    print(f"Grammar Issues: {len(analysis['grammar_issues'])}")
    if analysis['grammar_issues']:
        print("\nMistakes Found:\n" + "\n".join(analysis['grammar_issues']))

if _name_ == "_main_":
    video_file = input("Enter the path of your video file: ")
    analyze_video(video_file)
