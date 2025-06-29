import openai
import os

# Usa tu API key desde una variable de entorno o escríbela directamente aquí (⚠️ no recomendado subirlo a GitHub)
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("❌ No se encontró la API key en la variable de entorno OPENAI_API_KEY.")
    exit()

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hola, ¿estás funcionando?"}
        ]
    )
    print("✅ Conexión exitosa:")
    print(response.choices[0].message["content"])
except Exception as e:
    print("❌ Error al conectar con OpenAI:")
    print(e)
