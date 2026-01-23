"""
N8N Authentication Profile Example with Crawl4AI

This script demonstrates how to:
1. Create a persistent browser profile for n8n authentication
2. Save screenshots and content from authenticated pages
3. Use profiles for maintaining login sessions

Based on the BrowserProfiler class for browser profile management.
"""

import asyncio
import os
import base64
from pathlib import Path
from colorama import Fore, Style, init
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.browser_profiler import BrowserProfiler
from crawl4ai.async_logger import AsyncLogger

# Initialize colorama for colored output
init()

# ======= CONFIGURATION (MODIFY THESE VALUES) =======

# URL to scrape
TARGET_URL = "https://tubakhuym.app.n8n.cloud/workflow/nJA2ArB6nZzFvZIB"

# Browser settings
HEADLESS = False  # Set to False to see the browser window
BROWSER_TYPE = "chromium"  # Use chromium (the browser type matters for the profile format)

# Profile name (set to None to choose interactively or create new)
PROFILE_NAME = "n8n-profile"

# Content saving
SAVE_CONTENT = True
OUTPUT_MARKDOWN_FILENAME = "scraped_content.md"
OUTPUT_HTML_FILENAME = "scraped_content.html"

# Screenshot settings
TAKE_SCREENSHOT = True
SCREENSHOT_FILENAME = "screenshot.png"

# Additional wait time before scraping (to ensure page loads properly)
PRE_SCRAPE_WAIT_SECONDS = 5

# ======= END CONFIGURATION =======

# Create a shared logger instance
logger = AsyncLogger(verbose=True)

# Create a shared BrowserProfiler instance
profiler = BrowserProfiler(logger=logger)


async def save_screenshot(screenshot_data, filename):
    """Helper function to save a screenshot"""
    if not screenshot_data:
        logger.warning(f"No screenshot data available", tag="SCREENSHOT")
        return False
    
    try:
        screenshot_path = Path(filename)
        
        # Try to decode if it's base64 encoded
        if isinstance(screenshot_data, str):
            try:
                # If it starts with common base64 image prefixes
                if screenshot_data.startswith(('data:image', 'iVBOR', '/9j/')):
                    if screenshot_data.startswith('data:image'):
                        # Extract the base64 part after the comma
                        base64_data = screenshot_data.split(',', 1)[1]
                        screenshot_bytes = base64.b64decode(base64_data)
                    else:
                        # Just try to decode directly
                        screenshot_bytes = base64.b64decode(screenshot_data)
                else:
                    screenshot_bytes = screenshot_data.encode('utf-8')
            except:
                screenshot_bytes = screenshot_data.encode('utf-8')
        else:
            screenshot_bytes = screenshot_data
        
        # Write to file
        with open(screenshot_path, "wb") as f:
            f.write(screenshot_bytes)
        
        logger.success(f"Screenshot saved to {Fore.GREEN}{screenshot_path.absolute()}{Style.RESET_ALL}", tag="SCREENSHOT")
        return True
    except Exception as e:
        logger.error(f"Error saving screenshot: {str(e)}", tag="SCREENSHOT")
        return False


async def save_content(result, markdown_filename, html_filename):
    """Helper function to save scraped content"""
    if not result.success:
        logger.warning("No content to save - crawl was not successful", tag="CONTENT")
        return
    
    try:
        # Save markdown content
        md_output_file = Path(markdown_filename)
        md_output_file.write_text(result.markdown)
        logger.success(f"Markdown content saved to {Fore.GREEN}{md_output_file.absolute()}{Style.RESET_ALL}", tag="CONTENT")
        
        # Save HTML content
        html_output_file = Path(html_filename)
        html_output_file.write_text(result.html)
        logger.success(f"HTML content saved to {Fore.GREEN}{html_output_file.absolute()}{Style.RESET_ALL}", tag="CONTENT")
    except Exception as e:
        logger.error(f"Error saving content: {str(e)}", tag="CONTENT")


