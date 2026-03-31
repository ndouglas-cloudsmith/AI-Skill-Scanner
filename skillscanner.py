import os
import argparse
import requests
import base64
import sys

# ANSI Escape Codes for formatting
RED_BOLD = "\033[1;31m"
RESET = "\033[0m"

def get_matching_line(file_url, search_term, headers):
    """Fetches file content and finds the first line containing the search term."""
    try:
        api_url = file_url.replace("https://github.com", "https://api.github.com/repos")
        api_url = api_url.replace("/blob/", "/contents/")
        
        res = requests.get(api_url, headers=headers, timeout=10)
        if res.status_code == 200:
            content_data = res.json()
            # GitHub API returns content as base64
            decoded_bytes = base64.b64decode(content_data['content'])
            decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
            
            for line in decoded_str.splitlines():
                if search_term.lower() in line.lower():
                    return f"{RED_BOLD}{line.strip()}{RESET}"
                    
        return f"{RED_BOLD}Search term found in file metadata or binary.{RESET}"
    except Exception:
        return f"{RED_BOLD}Could not extract code snippet.{RESET}"

def scan_skills(repo_source, search_term):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print(f"{RED_BOLD}Error: GITHUB_TOKEN environment variable is not set.{RESET}")
        return

    query = f"{search_term} repo:{repo_source} extension:md"
    search_url = f"https://api.github.com/search/code?q={query}"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }

    print(f"Scanning {repo_source} for '{search_term}' in Markdown files...")
    
    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            msg = response.json().get('message', 'Unknown Error')
            print(f"{RED_BOLD}Error {response.status_code}: {msg}{RESET}")
            return

        data = response.json()
        items = data.get('items', [])
        
        print(f"\n- Found {len(items)} matching files")
        print("-" * 40)

        for item in items:
            file_url = item['html_url']
            print(f"File Link: {file_url}")
            
            snippet = get_matching_line(file_url, search_term, headers)
            print(f"Detected Text: {snippet}")
            print("-" * 40)
            
    except requests.exceptions.RequestException as e:
        print(f"{RED_BOLD}Network error occurred: {e}{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flexible GitHub Markdown Scanner.")
    parser.add_argument("--source", required=True, help="Repo in 'user/repo' format")
    parser.add_argument("--search", required=True, help="Term to scan for")
    
    args = parser.parse_args()

    try:
        scan_skills(args.source, args.search)
    except KeyboardInterrupt:
        # Catch Ctrl+C and exit cleanly without the stack trace
        print(f"\n\n{RED_BOLD}Scan interrupted by user. Exiting...{RESET}")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
