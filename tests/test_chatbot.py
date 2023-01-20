import os
import openai
import pandas as pd
import argparse
import json

openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_response(prompt:str, temperature:float=0.3, max_tokens:int=4000, engine:str='text-davinci-003'):
    """
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--customer_csv', default='/mnt/c/Users/owner/Data/personalized_marketing/test_data.csv')
    
    parser.add_argument('--temperature', default=0.3)
    parser.add_argument('--max_tokens', default=4000)
    parser.add_argument('--engine', default='text-davinci-003')

    parser.add_argument('--value_prop', default='Poop Inc. sells gold-leaf toilet paper to the uber wealthy.')
    parser.add_argument('--contact_list_type', default='New')
    parser.add_argument('--email_tone', default='Formal')
    parser.add_argument('--creative_conservative', default='Creative')

    parser.add_argument('--output_json', default='/mnt/c/Users/owner/Data/personalized_marketing/test_results.json')

    args = parser.parse_args()

    df = pd.read_csv(args.customer_csv)

    
    results = {}
    results['engine'] = args.engine
    results['temperature'] = args.temperature
    for idx, row in df.iterrows():
        prompt = f"""
        Write a {args.email_tone}, {args.creative_conservative} email to {row['Name']}, {row['Title']} who is a 
        {args.contact_list_type} customer from {row['Company']} in {row['Location']}. 
        Incorporate details like {row['Fictional fun fact from data source']}. Product: {args.value_prop},"""
        response = generate_response(prompt, args.temperature, args.max_tokens, args.engine)

        #print(f'Prompt: {prompt}')
        #print(f'Response: {response}')
        results[prompt] = response

    with open('/mnt/c/Users/owner/Data/personalized_marketing/test_results.json', 'w') as f:
        json.dump(results, f)
    


    
    

