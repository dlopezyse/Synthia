
#                   SYNTHIA
#   The AI system to accelerate knowledge 

##########
#LIBRARIES
##########

import streamlit as st
import time
from gensim.summarization import summarize
from googletrans import Translator
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import readtime
import textstat
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from io import StringIO
from textattack.augmentation import EmbeddingAugmenter
from textattack.augmentation import WordNetAugmenter
import speech_recognition as sr

###################
#PAGE CONFIGURATION
###################

st.set_page_config(page_title="SYNTHIA", page_icon=":robot_face:")

#########
#SIDEBAR
########

st.sidebar.header('SYNTHIA, I want to :crystal_ball:')
nav = st.sidebar.radio('',['Go to homepage', 'Summarize text', 'Paraphrase text', 'Analyze text'])
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')

#CONTACT
########
expander = st.sidebar.expander('Contact')
expander.write("I'd love your feedback :smiley: Want to collaborate? Develop a project? Find me on [LinkedIn] (https://www.linkedin.com/in/lopezyse/), [Twitter] (https://twitter.com/lopezyse) and [Medium] (https://lopezyse.medium.com/)")

#######
#PAGES
######

#HOME
#####

if nav == 'Go to homepage':

    st.markdown("<h1 style='text-align: center; color: white; font-size:28px;'>Welcome to SYNTHIA!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-size:56px;'<p>&#129302;</p></h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey; font-size:20px;'>Summarize, paraphrase, analyze text & more. Try our models, browse their source code, and share with the world!</h3>", unsafe_allow_html=True)
    """
    [![Star](https://img.shields.io/github/stars/dlopezyse/Synthia.svg?logo=github&style=social)](https://gitHub.com/dlopezyse/Synthia)
    &nbsp[![Follow](https://img.shields.io/twitter/follow/lopezyse?style=social)](https://www.twitter.com/lopezyse)
    &nbsp[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee--yellow.svg?logo=buy-me-a-coffee&logoColor=orange&style=social)](https://www.buymeacoffee.com/lopezyse)
    """
    st.markdown('___')
    st.write(':point_left: Use the menu at left to select a task (click on > if closed).')
    st.markdown('___')
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:18px;'><b>What is this App about?<b></h3>", unsafe_allow_html=True)
    st.write("Learning happens best when content is personalized to meet our needs and strengths.")
    st.write("For this reason I created SYNTHIA :robot_face:, the AI system to accelerate and design your knowledge in seconds! Use this App to summarize and simplify content. Paste your text or upload your file and you're done. We'll process it for you!")     
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:18px;'><b>Who is this App for?<b></h3>", unsafe_allow_html=True)
    st.write("Anyone can use this App completely for free! If you like it, please share it :+1: ")
    st.write("Are you into NLP? Our code is 100% open source and written for easy understanding. Fork it from [GitHub] (https://github.com/dlopezyse/Synthia), and pull any suggestions you may have. Become part of the community! Help yourself and help others :smiley:")

#-----------------------------------------

#SUMMARIZE
##########

