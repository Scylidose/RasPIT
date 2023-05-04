import openai
from config import OPENAI_API_KEY

# Set up the OpenAI API key
openai.api_key = OPENAI_API_KEY

def generate_response(prompt, model="text-davinci-002", max_tokens=150, n=1, stop=None, temperature=0.5):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature,
    )

    if n == 1:
        return response.choices[0].text.strip()
    else:
        return [choice.text.strip() for choice in response.choices]
