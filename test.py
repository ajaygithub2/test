import streamlit as st
import av
import numpy as np
import streamlit_webrtc as webrtc

def main():
    st.title("Webcam Live Feed")
    webrtc_streamer()

def webrtc_streamer():
    webrtc_ctx = webrtc.Streamer(
        video_transformer_factory=None,
        bundle_errors=True,
        key="example",
        mode=WebRtcMode.SENDRECV,
    )
    if not webrtc_ctx.video_transformer:
        webrtc_ctx.video_transformer = VideoTransformer()
    while True:
        try:
            video_frame = webrtc_ctx.video_transformer.recv()
            if video_frame is None:
                continue
            webrtc_ctx.send_video_frame(video_frame)
        except (av.AVError, StopIteration):
            break

class VideoTransformer(webrtc.VideoTransformerBase):
    def __init__(self):
        self.threshold = 0.5

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        return img

if __name__ == "__main__":
    main()
