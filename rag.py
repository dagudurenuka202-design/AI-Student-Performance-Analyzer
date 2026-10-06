import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader


# Embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Chroma database
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="student_knowledge"
)


def process_pdf(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"


    # Split text into chunks
    chunk_size = 1000

    chunks = [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]

    chunks = [
        chunk.strip()
        for chunk in chunks
        if chunk.strip()
    ]


    if not chunks:
        return []


    embeddings = embedding_model.encode(
        chunks
    ).tolist()


    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]


    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )

    return chunks


def search_knowledge(query):

    query_embedding = embedding_model.encode(
        [query]
    ).tolist()


    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )


    if not results["documents"]:
        return ""


    documents = results["documents"][0]

    return "\n\n".join(documents)