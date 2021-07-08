
#                   SYNTHIA
#   The AI system to turn text into knowledge 

##########
#lIBRARIES
##########

import streamlit as st
import streamlit.components.v1 as components
from gensim.summarization import summarize
from googletrans import Translator
from nltk.tokenize import word_tokenize
import readtime
import textstat

########
#HEADER
#######

st.set_page_config(page_title="Synthia")

st.markdown("<h4 style='text-align: center; color:grey;'>Turn text into knowledge</h4>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: white;'>Summarize. Translate. Generate. Measure.</h1>", unsafe_allow_html=True)
st.write('')

"""
[![Star](https://img.shields.io/github/stars/dlopezyse/Synthia.svg?logo=github&style=social)](https://gitHub.com/dlopezyse/Synthia)
&nbsp[![Follow](https://img.shields.io/twitter/follow/lopezyse?style=social)](https://www.twitter.com/lopezyse)
"""

st.markdown('___')

#########
#SIDEBAR
########

st.sidebar.header('I want to:')
nav = st.sidebar.radio('',['Summarize text', 'Translate text', 'Generate text', 'Measure text'])
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')

#ABOUT
######
expander = st.sidebar.beta_expander('About')
expander.write("Learning happens best when content is personalized to meet our needs and strengths. For this reason I created SYNTHIA, the AI system to accelerate and design your knowledge. Interested? This site is just a demo of several other available functionalities. Want to learn more? [Let's connect!] (https://www.linkedin.com/in/lopezyse/)")

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
                        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-text="This is SYNTHIA, the AI that turns text into knowledge" data-url="https://share.streamlit.io/dlopezyse/synthia/main" data-hashtags="AI,Synthia" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        """,
                        )

#-----------------------------------------

#TRANSLATE
##########

if nav == 'Translate text':
    st.markdown("<h3 style='text-align: left; color:#F63366;'><b>Translate Text<b></h3>", unsafe_allow_html=True)
    st.text('')
    
    translator = Translator()
             
    input_tr = st.text_area("Write some text in English. Then scroll down to translate", max_chars=5000)

    languages = ['','Spanish', 'French', 'Deutsch']
    options = st.selectbox('Please select a language for translation', languages)

    if options =='Spanish':
        with st.spinner('Traduciendo...'):
            trans1 = translator.translate(input_tr, dest="es").text
            st.write(trans1)
    elif options =='French':
        with st.spinner('Traduire...'):
            trans2 = translator.translate(input_tr, dest='fr').text
            st.write(trans2)   
    elif options =='Deutsch':
        with st.spinner('Übersetzen...'):
            trans3 = translator.translate(input_tr, dest='de').text
            st.write(trans3)
 
    st.markdown('___') 
    
    components.html(
                        """
                        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-text="This is SYNTHIA, the AI that turns text into knowledge" data-url="https://share.streamlit.io/dlopezyse/synthia/main" data-hashtags="AI,Synthia" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        """,
                        )

#-----------------------------------------
    
#GENERATE
#########

if nav == 'Generate text':
    st.markdown("<h3 style='text-align: left; color:#F63366;'><b>Generate Text<b></h3>", unsafe_allow_html=True)
    st.text('')

    input_ge = st.text_area("Type in some content, and we will write something for you", max_chars=500, value="The future of humanity will depend on")

    if st.button('Create text'):
        if input_ge =='':
            st.error('Please enter a search term')
        else:
            with st.spinner('Wait for it...'):
                result = input_ge.title()
                from transformers import GPT2LMHeadModel, GPT2Tokenizer
                tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
                model = GPT2LMHeadModel.from_pretrained('gpt2')
                inputs = tokenizer.encode(result, return_tensors='pt')
                outputs = model.generate(inputs, max_length=200, do_sample=True)
                text = tokenizer.decode(outputs[0], skip_special_tokens=True)
                st.write(text)

    st.markdown('___') 
    
    components.html(
                        """
                        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-text="This is SYNTHIA, the AI that turns text into knowledge" data-url="https://share.streamlit.io/dlopezyse/synthia/main" data-hashtags="AI,Synthia" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        """,
                        )
        
#-----------------------------------------
     
#MEASURE
########
       
if nav == 'Measure text':
    st.markdown("<h3 style='text-align: left; color:#F63366;'><b>Measure Text<b></h3>", unsafe_allow_html=True)
    st.text('')

    input_me = st.text_area("Write some text in English (minimum = 500 characters). Then scroll down to analyze it", max_chars=5000)

    if st.button('Measure'):
        if input_me =='':
            st.error('Please enter some text')
        elif len(input_me) < 500:
            st.error('Please enter a larger text')
        else:
            with st.spinner('Wait for it...'):
                rt = readtime.of_text(input_me)
                tc = textstat.flesch_reading_ease(input_me)
                tokenized_words = word_tokenize(input_me)
                lr = len(set(tokenized_words)) / len(tokenized_words)
                lr = round(lr,2)
                st.text('Reading Time')
                st.write(rt)
                st.text('Text Complexity (0 = hard to read, 100 = easy to read)')
                st.write(tc)
                st.text('Lexical Richness (distinct words over total number of words)')
                st.write(lr)

    st.markdown('___') 
    
    components.html(
                        """
                        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-text="This is SYNTHIA, the AI that turns text into knowledge" data-url="https://share.streamlit.io/dlopezyse/synthia/main" data-hashtags="AI,Synthia" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        """,
                        )

####################################