if nav == 'Summarize text':
    st.markdown("<h4 style='text-align: center; color:grey;'>Accelerate knowledge with SYNTHIA &#129302;</h4>", unsafe_allow_html=True)
    st.text('')
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:28px;'><b>Summarize text<b></h3>", unsafe_allow_html=True)
    st.text('')

    source = st.radio("How would you like to start? Choose an option below",
                          ("I want to input some text", "I want to upload a file"))
    st.text('')

    if source == 'I want to input some text':
        input_su = st.text_area("Write or paste your text in English (between 1,000 and 10,000 characters)", max_chars=10000)
        if st.button('Summarize'):
            if len(input_su) < 1000:
                st.error('Please enter a text in English of minimum 1,000 characters')
            else:
                with st.spinner('Processing...'):
                    time.sleep(2)
                    t_r = summarize(input_su, word_count=50, ratio=0.05)
                    result_t_r = (str(len(t_r)) + ' characters' + ' ('"{:.0%}".format(len(t_r)/len(input_su)) + ' of original content)')
                    st.markdown('___')
                    st.write('TextRank Model')
                    st.caption(result_t_r)
                    st.success(t_r) 
                    text = input_su
                    stopWords = set(stopwords.words("english"))
                    words = word_tokenize(text)
                    freqTable = dict()
                    for word in words:
                        word = word.lower()
                        if word in stopWords:
                            continue
                        if word in freqTable:
                            freqTable[word] += 1
                        else:
                            freqTable[word] = 1
                    sentences = sent_tokenize(text)
                    sentenceValue = dict()
                    for sentence in sentences:
                        for word, freq in freqTable.items():
                            if word in sentence.lower():
                                if sentence in sentenceValue:
                                    sentenceValue[sentence] += freq
                                else:
                                    sentenceValue[sentence] = freq
                    sumValues = 0
                    for sentence in sentenceValue:
                        sumValues += sentenceValue[sentence]  
                    average = int(sumValues / len(sentenceValue))
                    summary = ''
                    for sentence in sentences:
                        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.3 * average)):
                            summary += " " + sentence
                    s_m = summary
                    result_s_m = (str(len(s_m)) + ' characters' + ' ('"{:.0%}".format(len(s_m)/len(input_su)) + ' of original content)')
                    st.markdown('___')
                    st.write('Scoring Model')
                    st.caption(result_s_m)
                    st.success(s_m)
                    my_parser = PlaintextParser.from_string(input_su,Tokenizer('english'))
                    lex_rank_summarizer = LexRankSummarizer()
                    lexrank_summary = lex_rank_summarizer(my_parser.document,sentences_count=3)
                    summa = ''
                    for sentence in lexrank_summary:
                            summa = summa + str(sentence)
                    l_r = summa
                    result_l_r = (str(len(l_r)) + ' characters' + ' ('"{:.0%}".format(len(l_r)/len(input_su)) + ' of original content)')
                    st.markdown('___')
                    st.write('LexRank Model')
                    st.caption(result_l_r)
                    st.success(l_r)
                    st.balloons()

    if source == 'I want to upload a file':
        file = st.file_uploader('Upload your file here',type=['txt'])
        if file is not None:
            with st.spinner('Processing...'):
                    time.sleep(2)
                    stringio = StringIO(file.getvalue().decode("utf-8"))
                    string_data = stringio.read()
                    if len(string_data) < 1000 or len(string_data) > 10000:
                        st.error('Please upload a file between 1,000 and 10,000 characters')
                    else:
                        t_r = summarize(string_data, word_count=50, ratio=0.05)
                        result_t_r = (str(len(t_r)) + ' characters' + ' ('"{:.0%}".format(len(t_r)/len(string_data)) + ' of original content)')
                        st.markdown('___')
                        st.write('TextRank Model')
                        st.caption(result_t_r)
                        st.success(t_r) 
                        text = string_data
                        stopWords = set(stopwords.words("english"))
                        words = word_tokenize(text)
                        freqTable = dict()
                        for word in words:
                            word = word.lower()
                            if word in stopWords:
                                continue
                            if word in freqTable:
                                freqTable[word] += 1
                            else:
                                freqTable[word] = 1
                        # Creating a dictionary to keep the score of each sentence
                        sentences = sent_tokenize(text)
                        sentenceValue = dict()
                        for sentence in sentences:
                            for word, freq in freqTable.items():
                                if word in sentence.lower():
                                    if sentence in sentenceValue:
                                        sentenceValue[sentence] += freq
                                    else:
                                        sentenceValue[sentence] = freq
                        sumValues = 0
                        for sentence in sentenceValue:
                            sumValues += sentenceValue[sentence]  
                        average = int(sumValues / len(sentenceValue))
                        summary = ''
                        for sentence in sentences:
                            if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.3 * average)):
                                summary += " " + sentence
                        s_m = summary
                        result_s_m = (str(len(s_m)) + ' characters' + ' ('"{:.0%}".format(len(s_m)/len(string_data)) + ' of original content)')
                        st.markdown('___')
                        st.write('Scoring Model')
                        st.caption(result_s_m)
                        st.success(s_m)
                        my_parser = PlaintextParser.from_string(string_data,Tokenizer('english'))
                        lex_rank_summarizer = LexRankSummarizer()
                        lexrank_summary = lex_rank_summarizer(my_parser.document,sentences_count=3)
                        summa = ''
                        for sentence in lexrank_summary:
                                summa = summa + str(sentence)
                        l_r = summa
                        result_l_r = (str(len(l_r)) + ' characters' + ' ('"{:.0%}".format(len(l_r)/len(string_data)) + ' of original content)')
                        st.markdown('___')
                        st.write('LexRank Model')
                        st.caption(result_l_r)
                        st.success(l_r)
                        st.balloons()

