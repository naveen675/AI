import vertexai
from vertexai.language_models import TextGenerationModel
from datetime import datetime


print(datetime.now())

vertexai.init(project="genia-data-pipe", location="us-central1")
parameters = {
    "max_output_tokens": 256,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}
model = TextGenerationModel.from_pretrained("text-bison@001")
response = model.predict(
    """Example  1
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

Summarize 

.""",
    **parameters
)
print(f"Response from Model: {response.text}")