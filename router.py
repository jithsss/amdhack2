import torch
import torch.nn as nn
import torch.nn.functional as F
import requests

class GemmaGatingNetwork(nn.Module):
    def __init__(self, embedding_dim=768, hidden_dim=256):
        # 768 is the default embedding dimension for embeddinggemma
        super().__init__()
        self.fc1 = nn.Linear(embedding_dim, hidden_dim)
        self.dropout = nn.Dropout(0.2)
        self.fc2 = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        # Outputs a probability value between 0 (simple) and 1 (complex)
        return torch.sigmoid(self.fc2(x))

# Initialize the network and load your trained weights
gating_model = GemmaGatingNetwork()
gating_model.eval() # Set to evaluation mode for inference

def get_ollama_embeddings(prompt, model="embeddinggemma"):
    """Extracts the hidden state vector from the local Ollama instance."""
    url = "http://localhost:11434/api/embeddings"
    response = requests.post(url, json={"model": model, "prompt": prompt})
    response.raise_for_status() # Check for HTTP errors
    embedding = response.json()["embedding"]
    
    # Return as a 1D PyTorch tensor
    return torch.tensor(embedding, dtype=torch.float32)

def calculate_complexity(prompt):
    """The brain of the ADK router."""
    # 1. Grab the embedding (Zero API token cost)
    embedding_tensor = get_ollama_embeddings(prompt)
    
    # 2. Add batch dimension [1, embedding_dim]
    embedding_tensor = embedding_tensor.unsqueeze(0)
    
    # 3. Predict the complexity score
    with torch.no_grad():
        complexity_prob = gating_model(embedding_tensor).item()
        
    return complexity_prob

if __name__ == "__main__":
    # Example test
    sample_prompt = "Can you explain quantum computing in simple terms?"
    try:
        score = calculate_complexity(sample_prompt)
        print(f"Prompt: {sample_prompt}")
        print(f"Complexity Score: {score:.4f}")
    except Exception as e:
        print(f"Error testing complexity calculation: {e}")