#-----------------------------------------

#PARAPHRASE
###########

if nav == 'Paraphrase text':
    st.markdown("<h4 style='text-align: center; color:grey;'>Accelerate knowledge with SYNTHIA &#129302;</h4>", unsafe_allow_html=True)
    st.text('')
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:28px;'><b>Paraphrase text<b></h3>", unsafe_allow_html=True)
    st.text('')
    
    input_pa = st.text_area("Write or paste your text in English (maximum 500 characters)", max_chars=500)

    if st.button('Paraphrase'):
        if input_pa =='':
            st.error('Please enter some text')
        else:
            with st.spinner('Wait for it...'):
                    time.sleep(2)
                    translator = Translator()
                    mid = translator.translate(input_pa, dest="fr").text
                    mid2 = translator.translate(mid, dest="de").text
                    back = translator.translate(mid2, dest="en").text
                    st.markdown('___')
                    st.write('Back Translation Model')
                    st.success(back)
                    e_augmenter = EmbeddingAugmenter(transformations_per_example=1, pct_words_to_swap=0.3)
                    e_a = e_augmenter.augment(input_pa)
                    st.markdown('___')
                    st.write('Embedding Augmenter Model')
                    st.success(e_a)
                    w_augmenter = WordNetAugmenter(transformations_per_example=1, pct_words_to_swap=0.3)
                    w_a = w_augmenter.augment(input_pa)
                    st.markdown('___')
                    st.write('WordNet Augmenter Model')
                    st.success(w_a)
                    st.balloons()

#-----------------------------------------
   
#ANALYZE
########
       
if nav == 'Analyze text':
    st.markdown("<h4 style='text-align: center; color:grey;'>Accelerate knowledge with SYNTHIA &#129302;</h4>", unsafe_allow_html=True)
    st.text('')
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:28px;'><b>Analyze text<b></h3>", unsafe_allow_html=True)
    st.text('')
    
    source = st.radio("How would you like to start? Choose an option below",
                          ("I want to input some text", "I want to upload a file"))
    st.text('')

    if source == 'I want to input some text':
        input_me = st.text_area("Write or paste your text in English (maximum of 10,000 characters)", max_chars=10000)
        if st.button('Analyze'):
            if len(input_me) > 10000:
                st.error('Please enter a text in English of maximum 1,000 characters')
            else:
                with st.spinner('Processing...'):
                    time.sleep(2)
                    nltk.download('punkt')
                    rt = readtime.of_text(input_me)
                    tc = textstat.flesch_reading_ease(input_me)
                    tokenized_words = word_tokenize(input_me)
                    lr = len(set(tokenized_words)) / len(tokenized_words)
                    lr = round(lr,2)
                    st.markdown('___')
                    st.text('Reading Time')
                    st.write(rt)
                    st.markdown('___')
                    st.text('Text Complexity: from 0 or negative (hard to read), to 100 or more (easy to read)')
                    st.write(tc)
                    st.markdown('___')
                    st.text('Lexical Richness (distinct words over total number of words)')
                    st.write(lr)
                    st.balloons()

    if source == 'I want to upload a file':
        file = st.file_uploader('Upload your file here',type=['txt'])
        if file is not None:
            with st.spinner('Processing...'):
                    time.sleep(2)
                    stringio = StringIO(file.getvalue().decode("utf-8"))
                    string_data = stringio.read()
                    if len(string_data) > 10000:
                        st.error('Please upload a file of maximum 10,000 characters')
                    else:
                        nltk.download('punkt')
                        rt = readtime.of_text(string_data)
                        tc = textstat.flesch_reading_ease(string_data)
                        tokenized_words = word_tokenize(string_data)
                        lr = len(set(tokenized_words)) / len(tokenized_words)
                        lr = round(lr,2)
                        st.markdown('___')
                        st.text('Reading Time')
                        st.write(rt)
                        st.markdown('___')
                        st.text('Text Complexity: from 0 (hard to read), to 100 (easy to read)')
                        st.write(tc)
                        st.markdown('___')
                        st.text('Lexical Richness (distinct words over total number of words)')
                        st.write(lr)
                        st.balloons()

#-----------------------------------------
