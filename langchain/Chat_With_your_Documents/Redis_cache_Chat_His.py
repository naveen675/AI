async def retrieve_document( search_to_string, email_id, session_id, collection_name)-> AsyncIterable[str]:

        callback = AsyncIteratorCallbackHandler()

        llm = ChatOpenAI(
            callbacks=[callback],
            streaming=True,
            temperature=0,
            openai_api_key="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"
        )