async def crawl_with_profile(profile_path, url):
    """Use a profile to crawl an authenticated page"""
    logger.info(f"Crawling {Fore.CYAN}{url}{Style.RESET_ALL}", tag="CRAWL")
    logger.info(f"Using profile at {Fore.YELLOW}{profile_path}{Style.RESET_ALL}", tag="CRAWL")
    
    # Create browser config with the profile path
    browser_config = BrowserConfig(
        headless=HEADLESS,
        verbose=True,
        browser_type=BROWSER_TYPE,
        use_managed_browser=True,  # Required for persistent profiles
        user_data_dir=profile_path
    )
    
    # Set up crawler configuration
    crawl_config = CrawlerRunConfig(
        screenshot=TAKE_SCREENSHOT,
        cache_mode=CacheMode.BYPASS,  # Don't use cache
        scan_full_page=True,  # Ensure we scan the full page
        wait_for_images=True,  # Wait for images to load
        js_code=f"await new Promise(resolve => setTimeout(resolve, {PRE_SCRAPE_WAIT_SECONDS * 1000})); return true;"
    )
    
    # Initialize crawler with the browser config
    async with AsyncWebCrawler(config=browser_config, logger=logger) as crawler:
        # Open browser but wait for user confirmation before crawling
        logger.info(f"{Fore.YELLOW}Browser window opened. Please complete any authorization or permission dialogs.{Style.RESET_ALL}", tag="AUTH")
        confirmation = input(f"{Fore.CYAN}Press Enter when you've completed authorization to continue with the crawl: {Style.RESET_ALL}")
        
        start_time = asyncio.get_event_loop().time()
        
        # Crawl the URL - You should have access to authenticated content now
        logger.info(f"Starting crawl...", tag="CRAWL")
        result = await crawler.arun(url, config=crawl_config)
        
        elapsed_time = asyncio.get_event_loop().time() - start_time
        
        if result.success:
            # Log success
            logger.success(f"Crawl successful! ({elapsed_time:.2f}s)", tag="CRAWL")
            
            # Print page title
            title = result.metadata.get("title", "Unknown Title")
            logger.info(f"Page title: {Fore.GREEN}{title}{Style.RESET_ALL}", tag="CRAWL")
            
            # Save screenshot if requested
            if TAKE_SCREENSHOT and hasattr(result, 'screenshot'):
                await save_screenshot(result.screenshot, SCREENSHOT_FILENAME)
            
            # Save content if requested
            if SAVE_CONTENT:
                await save_content(result, OUTPUT_MARKDOWN_FILENAME, OUTPUT_HTML_FILENAME)
            
            return result
        else:
            # Log error status
            logger.error(f"Crawl failed: {result.error_message}", tag="CRAWL")
            return None


async def main():
    logger.info(f"{Fore.CYAN}N8N Authentication Profile Example{Style.RESET_ALL}", tag="DEMO")
    
    # Choose between interactive mode and automatic mode
    mode_input = input(f"{Fore.CYAN}Run in [i]nteractive mode or [a]utomatic mode? (i/a): {Style.RESET_ALL}").lower()
    
    if mode_input == 'i':
        # Interactive profile management
        logger.info("Starting interactive profile manager...", tag="DEMO")
        await profiler.interactive_manager(crawl_callback=crawl_with_profile)
    else:
        # Automatic mode
        profiles = profiler.list_profiles()
        selected_profile = None
        
        # If a specific profile name was requested
        if PROFILE_NAME:
            for profile in profiles:
                if profile["name"] == PROFILE_NAME:
                    selected_profile = profile
                    break
        
        if selected_profile:
            logger.info(f"Using existing profile: {Fore.CYAN}{selected_profile['name']}{Style.RESET_ALL}", tag="DEMO")
            profile_path = selected_profile["path"]
        elif profiles:
            # Use the first profile if we have any
            selected_profile = profiles[0]
            logger.info(f"Using most recent profile: {Fore.CYAN}{selected_profile['name']}{Style.RESET_ALL}", tag="DEMO")
            profile_path = selected_profile["path"]
        else:
            # Create a new profile if none exists
            logger.info("No profiles found. Creating a new one...", tag="DEMO")
            logger.info(f"{Fore.YELLOW}IMPORTANT: Please log in to n8n in the browser window that will open.{Style.RESET_ALL}", tag="DEMO")
            logger.info(f"When finished, press 'q' in this terminal to save the profile.", tag="DEMO")
            
            profile_path = await profiler.create_profile()
            if not profile_path:
                logger.error("Cannot proceed without a valid profile", tag="DEMO")
                return
        
        # Verify profile path exists
        if not os.path.exists(profile_path):
            logger.warning(f"Profile path does not exist: {profile_path}", tag="DEMO")
            logger.info("Creating a new profile instead...", tag="DEMO")
            profile_path = await profiler.create_profile()
            if not profile_path:
                logger.error("Cannot proceed without a valid profile", tag="DEMO")
                return
        
        # Crawl the target URL
        await crawl_with_profile(profile_path, TARGET_URL)


if __name__ == "__main__":
    try:
        # Run the async main function
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Example interrupted by user", tag="DEMO")
    except Exception as e:
        logger.error(f"Error in example: {str(e)}", tag="DEMO") 