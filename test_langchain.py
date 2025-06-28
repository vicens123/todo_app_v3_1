import os
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

def test_langchain_chat():
    try:
        chat = ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        response = chat([HumanMessage(content="Hello, who are you?")])
        print("✅ LangChain test passed.")
        print("Response:", response.content)

    except Exception as e:
        print("❌ LangChain test failed.")
        print("Error:", str(e))

# Ejecutar si se llama directamente
if __name__ == "__main__":
    test_langchain_chat()
