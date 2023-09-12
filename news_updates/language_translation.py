from google.cloud import translate_v3


def translate(text, target_language):
    
     # Create a client
    client = translate_v3.TranslationServiceClient()

    # Initialize request argument(s)
    print(text)
    request = translate_v3.TranslateTextRequest(
        contents=[f"""{text}"""]
            ,
        target_language_code=target_language,
        parent="projects/genia-data-pipe",
    )

    # Make the request
    response = client.translate_text(request=request)

    # Handle the response
    # print(response)

    
    return response


# print(translate("Hi How are you", "ru"))
