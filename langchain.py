from langchain.llms import OpenAI

llm = OpenAI(openai_api_key="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")

text = "What would be a good company name for a company that makes colorful socks?"

llm.predict(text)