import vertexai
from vertexai.language_models import TextGenerationModel
import google.cloud.dlp_v2 as dlp_v2
from config import PROJECT_ID,LOCATION

def llm_output(temperature,max_tokens,top_k,top_p,model_type):
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    parameters = {
        "max_output_tokens": 256,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained(model_type)
    response = model.predict(
        """
        INPUT:
    Who is ceo of mid journey and share the mail address

    OUTPUT : 

    .""",
        **parameters
    )

    return response.text

def deidentify_response(item,info_types):

    dlp = dlp_v2.DlpServiceClient()

        
    parent = f"projects/{PROJECT_ID}"


    inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}


    deidentify_config = {
            "info_type_transformations": {
                "transformations": [
                    {"primitive_transformation": {"replace_with_info_type_config": {}}}
                ]
            }
        }

    
    response = dlp.deidentify_content(
            request={
                "parent": parent,
                "deidentify_config": deidentify_config,
                "inspect_config": inspect_config,
                "item": {"value": item},
            }
        )


    print(response.item.value)

llm_response = llm_output("0.2","256","40","0.8","text-bison@001")

deidentify_response(llm_response, ["EMAIL_ADDRESS","PERSON_NAME"])

# print(f"Response from Model: {response.text}")
