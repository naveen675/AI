# Responsible AI and Data Governance

    With the increase of LLM models and datsets, The more concerned part 
    in the business prospects, Data governance, How can we ensure that the sensitive 
    data is not leaked. Considering this concern, we can use google cloud "Data Loss Prevention" service 
    to mask or encrypt the sensitive data. Let take an example to understand it more.

# Example

     You are requesting an LLM the following information 
    
          Request:
          Who is ceo of mid journey and share the mail address
  
          Actuall Response : 
          The CEO of Mid Journey is Karan Bajwa. His email address is karan@midjourney.com.
   
        Consider if this information need not not expose to certain users 
        then we can use DLP to mask the mail and name
        The response after applying the output will be as follows
        
          Response After DLP: 
          The CEO of MidJourney is [PERSON_NAME]. His email address is [EMAIL_ADDRESS].

  Cosider if there is any sensitive information like credit card number, transactions, phone numbers
  while training preparing datasets then with DLP API, we can mask them with generic name.
  There are multiple pre built info types that we can utilise to mask the sesitive information
  Referrences
  1. [Info Types](https://cloud.google.com/dlp/docs/infotypes-reference)
  2. [Data Loss Prevention](https://cloud.google.com/dlp/docs/)
  
