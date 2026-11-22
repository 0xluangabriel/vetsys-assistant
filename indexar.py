from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

divisor = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "documento"), ("##", "secao")]
)

todos_pedacos=[]

for arquivo in Path("docs").glob("*.md"):
    texto = arquivo.read_text(encoding="utf-8")
    pedacos = divisor.split_text(texto)
    for pedaco in pedacos:
        pedaco.metadata["arquivo"] = arquivo.name
        todos_pedacos.append(pedaco)
    print(arquivo.name, end=" = ")
    print(len(pedacos))
print("Total de pedaços: {}".format(len(todos_pedacos)))
print(todos_pedacos[0].metadata)
print(todos_pedacos[0].page_content[:100])

banco = Chroma.from_documents(
    documents=todos_pedacos,
    embedding=embeddings,
    persist_directory="chroma_db",
)

resultados = banco.similarity_search("quanto tempo de jejum antes de castrar?", k=3)

for resultado in resultados:
    print(resultado.metadata)
    print(resultado.page_content[:100])