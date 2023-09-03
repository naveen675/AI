#Summarises chat conversation or text on slack. 
# chat summary is built on top of Vertex AI text generation [llm model (text-bison@001) 
# Deploy this url endpoint in needed slack workspace. 
# Token validation at server side is mandatory to avoid hackers.
# Only request with valid token will be allowed to get the response
# single shot prompt is used to get the more accurate response.


import functions_framework
import vertexai
from vertexai.language_models import TextGenerationModel
from datetime import datetime
import google.cloud.logging
import json

client = google.cloud.logging.Client(project=ProjectId)
client.setup_logging()
log_name = "text-summary-cloudfunction-log"
logger = client.logger(log_name)


@functions_framework.http
def hello_http(request):
    
    input_text = request.form['text']
    logger.log(f"{input_text} received at : {datetime.now()}")
    vertexai.init(project=ProjectID, location=Location)

    parameters = {
        
        "max_output_tokens": 256,
        "temperature": 0.5,
        "top_p": 0.8,
        "top_k": 40
    }
    

    logger.log(f"Text received is : {input_text}")
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        f"""Example  1
    ---------------------------------------------------------------------------------------------------
    INPUT DIALOGUE:
    #Person1#: What time is it, Tom?
    #Person2#: Just a minute. It\'s ten to nine by my watch.
    #Person1#: Is it? I had no idea it was so late. I must be off now.
    #Person2#: What\'s the hurry?
    #Person1#: I must catch the nine-thirty train.
    #Person2#: You\'ve plenty of time yet. The railway station is very close. It won\'t take more than twenty minutes to get there.
    ---------------------------------------------------------------------------------------------------
    SUMMARY:
    #Person1# is in a hurry to catch a train. Tom tells #Person1# there is plenty of time.
    ---------------------------------------------------------------------------------------------------
    INPUT DIALOGUE:
    {input_text}
    ---------------------------------------------------------------------------------------------------
    SUMMARY: """,
      **parameters
    )

    data = {}
    data['blocks'] = []

    data['blocks'].append(
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Input text : {input_text}"
			}
		}
    )
    data['blocks'].append(

        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Summary : {response.text}"
			}
		}
    )
    
    logger.log(f"response : {data}")

    return json.dumps(data),200,{'Content-Type': 'application/json'}
