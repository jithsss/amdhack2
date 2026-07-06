import requests
import sys
from router import calculate_complexity

# Reconfigure stdout/stderr to UTF-8 to prevent encoding crashes on Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def generate_local(prompt, model="gemma4"):
    print(f"[Local Execution] Generating response using '{model}' for prompt: '{prompt}'")
    url = "http://localhost:11434/api/generate"
    try:
        response = requests.post(url, json={"model": model, "prompt": prompt, "stream": False})
        response.raise_for_status()
        return response.json().get("response", "No response returned.")
    except Exception as e:
        print(f"Local generation error: {e}")
        return "Local generation failed."

def generate_remote(prompt):
    print(f"[Remote Execution] Routing to cloud API for complex prompt: '{prompt}'")
    # In reality, this would call OpenAI, Anthropic, or a cloud-hosted AMD ROCm instance
    return "This is a detailed, complex response generated in the cloud."

def run_adk_pipeline(prompt, threshold=0.5):
    """
    The main ADK pipeline logic with Predictive Routing.
    """
    output_lines = []
    output_lines.append(f"\n--- Processing Prompt ---")
    output_lines.append(f"Prompt: {prompt}")
    
    try:
        # 1. Gate the prompt
        complexity_score = calculate_complexity(prompt)
        output_lines.append(f"Complexity Score: {complexity_score:.4f} (Threshold: {threshold})")
        
        # 2. Route based on the score
        if complexity_score >= threshold:
            response = generate_remote(prompt)
        else:
            response = generate_local(prompt)
            
        output_lines.append(f"Result: {response}")
        
    except Exception as e:
        output_lines.append(f"Pipeline Error: {e}")
        output_lines.append("Fallback: Routing to remote due to error.")
        response = generate_remote(prompt)
        output_lines.append(f"Result: {response}")

    # Print to console
    output_text = "\n".join(output_lines)
    print(output_text)
    
    # Save to file
    with open("adk_output.txt", "a", encoding="utf-8") as f:
        f.write(output_text + "\n")

    return response

if __name__ == "__main__":
    # Clear output file on run
    with open("adk_output.txt", "w", encoding="utf-8") as f:
        f.write("=== ADK Pipeline Execution Log ===\n")
    
    print("Initializing ADK Pipeline...")
    
    # Test cases
    prompts = [
        "What is 2+2?",
        "Write a comprehensive summary of the economic impacts of quantum computing."
    ]
    
    for p in prompts:
        run_adk_pipeline(p)
