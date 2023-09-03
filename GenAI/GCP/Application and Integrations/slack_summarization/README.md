# Slack Summarization of chat App
    
    When we open a long chat conversation between your coleagues about some bugs,
    server down or any other features, Everytime we have to go through the whole conversation 
    to get an idea of what is discussed. But with this Summarisation 
    App you can request to breif the whole conversation with one single request "/summarize".  
  
    This has built on top of Google cloud Vertex AI by using a language model. 
    An https Endpoint has created by deploying this application on cloud fucntion. 
    This will be invoked while deploying an app in slack work space.
    If the user wants to summarise a conversation or long text they can request with one single command "/summsarize"
    
    Note:
    A token validation is mandatory to avoid unknown http invokations . Only a request with valid token will be given response 200.

    Language Model
        Language model has developed with below tokens and parameters
    
          "max_output_tokens": 256,
          "temperature": 0.5,
          "top_p": 0.8,
          "top_k": 40
        Prompt
          Single shot prompt is used to improve the response of output for given input.
#### Technical
        deployed on google cloud platform
        Cloud function (GCP serverless Event trigger , used for connecting services, maintains the server script)
        Vertex AI platform (GCP highly demanding ML platform with Pretrained, AutomL, Custom ML features)
        Bison Language model
        Slack APP
        Cloud logging to generate logs for each run of cloud function

### Examples of few conversations and long texts

    Example 1
               Conversation : "
         [10:47 PM]
        @Sai
         Have you considered upgrading your system?
         
        Sai  [10:48 PM]
        Yes, but I'm not sure what exactly I would need.
        
        Naveen  [10:48 PM]
        You could consider adding a painting program to your software. 
        It would allow you to make up your own
        flyers and banners for advertising.
        
        Sai  [10:49 PM]
        That would be a definite bonus.
        
        Naveen  [10:49 PM]
        You might also want to upgrade your hardware because it is pretty outdated now.
        
        Sai  [10:50 PM]
        How can we do that?
        
        Naveen  [10:50 PM]
        You'd probably need a faster processor, to begin with. 
        And you also need a more powerful hard disc, 
        more memory and a  faster modem. Do you have a CD-ROM drive?
        
        Sai  [10:51 PM]
        No.
        
        Naveen  [10:51 PM]
        Then you might want to add a CD-ROM drive too, 
        because most new software programs are coming out on Cds.
        
        Sai  [10:51 PM]
        That sounds great. Thanks."
    
    Summary of above conversation:
       Sai and Naveen are discussing Sai's computer system. Naveen suggests 
       that Sai upgrade his system by adding a painting program, upgrading his hardware, 
       and adding a CD-ROM drive.

    Example 2

        Input text : "This tutorial is a step by step guide to writing a Slack Slash command. 
        A Slack Slash command is a great way for users to interact with a custom application. 
        As the documentation states, it allows users to invoke your app by typing a 
        string into the message composer box"
    Summary :
       This tutorial explains how to write a Slack Slash command. 
       A Slack Slash command is a great way for users to interact with a custom application.
