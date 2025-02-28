import os
import subprocess
import whisper
import nltk
from textblob import TextBlob


import re

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
nltk.download('wordnet')


def extract_audio(video_path, output_audio="output.wav"):
    if not os.path.exists(video_path):
        print("❌ Error: Video file not found!")
        return None

    print("🎬 Extracting audio from video...")
    command = f"ffmpeg -i \"{video_path}\" -vn -acodec pcm_s16le -ar 16000 -ac 1 \"{output_audio}\" -y"
    process = subprocess.run(command, shell=True, capture_output=True, text=True)

    if os.path.exists(output_audio):
        print("✅ Audio extraction successful:", output_audio)
        return output_audio
    else:
        print("❌ Error: Audio extraction failed!")
        print("FFmpeg Error:", process.stderr)
        return None

def transcribe_audio(audio_path):
    if not os.path.exists(audio_path):
        print("❌ Error: Audio file not found!")
        return None

    print("📝 Transcribing audio using Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    if result["text"]:
        print("✅ Transcription completed successfully!")
        return result["text"]
    else:
        print("❌ Error: Transcription failed!")
        return None

def analyze_text(text):
    print("📊 Performing text analysis...")

    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity

 
    fillers = ["uh","oh","ohh" "um", "like", "you know", "so", "actually", "basically", "literally"]
    hesitation_count = sum(len(re.findall(rf"\b{filler}\b", text, re.IGNORECASE)) for filler in fillers)

    grammar_errors = [sentence for sentence in blob.sentences if sentence.sentiment.polarity < -0.3]

    return {
        "sentiment": "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral",
        "sentiment_score": sentiment_score,
        "hesitation_count": hesitation_count,
        "grammar_issues": [str(sentence) for sentence in grammar_errors]
    }

def analyze_video(video_path):
    
    print("🚀 Starting video analysis...")

  
    audio_path = extract_audio(video_path)
    if not audio_path:
        return

   
    transcript = transcribe_audio(audio_path)
    if not transcript:
        return

    analysis = analyze_text(transcript)

    
    print("\n🔹 TRANSCRIPTION 🔹\n")
    print(transcript)
    print("\n🔹 ANALYSIS 🔹\n")
    print(f"✅ Sentiment: {analysis['sentiment']} (Score: {analysis['sentiment_score']:.2f})")
    print(f"⚠️ Hesitations (Filler Words Used): {analysis['hesitation_count']}")
    print(f"❌ Grammar Issues: {len(analysis['grammar_issues'])}")

    if analysis['grammar_issues']:
        print("\n🔻 Mistakes Found:\n" + "\n".join(analysis['grammar_issues']))

video_path = "/content/WhatsApp Video 2025-03-01 at 2.57.42 AM.mp4" 
analyze_video(video_path)

