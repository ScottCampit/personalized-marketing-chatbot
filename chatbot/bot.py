"""
Fine-tune GPT models
"""

import os
import openai
import streamlit as st
import pandas as pd
import time

openai.api_key = os.environ["OPENAI_API_KEY"]
pd.set_option('display.max_colwidth', None)

# Chat GPT 
def generate_response(prompt:str, temperature:float=0.1, max_tokens:int=2049, engine='text-davinci-003'):
    """
    Uses OpenAI API to generate response from a prompt. Prompt structure is currently fixed.
    """
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0.3,
        presence_penalty=0.3
    )
    generated_text = response["choices"][0]["text"]
    return generated_text

@st.cache
def cache_df(df):
    return df.to_csv().encode('utf-8')

if __name__ == "__main__":
    df = pd.DataFrame()
    # Upload Excel or CSV file
    st.title("NewCo Application")
    uploaded_file = st.file_uploader(
        label="Upload a single CSV file containing your contacts' information.", 
        type='csv',
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except:
            st.write("Wrong file type - please upload a csv.")
            
    # Create Form
    with st.form(key='my_form'):
        value_prop = st.text_area(
            label="What is your product's value proposition?",
            value="Our product is going to change the world because of X, Y, and Z."
        )
        contact_list_type = st.radio(
            label="New or existing customers?",
            options=("New", "Existing")
        )
        email_tone = st.radio(
            label="What is the tone?",
            options=("Formal", "Neutral", "Causual")
        )
        creative_conservative = st.radio(
            label="How creative versus conservative would you want to be?",
            options=("Creative", "Conservative")
        )
        st.write('Press submit to generate personalized emails.')
        submit_button = st.form_submit_button(label='Submit')

    is_done = False
    df['prompt'] = ''
    df['response'] = ''
    if submit_button:
        st.write("Generating emails!")
        all_prompts = list()
        all_responses = list()
        bar = st.progress(0)
        for idx, row in df.iterrows():
            bar.progress(idx+1)
            prompt = f"""
                Write a {email_tone}, {creative_conservative} email to {row['Name']}, {row['Title']} who is a 
                {contact_list_type} customer from {row['Company']} in {row['Location']}. 
                Incorporate details like {row['Fictional fun fact from data source']}. Product: {value_prop},"""
            response = generate_response(prompt)
            all_prompts.append(prompt)
            all_responses.append(response)
            df.loc[idx]['prompt'] = prompt
            df.loc[idx]['response'] = response
        
    is_done = True
    st.write("Finished!")
    
    if is_done:
        st.download_button(
            label="Download data as CSV",
            data=cache_df(df),
            file_name='test.csv'
        )


