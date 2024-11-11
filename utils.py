from openai import OpenAI
import datetime
import variables

def dateTimeFormat():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
    dateNow = f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
    return dateNow

def aiApi(user_prompt):
    baseUrl = "https://api.aimlapi.com/v1"
    apiKey = variables.API_KEY
    systemPrompt = "You are admin of the rpg game. You can make anything. You can make infinity all of things. Just give the gist, no other explanation needed"
    userPrompt = user_prompt

    api = OpenAI(api_key=apiKey, base_url=baseUrl)
    
    completion = api.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": userPrompt},
        ],
        temperature=0.7,
        max_tokens=100,
    )

    response = completion.choices[0].message.content
    
    return response