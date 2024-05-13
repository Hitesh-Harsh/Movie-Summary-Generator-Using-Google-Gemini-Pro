import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import os
import srt  # Import srt library for parsing SRT files

# Load environment variables
load_dotenv()

# Configure GenerativeAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for the GenerativeAI model
prompt = "You are a Youtube Video Summarizer. You will be taking the transcript text and summarizing the entire video and providing the important summary points in 250 Words in English. The Transcript text will be appended here"

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

def parse_srt_file(uploaded_file):
    # Parse the uploaded SRT file
    try:
        content = uploaded_file.getvalue().decode("utf-8")
        subtitles = list(srt.parse(content))
        return subtitles
    except Exception as e:
        st.error(f"Error parsing SRT file: {e}")
        return None

def main():
    st.image("pexels-tima-miroshnichenko-5662857.jpg", caption="Image Caption", width=1000, use_column_width=True)
    st.title("YouTube Transcript to Detailed Notes Converter")
    uploaded_file = st.file_uploader("Upload an SRT file", type="srt")

    if uploaded_file is not None:
        # Parse the SRT file
        subtitles = parse_srt_file(uploaded_file)
        if subtitles is not None:
            st.success("SRT file parsed successfully!")
            # Convert subtitles to plain text
            transcript_text = "\n".join([subtitle.content for subtitle in subtitles])
            # Save transcript text to a text file
            with open("transcript.txt", "w", encoding="utf-8") as text_file:
                text_file.write(transcript_text)
            st.success("Transcript text saved to transcript.txt file!")
            # Generate detailed notes using GenerativeAI
            if st.button("Get Detailed Notes"):
                summary = generate_gemini_content(transcript_text, prompt)
                st.markdown("## Detailed Notes:")
                st.write(summary)

if __name__ == "__main__":
    main()
