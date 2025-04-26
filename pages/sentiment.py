import streamlit as st
import os
import tempfile
import subprocess
from faster_whisper import WhisperModel
from textblob import TextBlob
import re
import logging

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Initialize Session State ---
if 'uploaded_video_path' not in st.session_state:
    st.session_state.uploaded_video_path = None

# --- Page Configuration ---
st.set_page_config(page_title="Sentiment Analysis", page_icon="🧠", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1B1F3B, #162447);
        font-family: 'Poppins', sans-serif;
        color: white;
        text-align: center;
    }
    .title {
        font-size: 60px;
        font-weight: bold;
        color: #38BDF8;
        text-shadow: 2px 2px 10px #38BDF8;
    }
    .upload-container {
        margin-top: 20px;
        padding: 15px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
    }
    .stButton button {
        background: linear-gradient(135deg, #6EE7B7, #3B82F6);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #3B82F6, #6EE7B7);
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .stButton button:active {
        transform: translateY(0);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .analysis-card {
        padding: 20px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
        margin: 10px 0;
    }
    .footer {
        margin-top: 50px;
        font-size: 14px;
        color: #888;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Optimized Whisper Model ---
@st.cache_resource
def load_model():
    try:
        return WhisperModel("small", device="cpu", compute_type="int8")
    except Exception as e:
        st.error(f"⚠️ Model loading failed: {str(e)}")
        return None

model = load_model()

# --- File Upload Section ---
st.markdown('<p class="title">🧠 Sentiment Analysis</p>', unsafe_allow_html=True)
st.markdown("## 📤 Upload Video File")
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file:
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(uploaded_file.read())
        st.session_state.uploaded_video_path = tmp_file.name

# --- Enhanced Audio Extraction ---
def extract_audio(video_path):
    """Extracts audio from video with error handling and validation"""
    try:
        temp_audio = tempfile.mktemp(suffix=".wav")

        ffmpeg_cmd = [
            'ffmpeg',
            '-y',
            '-i', video_path,
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            '-f', 'wav',
            '-loglevel', 'error',
            temp_audio
        ]

        result = subprocess.run(
            ffmpeg_cmd,
            capture_output=True,
            text=True,
            check=True
        )

        if not os.path.exists(temp_audio):
            raise Exception(f"Output file {temp_audio} was not created")
            
        if os.path.getsize(temp_audio) == 0:
            os.remove(temp_audio)
            raise Exception("Empty audio file generated - possibly no audio stream")

        return temp_audio

    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg error: {e.stderr}")
        if "No such file or directory" in e.stderr:
            st.error("⚠️ Input video file not found")
        elif "Invalid data found" in e.stderr:
            st.error("⚠️ Corrupted or unsupported video format")
        else:
            st.error(f"⚠️ Audio extraction failed: {e.stderr}")
    except Exception as e:
        logger.error(str(e))
        st.error(f"⚠️ {str(e)}")
    return None

# --- Robust Transcription ---
def transcribe_audio(audio_path):
    """Transcribes audio with error handling"""
    if not model:
        st.error("Model not loaded!")
        return ""
    
    try:
        segments, info = model.transcribe(
            audio_path,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        transcript = " ".join(segment.text for segment in segments)
        os.remove(audio_path)  # Cleanup temp file
        return transcript
    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}")
        st.error(f"⚠️ Transcription error: {str(e)}")
        return ""

# --- Enhanced Sentiment Analysis ---
def analyze_sentiment(text):
    """Analyzes sentiment with improved validation"""
    if not text.strip():
        return {
            "Sentiment": "No Speech",
            "Sentiment Score": 0,
            "Hesitation Count": 0,
            "Grammar Issues": []
        }

    try:
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity

        fillers = ["uh", "um", "like", "you know", "so", "actually", "basically"]
        hesitation_count = sum(
            len(re.findall(rf"\b{re.escape(filler)}\b", text, re.IGNORECASE))
            for filler in fillers
        )

        grammar_issues = [
            str(sentence) for sentence in blob.sentences
            if sentence.sentiment.polarity < -0.3
            and len(sentence.words) > 3
        ]

        return {
            "Sentiment": "Positive" if sentiment_score > 0.1 else 
                        "Negative" if sentiment_score < -0.1 else "Neutral",
            "Sentiment Score": sentiment_score,
            "Hesitation Count": hesitation_count,
            "Grammar Issues": grammar_issues
        }
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {str(e)}")
        return {
            "Sentiment": "Error",
            "Sentiment Score": 0,
            "Hesitation Count": 0,
            "Grammar Issues": []
        }

# --- Main UI ---
st.markdown("## 🎙️ Transcription + Sentiment Analysis")

if st.session_state.uploaded_video_path and os.path.exists(st.session_state.uploaded_video_path):
    with st.expander("🎥 Preview Video"):
        st.video(st.session_state.uploaded_video_path)

    if st.button("🚀 Start Analysis", type="primary"):
        with st.spinner("🔍 Extracting audio..."):
            audio_file = extract_audio(st.session_state.uploaded_video_path)
            
        if audio_file:
            with st.spinner("📝 Transcribing audio..."):
                transcript = transcribe_audio(audio_file)
                
            if transcript:
                st.success("✅ Transcription Complete!")
                with st.expander("📜 View Transcript"):
                    st.text_area("Transcript", transcript, height=150)

                with st.spinner("🧠 Analyzing sentiment..."):
                    analysis = analyze_sentiment(transcript)

                # --- Display Results ---
                st.markdown("## 📊 Analysis Results")
                
                # Sentiment Display
                sentiment = analysis["Sentiment"]
                score = analysis["Sentiment Score"]
                colors = {
                    "Positive": "#4CAF50",
                    "Negative": "#FF4B4B",
                    "Neutral": "#FFC107",
                    "Error": "#9E9E9E",
                    "No Speech": "#607D8B"
                }
                emoji = {
                    "Positive": "😃",
                    "Negative": "😡",
                    "Neutral": "😐",
                    "Error": "❌",
                    "No Speech": "🔇"
                }
                
                st.markdown(f"""
                    <div style="background-color: {colors[sentiment]}; 
                                color: white; 
                                padding: 1rem; 
                                border-radius: 10px;
                                text-align: center;
                                margin: 1rem 0;">
                        <h2>{emoji[sentiment]} {sentiment}</h2>
                        <h3>Score: {score:.2f}</h3>
                    </div>
                """, unsafe_allow_html=True)

                # Detailed Metrics
                cols = st.columns(2)
                with cols[0]:
                    st.markdown("### 🤔 Filler Words")
                    filler_count = analysis["Hesitation Count"]
                    st.metric("Total Fillers", filler_count)
                    if filler_count > 5:
                        st.error("Too many filler words! Practice speaking more deliberately.")
                    elif filler_count > 0:
                        st.warning("Moderate filler words detected. Try to reduce them.")
                    else:
                        st.success("Excellent speech clarity!")

                with cols[1]:
                    st.markdown("### 📚 Grammar Check")
                    issues = analysis["Grammar Issues"]
                    if issues:
                        st.error(f"Found {len(issues)} potential issues")
                        with st.expander("View Issues"):
                            for issue in issues:
                                st.warning(f"- {issue}")
                    else:
                        st.success("No significant grammar issues found!")

                # Final Recommendations
                st.markdown("## 🎯 Improvement Tips")
                if sentiment == "Negative":
                    st.error("""
                    **Improvement Needed:**  
                    - Practice positive language framing  
                    - Use more confident vocabulary  
                    - Record practice sessions for review
                    """)
                elif filler_count > 3:
                    st.warning("""
                    **Clarity Tips:**  
                    - Pause instead of using filler words  
                    - Practice with a metronome  
                    - Record and review your speech
                    """)
                else:
                    st.success("""
                    **Great Job!**  
                    - Maintain your speaking pace  
                    - Continue practicing regularly  
                    - Review advanced communication techniques
                    """)
else:
    st.warning("⚠️ Please upload a video file first!")

# --- Navigation ---

