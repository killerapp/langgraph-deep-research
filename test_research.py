import requests
from typing import Optional, Union, Dict, Any

class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def run_stateless(
        self,
        assistant_id: str,
        input_data: Optional[Union[str, Dict, list]] = None,
        config: Optional[Dict] = None,
        metadata: Optional[Dict] = None,
        **kwargs
    ) -> Dict:
        payload = {
            "assistant_id": assistant_id,
            "input": input_data,
            "config": config,
            "metadata": metadata,
        }
        payload.update(kwargs)
    
        url = f"{self.base_url}/runs/wait"
        response = self.session.post(url, json=payload)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("HTTP Error:", response.status_code, response.text)
            raise e
        return response.json()

def main():
    # Initialize the client with the LangGraph server URL
    client = MCPClient("http://127.0.0.1:2024")
    
    # The assistant ID for ollama_deep_researcher
    assistant_id = "a6ab75b8-fb3d-5c2c-a436-2fee55e33a06"
    
    # The research topic - must be a string as per SummaryStateInput
    research_input = "Latest developments in quantum computing"
    
    # Configuration based on Configuration class
    config = {
        "configurable": {
            "max_web_research_loops": 3,
            "local_llm": "deepseek-r1:32b",
            "max_output_tokens": 16384,
            "max_search_results": 5
        }
    }

    try:
        print(f"Starting research on topic: {research_input}")
        result = client.run_stateless(
            assistant_id=assistant_id,
            input_data={"research_topic": research_input},  # Pass as dict with research_topic key
            config=config,
            metadata={}  # Empty metadata object
        )
        print("\nResearch Results:")
        print(result)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
