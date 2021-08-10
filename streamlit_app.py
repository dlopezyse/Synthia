
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
nav = st.sidebar.radio('',['Summarize text', 'Paraphrase text', 'Measure text'])
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

####################################
