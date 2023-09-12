import vertexai
from vertexai.language_models import TextGenerationModel
import google.cloud.logging
from config import PROJECT_ID,LOCATION
from datetime import datetime
from language_translation import translate
import re

client = google.cloud.logging.Client(project=PROJECT_ID)
client.setup_logging()
log_name = "news_updates_log"
logger = client.logger(log_name)

vertexai.init(project=PROJECT_ID, location=LOCATION)

parameters = {
        
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
}

model = TextGenerationModel.from_pretrained("text-bison@001")

def generate_topics():

    topic_name="cloud Computing"
    input_text = f"""
    Example 1:
        Input : 
        Give me trending topic in AI as one word.
        Output:
        Generative AI

        Input : 
        Give me trending topic in {topic_name} 

        Output:
        

    """

    response_text = model.predict(
       input_text,
      **parameters
    )

    str_response = str(response_text)

    # words = []
    # for line in str_response.splitlines():
    #     words.append(line.split('.')[1].strip())

    # # Create a string with the list of words
    # generated_topic = '\n'.join(words)

    print(f"topic name : {str_response}   END")

    return str_response


    #glossary_list = re.findall(r"\d+\.\s+(.*)\n", response_text)
    # print(type(response_text))

def get_explanations(generated_topic):

    input_text =  f"Explain about {generated_topic}. Also, include some relevant website links at the end for detailed explanation"

    response_text = model.predict(
        input_text,
        **parameters
    )

    str_response = str(response_text)

    return str_response
    # print(str_response)



generated_topic = generate_topics()
explanation = get_explanations(generated_topic)
translation_required = True

if translation_required:
    explanation = translate(explanation,'hi')
    print("Translating to hindi")
print(explanation)



# import re

# # Create a list of strings
# strings = ["1. Artificial intelligence (AI)", "2. Machine learning (ML)", "3. Deep learning (DL)", "4. Internet of things (IoT)", "5. Blockchain", "6. Edge computing", "7. Serverless computing", "8. Containerization", "9. Microservices", "10. DevOps"]

# # Remove all numbers from the strings
# new_strings = [re.sub("\\d+", "", string) for string in strings]

# # Create a new list with the words
# words = [word for string in new_strings for word in string.split()]

# # Print the new list
# print(words)



"""

words = []
for word in data.split():
    if word.isalpha():
        words.append(word)

# Create a string with the words in the list
string = " ".join(words)

# Print the string
print(string)

"""

