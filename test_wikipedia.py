from ai.knowledge.wikipedia_source import WikipediaSource

wiki = WikipediaSource()

result = wiki.search("Python programming")

print("=" * 50)
print("Success :", result.success)
print("Source  :", result.source)
print("Query   :", result.query)
print("Content :")
print(result.content)
print("=" * 50)