from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    input="Give analysis about the item "
)

print(response.output_text)

# this part of the code is not complete, and it is mainly given llm analysis between items or products