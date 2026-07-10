import requests
import subprocess
import getpass
import sys

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(result.stderr)
        return False
    return True

def main():
    print("=== GitHub Automation Script ===")
    print("This script will create the remote repository 'amdhack2' on GitHub and push the current main branch to it.")
    
    # 1. Get token
    # Using input instead of getpass just in case terminal environment issues, but prompt clearly
    token = input("Please enter your GitHub Personal Access Token (PAT) (generate one at https://github.com/settings/tokens with 'repo' scope): ").strip()
    if not token:
        print("Token cannot be empty.")
        sys.exit(1)
        
    username = "jithsss"
    repo_name = "AMDhack"
    
    # 2. Call GitHub API to create the repository
    print(f"\nCreating repository '{repo_name}' on GitHub under user '{username}'...")
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "private": False,  # Set to True if you want a private repo
        "description": "ADK Predictive Router setup"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"Successfully created repository: https://github.com/{username}/{repo_name}")
    elif response.status_code == 422:
        print(f"Repository '{repo_name}' already exists on GitHub. Proceeding to push anyway...")
    elif response.status_code == 403:
        print(f"\n[Warning] Failed to create repository via API. Status code: 403")
        print("This usually means your Personal Access Token (PAT) lacks repo creation permissions.")
        print("We will attempt to push directly. (If you haven't already, please create 'amdhack2' manually at https://github.com/new first!)")
    else:
        print(f"Failed to create repository. Status code: {response.status_code}")
        print(response.json())
        sys.exit(1)
        
    # 3. Configure remote and push
    print("\nPushing local main branch to GitHub...")
    
    # Remove origin if it already exists
    subprocess.run("git remote remove origin", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Add remote using authenticated URL
    remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    if not run_command(f"git remote add origin {remote_url}"):
        sys.exit(1)
        
    # Push to main
    if run_command("git push -u origin main"):
        print("\n🎉 Successfully pushed code to GitHub!")
        print(f"Repository URL: https://github.com/{username}/{repo_name}")
    else:
        print("\nInitial push failed. The remote repository might already contain files (like a README or LICENSE).")
        choice = input("Would you like to force push to overwrite the remote files? (y/n): ").strip().lower()
        if choice == 'y':
            print("Force pushing...")
            if run_command("git push -u origin main --force"):
                print("\n🎉 Successfully force pushed code to GitHub!")
                print(f"Repository URL: https://github.com/{username}/{repo_name}")
            else:
                print("\n❌ Force push failed.")
        else:
            print("\n❌ Push canceled.")

if __name__ == "__main__":
    main()
