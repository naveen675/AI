from PIL import Image
from google.cloud import aiplatform
from google.oauth2 import service_account
import base64

credentials = service_account.Credentials.from_service_account_file(
"sample.json")

import vertexai
import io
from vertexai.vision_models import ImageCaptioningModel,ImageQnAModel
aiplatform.init(
        project="project",
        staging_bucket="gs://",
        credentials=credentials,

    )
model = ImageCaptioningModel.from_pretrained("imagetext@001")
image = Image.open("dog-11422.png")


captions = model.get_captions(
    image=image,
    # Optional:
    number_of_results=1,
    language="en",
)
print(captions)



model = ImageQnAModel.from_pretrained("imagetext@001")
image = Image.load_from_file("gorrilla2.jfif")
answers = model.ask_question(
    image=image,
    question="Detect The Obect in the image tell me its name",
    # Optional:
    number_of_results=1,
)
print(answers)
