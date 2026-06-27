SCRAPER_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "navigate",
            "description": "Navigates the browser to the specified URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The full HTTP/HTTPS URL to visit."
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_page_content",
            "description": "Extracts the visible text from the current webpage.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]