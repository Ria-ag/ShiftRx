import os
import sys

def setup():
    print("="*60)
    print("GROQ API SETUP")
    print("="*60)
    
    if os.path.exists(".env"):
        print("\n.env file already exists")
        with open(".env", "r") as f:
            content = f.read()
            if "GROQ_API_KEY" in content and "gsk_" in content:
                print("API key is configured")
                print("\nReady to run: python run.py")
                return
    
    api_key = input("\nPaste your Groq API key here: ").strip()
    
    if not api_key:
        print("\nNo key provided. Exiting.")
        sys.exit(1)
    
    if not api_key.startswith("gsk_"):
        print("\nWarning: Key doesn't start with 'gsk_'")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Exiting.")
            sys.exit(1)
    
    # Create .env file
    with open(".env", "w") as f:
        f.write(f"GROQ_API_KEY={api_key}\n")
    
    print("\n.env file created!")
    
    # Check dependencies
    print("\nChecking dependencies...")
    try:
        import groq
        import jsonschema
        from dotenv import load_dotenv
        print("All dependencies installed")
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("\nInstalling dependencies...")
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
    
    print("\n" + "="*60)
    print("Setup complete!")
    print("="*60)
    print("\nRun your extraction: python run.py")
    print("  python run.py")

if __name__ == "__main__":
    setup()