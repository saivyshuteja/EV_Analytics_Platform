#!/usr/bin/env python3
import sys
import os
import traceback

# Add backend to path
sys.path.insert(0, 'e:\\ev-analytics-platform\\backend')
os.chdir('e:\\ev-analytics-platform\\backend')

print("="*70)
print("TESTING RAG FILES")
print("="*70)

# Test 1: ingestion.py
print("\n[1/3] Testing ingestion.py...")
print("-"*70)
try:
    from ai.rag.ingestion import EVKnowledgeIngestion
    print("✓ Import successful")
    
    ingestion = EVKnowledgeIngestion()
    print("✓ Class instantiation successful")
    
    docs = ingestion.load_documents()
    print(f"✓ Loaded {len(docs)} documents")
    
    if len(docs) > 0:
        chunks = ingestion.create_chunks(docs)
        print(f"✓ Created {len(chunks)} chunks")
        print("✓ ingestion.py is WORKING ✅")
    else:
        print("⚠ No documents loaded (documents folder may be empty)")
        
except Exception as e:
    print(f"✗ Error in ingestion.py: {str(e)}")
    print("Traceback:")
    traceback.print_exc()
    print("ingestion.py status: ❌ FAILED")

# Test 2: retriever.py
print("\n[2/3] Testing retriever.py...")
print("-"*70)
try:
    from ai.rag.retriever import EVRetriever
    print("✓ Import successful")
    
    # Check if vector store exists first
    import os
    vector_store_path = 'e:\\ev-analytics-platform\\backend\\data\\vector_store\\faiss_index'
    if not os.path.exists(vector_store_path):
        print(f"⚠ Vector store not found at: {vector_store_path}")
        print("  → Need to run ingestion.py first to create it")
        print("retriever.py status: ⚠ WAITING FOR VECTOR STORE")
    else:
        retriever = EVRetriever()
        print("✓ Class instantiation successful")
        
        results = retriever.search("What is CAFV eligibility?")
        print(f"✓ Search returned {len(results)} results")
        print("✓ retriever.py is WORKING ✅")
        
except Exception as e:
    print(f"✗ Error in retriever.py: {str(e)}")
    print("Traceback:")
    traceback.print_exc()
    print("retriever.py status: ❌ FAILED")

# Test 3: qa_chain.py
print("\n[3/3] Testing qa_chain.py...")
print("-"*70)
try:
    # Check GROQ_API_KEY first
    groq_key = os.environ.get('GROQ_API_KEY')
    if not groq_key:
        print("⚠ GROQ_API_KEY not set in environment")
        print("  → Set it with: $env:GROQ_API_KEY = 'your-key'")
        print("qa_chain.py status: ⚠ MISSING API KEY")
    else:
        from ai.rag.qa_chain import EVRAGChain
        print("✓ Import successful")
        
        rag = EVRAGChain()
        print("✓ Class instantiation successful")
        print("✓ qa_chain.py is WORKING ✅")
        
except Exception as e:
    print(f"✗ Error in qa_chain.py: {str(e)}")
    print("Traceback:")
    traceback.print_exc()
    print("qa_chain.py status: ❌ FAILED")

print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)
print("\nRun order to get everything working:")
print("1. ingestion.py  → Creates vector store")
print("2. retriever.py  → Tests vector store retrieval")
print("3. qa_chain.py   → Tests QA with Groq API")
print("="*70)
