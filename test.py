import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer, WebRtcMode
from PIL import Image
import numpy as np

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
        video_transformer_factory=WebcamTransformer,
    )

    # Display the video feed and captured frames
    if webrtc_ctx.video_transformer and webrtc_ctx.video_transformer.frame is not None:
        # Convert the RGB frame to PIL Image
        pil_image = Image.fromarray(np.uint8(webrtc_ctx.video_transformer.frame))

        # Display the PIL Image in Streamlit
        st.image(pil_image, channels="RGB", use_column_width=True)


if __name__ == "__main__":
    app()
