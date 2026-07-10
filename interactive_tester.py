import sys
import io
from adk_pipeline import run_adk_pipeline

# Reconfigure stdout/stderr to UTF-8 to prevent encoding crashes on Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def main():
    print("==================================================")
    print("       ADK Predictive Router - Prompt Tester      ")
    print("==================================================")
    print("Type a prompt and press Enter to see the routing decision and response.")
    print("Type 'exit' or 'quit' to close the tester.")
    print("--------------------------------------------------")

    while True:
        try:
            # Get prompt from user
            prompt = input("\nEnter prompt: ").strip()
            
            # Check for exit commands
            if prompt.lower() in ['exit', 'quit', 'q']:
                print("\nExiting Prompt Tester. Goodbye!")
                break
                
            if not prompt:
                print("Prompt cannot be empty. Please enter a valid prompt.")
                continue

            # Run through the ADK pipeline
            # Threshold is set to 0.5 by default
            run_adk_pipeline(prompt)
            
        except KeyboardInterrupt:
            print("\nExiting Prompt Tester. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
