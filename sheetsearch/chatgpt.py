from openai import OpenAI
from sheetsearch import config


def query(prompt: str):
    '''
    openai.api_key = config.OPENAI_API_KEY

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
              {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    message = completion['choices'][0]['message']
    csv_string = message['content']
    '''

    client = OpenAI(api_key=config.OPENAI_API_KEY)
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
              {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    message = chat_completion.choices[0].message
    csv_string = message.content

    result = {}
    try:
        if csv_string and len(csv_string) > 0:
            result = csv_string_to_list(csv_string)
    except Exception as e:
        print(e)

    return result


def csv_string_to_list(csv_string):
    result = []
    lines = csv_string.strip().split('\n')
    headers = lines[0].split(',')

    for line in lines[1:]:
        values = line.split(',')
        item_dict = dict(zip(headers, values))
        result.append(item_dict)

    return result
