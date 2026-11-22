from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
banco = Chroma(persist_directory="chroma_db", embedding_function=embeddings)


def buscar_documentos(pergunta: str):
    """Busca nos documentos internos da clínica as informações gerais e regras:
    protocolos de vacinação, preparo e cuidados de castração e exames, preços,
    agendamento, cancelamento, formas de pagamento, horários e serviços.
    Use para perguntas sobre como a clínica funciona ou sobre orientações gerais.
    NÃO use para dados de um animal específico (vacinas aplicadas, histórico):
    para isso, use as ferramentas da API.
    Devolve trechos dos documentos, cada um com a sua fonte (arquivo e seção)."""
    resultados = banco.similarity_search(pergunta, k=3)

    blocos = []
    for resultado in resultados:
        fonte = "[Fonte: {}, seção {}]".format(
            resultado.metadata["arquivo"],
            resultado.metadata.get("secao", "introdução"),
        )
        bloco = fonte + "\n" + resultado.page_content
        blocos.append(bloco)

    return "\n\n".join(blocos)


if __name__ == "__main__":
    print(buscar_documentos("posso pagar com boleto?"))