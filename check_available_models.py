import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("=" * 60)
print("CHECKING GOOGLE GENERATIVE AI SETUP")
print("=" * 60)

# Try the old package first
try:
    import google.generativeai as genai
    print("✓ google.generativeai package is installed")
    
    genai.configure(api_key=api_key)
    
    print("\nListing available models:")
    print("-" * 60)
    
    models = genai.list_models()
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
    
    print("\n" + "=" * 60)
    print("Copy one of the model names above and we'll use it!")
    print("=" * 60)
    
except ImportError:
    print("✗ google.generativeai NOT installed")
    print("\nRun: pip install google-generativeai")
except Exception as e:
    print(f"Error: {e}")