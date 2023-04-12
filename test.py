import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer, WebRtcMode

# Create a custom video transformer by inheriting from VideoTransformerBase
class WebcamTransformer(VideoTransformerBase):
    def __init__(self):
        self.frame = None

    # Override the transform method to process each video frame
    def transform(self, frame):
        self.frame = frame.to_ndarray(format="rgb24")  # Convert the frame to a numpy array

        # Return the processed frame, side, and surity
        return self.frame

    # Override the emit method to return the processed frame
    def emit(self):
        return self.frame

# Create a Streamlit app
def app():
    st.title("Webcam Feed")

    # Use the webrtc_streamer function to capture video from the webcam
    webrtc_ctx = webrtc_streamer(
        key="webcam",
        mode=WebRtcMode.SENDRECV,  # Specify the mode as SENDRECV
        video_processor_factory=WebcamTransformer,
    )


if __name__ == "__main__":
    app()
