from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import av
import cv2
import threading
import streamlit_webrtc as sw
import playsound
import streamlit as st
from PIL import Image
image = Image.open('fire-alarm.png')

st.image(image,width=100)

with open( "style.css" ) as css:
        st.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)
        
        st.markdown('<h1 class="heading">Fire Alarm System</h1>', unsafe_allow_html=True)    
       

cascade =cv2.CascadeClassifier("fire_detection.xml")
class VideoProcessor:
  
    def recv(self, frame):
        if st.button("Turn off audio"):
            sw.off(frame)
        def play_alarm():
            playsound.playsound('alarm_beeps.mp3',True)
        
        frm = frame.to_ndarray(format="bgr24")
        fire = cascade.detectMultiScale(cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY),  1.2, 5)
        for x,y,w,h in fire:
            cv2.rectangle(frm, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 2)
            if w > 120 and h>120:
                 cv2.putText(frm, "high intensity", (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            elif w<100 and h< 100:
                  cv2.putText(frm, "low intensity", (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            else:
                 cv2.putText(frm, "small flame", (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0),2)
            threading.Thread(target=play_alarm).start()
            st.write("Fire Detected")
            
        return av.VideoFrame.from_ndarray(frm, format='bgr24')

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)
webrtc_streamer(key="key", video_processor_factory=VideoProcessor,
				rtc_configuration=RTCConfiguration(
					{"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
					),media_stream_constraints={"video": True, "audio": False},
	)