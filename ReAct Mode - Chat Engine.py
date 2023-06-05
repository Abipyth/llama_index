import sys
sys.path.append("C:/users/abinaya/appdata/roaming/python/python311/site-packages")
import requests
from tqdm import tqdm
from langchain.chat_models import ChatOpenAI
from llama_index import VectorStoreIndex, SimpleDirectoryReader
import os

# Load the text data from the URL
url = "https://www.gutenberg.org/cache/epub/70911/pg70911.txt"
response = requests.get(url, stream=True)
response.raise_for_status()

# Create the 'data' directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Save the text data as a single file
file_path = 'data/pg70911.txt'
with open(file_path, 'wb') as file:
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        file.write(data)
    progress_bar.close()

print("Text data has been saved.")

# Split the text data into chapters
with open(file_path, 'r', encoding='utf-8') as file:
    text_data = file.read()

chapters = text_data.split("CHAPTER")

# Save each chapter as a separate text file
for i, chapter in enumerate(chapters[1:], 1):
    chapter_path = f"data/chapter_{i}.txt"
    with open(chapter_path, "w", encoding='utf-8') as file:
        file.write(chapter.strip())
    print(f"Chapter {i} saved.")

# Create separate indexes and query engines for each chapter
query_engines = []
for i in range(1, 7):
    chapter_path = f"data/chapter_{i}.txt"
    with open(chapter_path, 'r', encoding='utf-8') as file:
        chapter_data = file.read()
        chapter_index = VectorStoreIndex.from_documents([chapter_data])
        chapter_query_engine = SimpleDirectoryReader(index=chapter_index, chat_model=ChatOpenAI(openai_api_key="YOUR_API_KEY"))
        query_engines.append(chapter_query_engine)

# Example Questions and Testing Query Engines
example_questions = [
    "What is discussed in Chapter 3?",
    "Who is the main character in Chapter 5?",
    "Find references to a specific term in Chapter 2.",
    # Add more example questions as needed
]

for i, question in enumerate(example_questions):
    chapter_number = i % 6 + 1
    chapter_query_engine = query_engines[chapter_number - 1]
    response = chapter_query_engine.query(question)
    print(f"Question: {question}")
    print(f"Chapter {chapter_number} Response: {response}")
    print("------")


