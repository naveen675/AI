# Slack Summarisation chat App
    When we open a long chat conversation between your coleagues about some bugs,server down or any other features, Everytime we have to go through the whole conversation to get an idea of what is discussed. But with this Summarisation App you can request to breif the whole conversation with one single request "/summarize".  
  
    This has built on top of Google cloud Vertex AI by using a language model. 
    An https Endpoint has created by deploying this application on cloud fucntion. 
    This will be invoked while deploying an app in slack work space.
    If the user wants to summarise a conversation or long text they can request with one single command "/summsarize"
    
    Note:
    A token validation is mandatory to avoid unknown http invokations . Only a request with valid token will be given response 200.

### Language Model
    Language model has developed with below tokens and parameters

      "max_output_tokens": 256,
      "temperature": 0.2,
      "top_p": 0.8,
      "top_k": 40
    Prompt
      Single shot prompt is used to improve the response of output for given input.
