#!/usr/bin/env python3
import sys
import traceback

print("=" * 60)
print("Testing ingestion.py")
print("=" * 60)
try:
    from ai.rag.ingestion import EVKnowledgeIngestion
    print("✓ Successfully imported EVKnowledgeIngestion")
    ingestion = EVKnowledgeIngestion()
    print("✓ Successfully instantiated EVKnowledgeIngestion")
    docs = ingestion.load_documents()
    print(f"✓ Successfully loaded {len(docs)} documents")
except Exception as e:
    print(f"✗ Error with ingestion.py:")
    traceback.print_exc()

print("\n" + "=" * 60)
print("Testing retriever.py")
print("=" * 60)
try:
    from ai.rag.retriever import EVRetriever
    print("✓ Successfully imported EVRetriever")
    retriever = EVRetriever()
    print("✓ Successfully instantiated EVRetriever")
except Exception as e:
    print(f"✗ Error with retriever.py:")
    traceback.print_exc()

print("\n" + "=" * 60)
print("Testing qa_chain.py")
print("=" * 60)
try:
    from ai.rag.qa_chain import EVRAGChain
    print("✓ Successfully imported EVRAGChain")
    rag = EVRAGChain()
    print("✓ Successfully instantiated EVRAGChain")
except Exception as e:
    print(f"✗ Error with qa_chain.py:")
    traceback.print_exc()

print("\n" + "=" * 60)
print("Summary complete")
print("=" * 60)
