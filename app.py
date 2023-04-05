import re
import openai
import time

# Define the topic variable
topic = "Discuss the a boys love of his mother." 

# Define the actors
actor_one = "Carl Jung"
actor_two = "Sigmund Freud"
print(f"Roleplaying {actor_one} and {actor_two} discussing {topic}")

# Define the actorone function
def actorone(text, last_response):
    # import the OpenAI API key to access GPT models
    openai.api_key = "your-key-here"
    # Split the data into tokens using a regular expression
    tokens = re.findall(r'\b\w+\b', text)
    # Initialize "content" with an empty string
    content = ""
    # Join all the tokens into a single string
    input_text = ' '.join(tokens)
    # Define the prompt
    prompt = f"You are roleplaying {actor_one} talking to {actor_two} about {topic}, you will answer in short one sentence answers. Here is the last response you gave, look at it before replying again:" + last_response
    # Send the input and prompt to the OpenAI GPT-3 model
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=170,
        n=1,
        stop=None,
        timeout=30,
        temperature=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.5,
        inputs={
            "text": input_text,
            "metadata": {
                "role": "user"
            }
        },
        output_prefix=last_response,
        output_suffix="\n\nSystem:"
    )
    # Get the generated response from the OpenAI API
    content = completions.choices[0].text.strip().replace("\n", "")
    # Update the last response variable
    last_response = content
    return content, last_response

# Define the actortwo function
def actortwo(text, last_response):
    # import the OpenAI API key to access GPT models
    openai.api_key = "your-key-here"
    # Split the data into tokens using a regular expression
    tokens = re.findall(r'\b\w+\b', text)
    # Initialize "content" with an empty string
    content = ""
    # Join all the tokens into a single string
    input_text = ' '.join(tokens)
    # Define the prompt
    prompt = f"You are role playing {actor_two} talking to {actor_one} about {topic}, you will answer in short one sentence answers. Here is the last response you gave, look at it before replying again:" + last_response
    # Send the input and prompt to the OpenAI GPT-3 model
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=170,
        n=1,
        stop=None,
        timeout=30,
        temperature=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.5,
        inputs={
            "text": input_text,
            "metadata": {
                "role": "user"
            }
        },
        output_prefix=last_response,
        output_suffix="\n\nSystem:"
    )
    # Get the generated response from the OpenAI API
    content = completions.choices[0].text.strip().replace("\n", "")
    # Update the last response variable
    last_response = content
    return content, last_response

# Define the talk_to_self function
def talk_to_self(topic):
    # Initialize "content" with the topic
    content = topic
    # Initialize "last_response" with an empty string
    last_response = ""
    # Loop 50 times
    for i in range(50):
        # Call the actorone function with the current content and last_response
        actorone_response = actorone(content, last_response)
        # Call the actortwo function with the actorone's response and last_response
        actortwo_response = actortwo(actorone_response, last_response)
        # Update the content variable with the actortwo's response
        content = actorone(actortwo_response, last_response)
        time.sleep(10)
        # Print the conversation
        print(f"{actor_one}: " + actorone_response)
        time.sleep(10)
        print(f"{actor_two}: " + actortwo_response)
        # Update the last_response variable
        last_response = actortwo_response

# Call the talk_to_self function
if __name__ == '__main__':
    talk_to_self(topic)
