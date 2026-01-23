import asyncio
import json
import os
from pathlib import Path

from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from dotenv import load_dotenv
from models.schemas import ResultSchema


async def main():
    """
    Crawl a URL and extract structured JSON data using LLM.
    
    Args:
        url: The URL to crawl
        schema: JSON schema for extraction
        output_dir: Directory to save results (optional)
        prompt: Custom prompt for LLM extraction (optional)
        api_key: OpenAI API key (uses environment variable if not provided)
    """
    # Get API key from args or environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Warning: No OpenAI API key provided. Set OPENAI_API_KEY environment variable or use --api-key")
    
    # Configure browser settings
    browser_config = BrowserConfig(
        headless=True,
        verbose=False
    )
    
    # Load instruction from file
    try:
        with open("prompts/extraction_prompt.txt", "r") as f:
            instruction = f.read()
    except FileNotFoundError:
        print("Warning: extraction_prompt.txt not found. Using default instruction.")
        instruction = "Extract structured data in the Results heading 2 which has the URL started with https://n8n.io/workflows/ according to the schema."
    
    url = "https://n8n.io/workflows/categories/ai/"
    # 1. Define the LLM extraction strategy
    llm_strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="openai/gpt-oss-20b", 
            api_token=api_key
        ),
        schema=ResultSchema.model_json_schema(),
        extraction_type="schema",
        instruction=instruction,
        chunk_token_threshold=1000,
        overlap_rate=0.0,
        apply_chunking=True,
        input_format="markdown",  # or "html", "fit_markdown"
        extra_args={"temperature": 0.0, "max_tokens": 5000}
    )
    
    # 2. Configure the crawler run with the extraction strategy
    run_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS
    )
        
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the crawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Run the crawler with LLM extraction
        result = await crawler.arun(url=url, config=run_config)
        
        # Display results
        print(f"Crawl successful: {result.success}")
        if not result.success:
            print(f"Error: {result.error_message}")
            return
        
        # Process extracted content
        if hasattr(result, 'extracted_content') and result.extracted_content:
            print("\nExtracted JSON data:")
            try:
                extracted_data = json.loads(result.extracted_content) if isinstance(result.extracted_content, str) else result.extracted_content
                print(json.dumps(extracted_data, indent=2))
                
                # Save the extracted JSON if output directory is specified
                if output_dir:
                    output_path = Path(output_dir)
                    output_path.mkdir(exist_ok=True, parents=True)
                    
                    # Create filename from URL
                    url_filename = url.replace("://", "_").replace("/", "_").replace("?", "_")
                    if len(url_filename) > 100:
                        url_filename = url_filename[:100]
                    
                    # Save JSON and markdown
                    json_file = output_path / f"{url_filename}.json"
                    markdown_file = output_path / f"{url_filename}.md"
                    
                    with open(json_file, "w", encoding="utf-8") as f:
                        json.dump(extracted_data, f, indent=2)
                    
                    with open(markdown_file, "w", encoding="utf-8") as f:
                        f.write(result.markdown.raw_markdown if hasattr(result, 'markdown') and result.markdown else "")
                    
                    print(f"\nExtracted JSON saved to: {json_file}")
                    print(f"Markdown content saved to: {markdown_file}")
                
                # Show usage statistics if available
                if hasattr(llm_strategy, 'show_usage'):
                    llm_strategy.show_usage()
                
            except Exception as e:
                print(f"Error processing extracted content: {e}")
        else:
            print("\nNo structured data was extracted or extraction failed.")

if __name__ == "__main__":
    load_dotenv(override=True)
    asyncio.run(main()) 