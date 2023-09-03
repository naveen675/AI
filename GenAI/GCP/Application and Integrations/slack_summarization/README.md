# Slack Summarisation chat bot


When we open a long chat conversation between your coleagues about some bugs,server down or any other features, Everytime we have to go through the whole conversation to get an idea of what is discussed. But with this Summarisation bot you can request to summarize the whole conversation with one single request "/summarize".  

This has built on top of Google cloud Vertex AI by using a language model. 
An https Endpoint has created by deploying this application on cloud fucntion. 
This will be invoked while deploying an app in slack work space.
If the user wants to summarise a conversation or long text they can request with one single command "/summsarize"

Note:
A token validation is mandatory to avoid unknown http invokations . Only a request with valid token will be given response 200.
