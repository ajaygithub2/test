import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase


# Define a custom VideoTransformer class to handle video frames
class WebcamVideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.width = None
        self.height = None

    def transform(self, frame):
        return frame

    def on_receive(self, frame):
        if self.width is None or self.height is None:
            self.width = frame.width
            self.height = frame.height
        return frame


# Streamlit app
def main():
    st.title("Webcam Video Feed")
    st.write("Use the button below to start the webcam video feed.")

    # Display video feed using webrtc_streamer
    webrtc_streamer(key="webcam", video_processor_factory=WebcamVideoTransformer())


if __name__ == "__main__":
    main()
