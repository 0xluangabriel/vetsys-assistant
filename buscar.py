from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma

load_dotenv()

MODELO = "gemini-3.5-flash-lite"

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
banco = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
llm = ChatGoogleGenerativeAI(model=MODELO)

# daqui para baixo: a pergunta, a busca, o contexto, o prompt e a resposta

pergunta = "qual é a melhor ração para filhotes?"
resultados = banco.similarity_search(pergunta, k=3)

contexto = ""
blocos = []

for resultado in resultados:
    fonte = "[Fonte: {}, seção {}]".format(resultado.metadata["arquivo"], resultado.metadata.get("secao", "introdução"))
    bloco = fonte + "\n" + resultado.page_content
    blocos.append(bloco)

contexto = "\n\n".join(blocos)

prompt = f"""Você é o assistente da Clínica Veterinária VetSys.
Responda à pergunta do tutor usando SOMENTE as informações do contexto abaixo.
Se a resposta não estiver no contexto, diga exatamente:
"Não encontrei essa informação nos documentos da clínica."
Não invente valores, prazos nem procedimentos.
No final, cite as fontes usadas, no formato (arquivo, seção).

Contexto:
{contexto}

Pergunta: {pergunta}"""

resposta = llm.invoke(prompt)
print(resposta.text)