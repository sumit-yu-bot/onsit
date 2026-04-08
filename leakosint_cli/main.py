#!/usr/bin/env python3
"""
LeakOSINT CLI - Search for leaked data via command line
"""

import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Install with: pip install requests")
    sys.exit(1)

API_URL = "https://leakosintapi.com/"

def print_banner():
    """Display tool banner"""
    banner = """
    ╔═══════════════════════════════════════╗
    ║      LeakOSINT CLI Tool v1.0          ║
    ║   Search Leaked Data from Terminal    ║
    ╚═══════════════════════════════════════╝
    """
    print(banner)

def call_api(token, query, limit, lang, output_type):
    """Make API request to LeakOSINT"""
    payload = {
        "token": token,
        "request": query,
        "limit": limit,
        "lang": lang,
        "type": output_type
    }
    
    try:
        print(f"\n[*] Searching for: {query}")
        print("[*] Please wait...\n")
        
        response = requests.post(API_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"API returned status code {response.status_code}",
                "details": response.text
            }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response", "raw": response.text}

def interactive_mode(token):
    """Run in interactive mode"""
    print_banner()
    print("Welcome to Interactive Mode!\n")
    
    print("What would you like to search?")
    print("Examples: phone number, email, username, IP address, etc.\n")
    query = input("Enter your query: ").strip()
    
    if not query:
        print("\n[!] No query provided. Exiting.")
        sys.exit(0)
    
    limit_input = input("Results limit (press Enter for default 100): ").strip()
    try:
        limit = int(limit_input) if limit_input else 100
    except ValueError:
        print("[!] Invalid number. Using default limit: 100")
        limit = 100
    
    lang = input("Language code (press Enter for default 'en'): ").strip() or "en"
    
    print("\nOutput format:")
    print("  1. json (detailed)")
    print("  2. short (summary)")
    print("  3. html (web format)")
    output_choice = input("Choose format (1/2/3, default=1): ").strip()
    
    output_map = {"1": "json", "2": "short", "3": "html", "": "json"}
    output_type = output_map.get(output_choice, "json")
    
    result = call_api(token, query, limit, lang, output_type)
    
    print("\n" + "="*50)
    print("RESULTS:")
    print("="*50 + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("\n" + "="*50)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="LeakOSINT CLI - Search for leaked data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  leakosint --token YOUR_TOKEN
  leakosint --token YOUR_TOKEN --query "email@example.com"
  export LEAKOSINT_TOKEN="your_token"
  leakosint --query "search_term"
        """
    )
    
    parser.add_argument("--token", help="API token (or set LEAKOSINT_TOKEN)")
    parser.add_argument("--query", help="Single search query")
    parser.add_argument("--limit", type=int, default=100, help="Max results")
    parser.add_argument("--lang", default="en", help="Language code")
    parser.add_argument("--type", default="json", choices=["json", "short", "html"], help="Output format")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    token = args.token or os.environ.get("LEAKOSINT_TOKEN")
    
    if not token:
        print("\n[!] ERROR: API token required!")
        print("\nProvide token:")
        print("  1. leakosint --token YOUR_TOKEN")
        print("  2. set LEAKOSINT_TOKEN=YOUR_TOKEN\n")
        sys.exit(1)
    
    if args.interactive or not args.query:
        interactive_mode(token)
    else:
        print_banner()
        result = call_api(token, args.query, args.limit, args.lang, args.type)
        
        print("\n" + "="*50)
        print("RESULTS:")
        print("="*50 + "\n")
        
        if args.pretty:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
