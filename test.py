import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer, WebRtcMode
from PIL import Image
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    static_image_mode=False
)

# Create a custom video transformer by inheriting from VideoTransformerBase
class WebcamTransformer(VideoTransformerBase):
    def __init__(self):
        self.frame = None

    # Override the transform method to process each video frame
    def transform(self, frame):
        self.frame = frame.to_ndarray(format="rgb24")  # Convert the frame to a numpy array

        # Process the frame using mediapipe
        results = hands.process(self.frame)
        landmarks = results.multi_hand_landmarks

        # Extract hand information from the processed frame
        self.side = None
        self.surity = None
        try:
            if landmarks is None:
                self.side = "No Hands in frame"
                self.surity = "Pretty sure"
            elif len(landmarks) == 1:
                self.surity = f"{float(str(results.multi_handedness[0].classification[0])[16:20]) * 100}%"
                if "Left" in str(results.multi_handedness[0].classification[0]):
                    self.side = "Left"
                elif "Right" in str(results.multi_handedness[0].classification[0]):
                    self.side = "Right"
            elif len(landmarks) > 1:
                self.surity = f"{(float(str(results.multi_handedness[0].classification[0])[16:20])*50) + (float(str(results.multi_handedness[1].classification[0])[16:20])*50)}%"
                self.side = "Both"
        except:
            pass

        # Return the processed frame, side, and surity
        return self.frame, self.side, self.surity

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

        # Display the hand information as text on the Streamlit page
        print(f"Side: {webrtc_ctx.video_transformer.side}")
        print(f"Surity: {webrtc_ctx.video_transformer.surity}")


if __name__ == "__main__":
    app()
