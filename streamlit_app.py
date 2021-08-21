
#                   SYNTHIA
#   The AI system to turn words into knowledge 

##########
#LIBRARIES
##########

import streamlit as st
import streamlit.components.v1 as components
from gensim.summarization import summarize
from googletrans import Translator
import nltk
from nltk.tokenize import word_tokenize
import readtime
import textstat
import queue
import threading
import time
import urllib.request
from collections import deque
from pathlib import Path
from typing import List
import av
import numpy as np
import pydub
from streamlit_webrtc import (
    AudioProcessorBase,
    ClientSettings,
    WebRtcMode,
    webrtc_streamer,
)


HERE = Path(__file__).parent

# This code is based on https://github.com/streamlit/demo-self-driving/blob/230245391f2dda0cb464008195a470751c01770b/streamlit_app.py#L48  # noqa: E501
def download_file(url, download_to: Path, expected_size=None):
    # Don't download the file twice.
    # (If possible, verify the download using the file length.)
    if download_to.exists():
        if expected_size:
            if download_to.stat().st_size == expected_size:
                return
        else:
            st.info(f"{url} is already downloaded.")
            if not st.button("Download again?"):
                return

    download_to.parent.mkdir(parents=True, exist_ok=True)

    # These are handles to two visual elements to animate.
    weights_warning, progress_bar = None, None
    try:
        weights_warning = st.warning("Downloading %s..." % url)
        progress_bar = st.progress(0)
        with open(download_to, "wb") as output_file:
            with urllib.request.urlopen(url) as response:
                length = int(response.info()["Content-Length"])
                counter = 0.0
                MEGABYTES = 2.0 ** 20.0
                while True:
                    data = response.read(8192)
                    if not data:
                        break
                    counter += len(data)
                    output_file.write(data)

                    # We perform animation by overwriting the elements.
                    weights_warning.warning(
                        "Downloading %s... (%6.2f/%6.2f MB)"
                        % (url, counter / MEGABYTES, length / MEGABYTES)
                    )
                    progress_bar.progress(min(counter / length, 1.0))
    # Finally, we remove these visual elements by calling .empty().
    finally:
        if weights_warning is not None:
            weights_warning.empty()
        if progress_bar is not None:
            progress_bar.empty()

########
#HEADER
#######

st.set_page_config(page_title="Synthia")

st.markdown("<h4 style='text-align: center; color:grey;'>Turn words into knowledge</h4>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: white;'>Summarize. Paraphrase. Measure.</h1>", unsafe_allow_html=True)
st.write('')

"""
[![Star](https://img.shields.io/github/stars/dlopezyse/Synthia.svg?logo=github&style=social)](https://gitHub.com/dlopezyse/Synthia)
&nbsp[![Follow](https://img.shields.io/twitter/follow/lopezyse?style=social)](https://www.twitter.com/lopezyse)
"""
st.write('')
st.write(':point_left: Use the menu at left to select your task (click on > if closed).')

st.markdown('___')

#########
#SIDEBAR
########

st.sidebar.header('I want to :bulb:')
nav = st.sidebar.radio('',['Summarize text', 'Paraphrase text', 'Measure text', 'Speech to Text'])
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')

#ABOUT
######
expander = st.sidebar.expander('About')
expander.write("Learning happens best when content is personalized to meet our needs and strengths. For this reason I created SYNTHIA :robot_face:, the AI system to accelerate and design your knowledge in seconds (this site is only a demo of several other functionalities). I'd love your feedback on this :smiley:, so if you want to reach out you can find me on [LinkedIn] (https://www.linkedin.com/in/lopezyse/) and [Twitter] (https://twitter.com/lopezyse)")


#######
#PAGES
######

#SUMMARIZE
##########

if nav == 'Summarize text':
    st.markdown("<h3 style='text-align: left; color:#F63366;'><b>Summarize Text<b></h3>", unsafe_allow_html=True)
    st.text('')
    
    input_su = st.text_area("Write some text or copy & paste so we can summarize it (minimum = 1000 characters)", max_chars=5000)

    if st.button('Summarize'):
        if input_su =='':
            st.error('Please enter some text')
        elif len(input_su) < 1000:
            st.error('Please enter a larger text')
        else:
            with st.spinner('Wait for it...'):
                st.success(summarize(input_su, word_count=50, ratio=0.05))

    st.markdown('___')

    components.html(
                        """
                        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-text="This is SYNTHIA, the AI that turns words into knowledge via @lopezyse" data-url="https://share.streamlit.io/dlopezyse/synthia/main" data-hashtags="AI,Education,MachineLearning,Synthia" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        """,
                        )

#-----------------------------------------

#PARAPHRASE
###########

