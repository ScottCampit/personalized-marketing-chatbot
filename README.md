# Personalized marketing using chatbot

## Key features to implement

The current version of the app uses streamlit for the front/backend to quickly iterate through ideas. Will develop front-end with JS and host on AWS or other platform later.

Code is found in `chatbot/bot.py`.

### 1. Upload targets' contact information

To upload a single CSV file, we can use the `st.file_uploader` method:

```{python}
uploaded_file = st.file_uploader(
    label="Upload a single CSV file containing your contacts' information.", 
    type='csv',
    accept_multiple_files=False
)
```

There is a quick catch, where an error is returned if the file type is not a CSV file.

```{python}
if uploaded_file is not None:
  try:
      df = pd.read_csv(uploaded_file)
  except:
      st.write("Wrong file type - please upload a csv.")
```

#### Current limitations and to dos

* Extend to Excel files and write tests to ensure it is working properly

### 2. Allow the marketing professional to specify the campaign they'd like to run

As a starting point, the professional can write in what the value proposition is as a text field. They can then select via radio buttons additional customizations to the email.

Note that this is a batch job - they need to fill out all fields before the AI begins to work.

```{python}
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
```

#### Current limitations and to dos

* Need to see from users if they'd like more flexibility in options
* Edit fields so that instead of radio buttons they are more attractive from UI/UX perspective

### 3. Develop an AI that generates email copy based on the professional's inputs

Now that we have a way of capturing inputs, we need to generate outputs 

```{python}
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
```

#### Current limitations and to dos

* Additional prompt engineering
  * Provide users with options for different prompts?
  * Need to figure out way to increase token length
* Play around with models
  * Hyperparameter tuning
  * Try out different model architectures if open-source (e.g. LaMBDA)

## To do

- [ ] Provide a variance score for each email to inform the user which email copies should be reviewed, given a high degree of variance
- [ ] Initiate campaign by:
 - [ ] Copy and pasting into email client
 - [ ] Sending emails directly from platform
 - [ ] Sending emails directly from their own email client
 - [ ] Sending emails directly from their ppreferred marketing solution
- [ ] AI can create cohorts for A/B testing and refine email copies for pending contacts and future campaigns
- [ ] Statistics:
 - [ ] Open rates
 - [ ] CTR rates