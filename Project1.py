import requests
import json
from bs4 import BeautifulSoup

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"  # Change to your model

def ask_ollama(prompt):
    """Simple function to ask Ollama a question"""
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=data)
        result = response.json()
        return result['response']
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, couldn't get response from Ollama"

def scrape_website(url):
    """Get text content from a website"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unnecessary elements
        for element in soup(['script', 'style', 'img', 'input']):
            element.decompose()
            
        # Get title and text
        title = soup.title.string if soup.title else "No title"
        text = soup.get_text(separator='\n', strip=True)
        
        return f"Title: {title}\n\nContent:\n{text}"
    
    except Exception as e:
        return f"Error scraping website: {e}"

def create_brochure(company_name, website_url):
    """Create a company brochure"""
    print(f"Scraping {website_url}...")
    website_content = scrape_website(website_url)
    
    # Limit content to avoid overwhelming the model
    if len(website_content) > 3000:
        website_content = website_content[:3000] + "..."
    
    prompt = f"""
    Create a short marketing brochure for {company_name} based on their website content below.
    Make it professional and engaging for customers and investors.
    Use markdown formatting.
    
    Website content:
    {website_content}
    
    Brochure:
    """
    
    print(f"Creating brochure for {company_name}...")
    brochure = ask_ollama(prompt)
    return brochure

# Example usage
if __name__ == "__main__":
    # Test connection
    test_response = ask_ollama("Hello! Are you working?")
    print("Ollama test:", test_response[:100] + "...")
    
    # Create brochure
    company = "HuggingFace"
    url = "https://huggingface.co"
    
    brochure = create_brochure(company, url)
    print("\n" + "="*50)
    print("COMPANY BROCHURE")
    print("="*50)
    print(brochure)
    