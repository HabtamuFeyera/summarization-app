import streamlit as st
import requests
from datetime import datetime

# App title
st.title("Multithreaded Summarization API")

# Input fields
text = st.text_area("Enter text to summarize:")
threads = st.number_input("Number of threads", min_value=1, max_value=10, value=1)

# Button to submit request
if st.button("Summarize"):
    if text.strip():
        st.info("Sending request to API...")
        start_time = datetime.now()

        # Send request to backend API
        response = requests.post(
            "http://127.0.0.1:8000/summarize",
            json={"text": text, "threads": threads}
        )

        end_time = datetime.now()

        if response.status_code == 200:
            data = response.json()
            summaries = data.get("summaries", [])
            processing_time = data.get("processing_time", 0)

            st.success(f"Processed in {processing_time} seconds")
            for idx, summary in enumerate(summaries):
                st.write(f"Summary {idx + 1}: {summary}")
        else:
            st.error(f"API Error: {response.text}")
        
        st.write(f"Request time: {end_time - start_time}")
    else:
        st.warning("Please enter text!")
