import re
import openai
import time

# Define the topic variable
topic = "Discuss the a boys love of his mother." 

# Define the actors
actor_one = "Carl Jung"
actor_two = "Sigmund Freud"
print(f"Roleplaying {actor_one} and {actor_two} discussing {topic}")


def actorone(text, chunk_size, last_response):
    # import the OpenAI API key to access GPT models
    openai.api_key = ""
    # Split the data into tokens using a regular expression
    tokens = re.findall(r'\b\w+\b', text)
    # Initialize "content" with an empty string
    content = ""
    # Iterate through the tokens in chunks of chunk_size
    for i in range(0, len(tokens), chunk_size):
        chunk = tokens[i:i+chunk_size]
        sum_string = ' '.join(chunk)
        preprompt = f"You are roleplaying {actor_one} talking to {actor_two} about {topic}, you will answer in short one sentence answers. Here is the last response you gave, look at it before replying again:" + last_response
        completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=170,
            n=1,
            stop=None,
            timeout=30,
            temperature=0.9,
            messages=[
                {"role": "system", "content": preprompt},
                {"role": "user", "content": sum_string},
                {"role": "system", "content": last_response}
            ]
        )
        content = completions["choices"][0]["message"]["content"].strip().replace("\n", "")
        # Update the last response variable
        last_response = content
    return content


def actortwo(text, chunk_size, last_response):
    # import the OpenAI API key to access GPT models
    openai.api_key = ""
    # Split the data into tokens using a regular expression
    tokens = re.findall(r'\b\w+\b', text)
    # Initialize "content" with an empty string
    content = ""
    # Iterate through the tokens in chunks of chunk_size
    for i in range(0, len(tokens), chunk_size):
        chunk = tokens[i:i+chunk_size]
        sum_string = ' '.join(chunk)
        preprompt = f"You are role playing {actor_two} talking to {actor_one} about {topic}, you will answer in short one sentence answers. Here is the last response you gave, look at it before replying again:" + last_response
        completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=170,
            n=1,
            stop=None,
            timeout=30,
            temperature=0.9,
            messages=[
                {"role": "system", "content": preprompt},
                {"role": "user", "content": sum_string},
                {"role": "system", "content": last_response}
            ]
        )
        content = completions["choices"][0]["message"]["content"].strip().replace("\n", "")
        # Update the last response variable
        last_response = content

    return content

def talk_to_self(topic, chunk_size=10):
    # Initialize "content" with the topic
    content = topic
    # Initialize "last_response" with an empty string
    last_response = ""
    # Loop 50 times
    for i in range(50):
        # Call the actorone function with the current content and chunk_size, and last_response
        actorone_response = actorone(content, chunk_size, last_response)
        # Call the actortwo function with the actorone's response, chunk_size, and last_response
        actortwo_response = actortwo(actorone_response, chunk_size, last_response)
        # Update the content variable with the actortwo's response
        content = actorone(actortwo_response, chunk_size, last_response)
        time.sleep(10)
        # Print the conversation
        print(f"{actor_one}: " + (actorone_response))
        time.sleep(10)
        print(f"{actor_two}: " + (actortwo_response))
        # Update the last_response variable
        last_response = actortwo_response


if __name__ == '__main__':
    talk_to_self(topic, 10)