if nav == 'Paraphrase text':
    st.markdown("<h3 style='text-align: left; color:#F63366;'><b>Paraphrase Text<b></h3>", unsafe_allow_html=True)
    st.text('')
    
    input_pa = st.text_area("Write some text or copy & paste so we can paraphrase it", max_chars=5000)

    if st.button('Paraphrase'):
        if input_pa =='':
            st.error('Please enter some text')
        else:
            with st.spinner('Wait for it...'):
                translator = Translator()
                mid = translator.translate(input_pa, dest="fr").text
                mid2 = translator.translate(mid, dest="de").text
                back = translator.translate(mid2, dest="en").text
                st.write(back)

    st.markdown('___')

    components.html(
                        """
                        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-text="This is SYNTHIA, the AI that turns words into knowledge via @lopezyse" data-url="https://share.streamlit.io/dlopezyse/synthia/main" data-hashtags="AI,Education,MachineLearning,Synthia" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        """,
                        )

#-----------------------------------------
   
#MEASURE
########
       
if nav == 'Measure text':
    st.markdown("<h3 style='text-align: left; color:#F63366;'><b>Measure Text<b></h3>", unsafe_allow_html=True)
    st.text('')

    input_me = st.text_area("Input some text in English, and scroll down to analyze it", max_chars=5000)

    if st.button('Measure'):
        if input_me =='':
            st.error('Please enter some text')
        elif len(input_me) < 500:
            st.error('Please enter a larger text')
        else:
            with st.spinner('Wait for it...'):
                nltk.download('punkt')
                rt = readtime.of_text(input_me)
                tc = textstat.flesch_reading_ease(input_me)
                tokenized_words = word_tokenize(input_me)
                lr = len(set(tokenized_words)) / len(tokenized_words)
                lr = round(lr,2)
                st.text('Reading Time')
                st.write(rt)
                st.text('Text Complexity (score from 0 (hard to read), to 100 (easy to read))')
                st.write(tc)
                st.text('Lexical Richness (distinct words over total number of words)')
                st.write(lr)

    st.markdown('___') 
    
    components.html(
                        """
                        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-text="This is SYNTHIA, the AI that turns words into knowledge via @lopezyse" data-url="https://share.streamlit.io/dlopezyse/synthia/main" data-hashtags="AI,Education,MachineLearning,Synthia" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        """,
                        )

#-----------------------------------------
   
#SPEECH-TO-TEXT
########

def app_sst(model_path: str, lm_path: str, lm_alpha: float, lm_beta: float, beam: int):
    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        client_settings=ClientSettings(
            rtc_configuration={
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
            },
            media_stream_constraints={"video": False, "audio": True},
        ),
    )

    status_indicator = st.empty()

    if not webrtc_ctx.state.playing:
        return

    status_indicator.write("Loading...")
    text_output = st.empty()
    stream = None

    while True:
        if webrtc_ctx.audio_receiver:
            if stream is None:
                from deepspeech import Model

                model = Model(model_path)
                model.enableExternalScorer(lm_path)
                model.setScorerAlphaBeta(lm_alpha, lm_beta)
                model.setBeamWidth(beam)

                stream = model.createStream()

                status_indicator.write("Model loaded.")

            sound_chunk = pydub.AudioSegment.empty()
            try:
                audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
            except queue.Empty:
                time.sleep(0.1)
                status_indicator.write("No frame arrived.")
                continue

            status_indicator.write("Running. Say something!")

            for audio_frame in audio_frames:
                sound = pydub.AudioSegment(
                    data=audio_frame.to_ndarray().tobytes(),
                    sample_width=audio_frame.format.bytes,
                    frame_rate=audio_frame.sample_rate,
                    channels=len(audio_frame.layout.channels),
                )
                sound_chunk += sound

            if len(sound_chunk) > 0:
                sound_chunk = sound_chunk.set_channels(1).set_frame_rate(
                    model.sampleRate()
                )
                buffer = np.array(sound_chunk.get_array_of_samples())
                stream.feedAudioContent(buffer)
                text = stream.intermediateDecode()
                text_output.markdown(f"**Text:** {text}")
        else:
            status_indicator.write("AudioReciver is not set. Abort.")
            break

if nav == 'Speech to Text':
    st.markdown("<h3 style='text-align: left; color:#F63366;'><b>Speech to Text<b></h3>", unsafe_allow_html=True)
    st.text('')
	st.markdown("This demo app is using [DeepSpeech](https://github.com/mozilla/DeepSpeech), an open speech-to-text engine. A pre-trained model released with [v0.9.3](https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3), trained on American English is being served.")
	MODEL_URL = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm"
	LANG_MODEL_URL = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer"
	MODEL_LOCAL_PATH = HERE / "models/deepspeech-0.9.3-models.pbmm"
	LANG_MODEL_LOCAL_PATH = HERE / "models/deepspeech-0.9.3-models.scorer"

	download_file(MODEL_URL, MODEL_LOCAL_PATH, expected_size=188915987)
	download_file(LANG_MODEL_URL, LANG_MODEL_LOCAL_PATH, expected_size=953363776)
	lm_alpha = 0.931289039105002
	lm_beta = 1.1834137581510284
	beam = 100
	sound_only_page = "Speak Up"
	app_mode = st.selectbox("Choose the app mode", [sound_only_page])
	if app_mode == sound_only_page:
		app_sst(
    		str(MODEL_LOCAL_PATH), str(LANG_MODEL_LOCAL_PATH), lm_alpha, lm_beta, beam
        )

####################################

