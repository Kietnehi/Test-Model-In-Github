#!/usr/bin/env python3
"""
Browser Profile Manager for Crawl4AI

This script helps manage browser profiles for identity-based crawling with Crawl4AI.
It allows users to create, list, delete, and test profiles for authenticated browsing.
"""

import asyncio
import sys
import time
from pathlib import Path
from crawl4ai import BrowserProfiler, AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

# Default wait time for system prompts (like keychain access)
SYSTEM_PROMPT_WAIT = 5

async def create_or_update_profile(profiler, profile_name=None, initial_url=None):
    """
    Create a new profile or update an existing one.
    
    Args:
        profiler: BrowserProfiler instance
        profile_name: Optional name for the profile
        initial_url: Optional URL to open initially (for user guidance only)
    
    Returns:
        Path to the created/updated profile or None if cancelled
    """
    try:
        # Get profile name if not provided
        if profile_name is None:
            profile_name = input("Enter profile name (e.g., facebook-profile): ").strip()
            if not profile_name:
                print("Profile name cannot be empty.")
                return None

        # Check if profile exists
        existing_path = profiler.get_profile_path(profile_name)
        if existing_path:
            print(f"Profile '{profile_name}' already exists at: {existing_path}")
            update = input("Do you want to update this profile? (y/n): ").strip().lower()
            if update != 'y':
                return None

        # Get initial URL if not provided (for instruction purposes only)
        if initial_url is None:
            initial_url = input("\nEnter URL you plan to visit first (leave empty for blank page): ").strip()
        
        # User instructions
        print("\nA browser window will open. Please:")
        print("1. Log in to the websites you want to access")
        if initial_url:
            print(f"   (Navigate to {initial_url} first)")
        print("2. Configure any other browser settings as needed")
        print("3. When finished, return to this terminal and press 'q' to save the profile")
        input("\nPress Enter to continue...")
        
        # Create the profile interactively
        print("\nOpening browser window. Log in to your accounts and set up your preferences...")
        profile_path = await profiler.create_profile(profile_name=profile_name)
        
        print(f"\nProfile successfully {'updated' if existing_path else 'created'} and saved at: {profile_path}")
        print(f"\nYou can now use this profile with crawl_with_profile.py by setting PROFILE_NAME = '{profile_name}'")
        
        return profile_path
    except Exception as e:
        print(f"Error creating/updating profile: {str(e)}")
        return None

def list_profiles(profiler):
    """
    List all available profiles.
    
    Args:
        profiler: BrowserProfiler instance
    
    Returns:
        List of profile dictionaries or empty list if none found
    """
    try:
        profiles = profiler.list_profiles()
        if not profiles:
            print("\nNo profiles found.")
            return []
        
        print("\nAvailable profiles:")
        for i, profile in enumerate(profiles, 1):
            print(f"{i}. {profile['name']} (Created: {profile['created']})")
            print(f"   Path: {profile['path']}")
            print(f"   Browser type: {profile['type']}")
            print()
        
        return profiles
    except Exception as e:
        print(f"Error listing profiles: {str(e)}")
        return []

def delete_profile(profiler):
    """
    Delete a selected profile.
    
    Args:
        profiler: BrowserProfiler instance
    """
    try:
        profiles = profiler.list_profiles()
        if not profiles:
            print("\nNo profiles found to delete.")
            return
        
        print("\nSelect a profile to delete:")
        for i, profile in enumerate(profiles, 1):
            print(f"{i}. {profile['name']} (Created: {profile['created']})")
        
        try:
            choice = int(input("\nEnter profile number to delete (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(profiles):
                profile_name = profiles[choice-1]['name']
                confirm = input(f"Are you sure you want to delete profile '{profile_name}'? (y/n): ").strip().lower()
                
                if confirm == 'y':
                    success = profiler.delete_profile(profile_name)
                    if success:
                        print(f"Profile '{profile_name}' deleted successfully.")
                    else:
                        print(f"Failed to delete profile '{profile_name}'.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
    except Exception as e:
        print(f"Error deleting profile: {str(e)}")

async def test_profile(profiler):
    """
    Test a profile by crawling a specified URL.
    
    Args:
        profiler: BrowserProfiler instance
    """
    try:
        profiles = list_profiles(profiler)
        if not profiles:
            return
        
        try:
            choice = int(input("\nEnter profile number to test (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(profiles):
                profile_name = profiles[choice-1]['name']
                profile_path = profiles[choice-1]['path']
                browser_type = profiles[choice-1]['type']
                
                url = input("\nEnter URL to test crawling (e.g., https://example.com): ").strip()
                if not url:
                    print("URL cannot be empty.")
                    return
                
                headless = input("Run in headless mode? (y/n, default: n): ").strip().lower() == 'y'
                take_screenshot = input("Take screenshot? (y/n, default: y): ").strip().lower() != 'n'
                
                print(f"\nTesting profile '{profile_name}' on {url}...")
                
                # Configure the browser with the profile
                browser_config = BrowserConfig(
                    headless=headless,
                    verbose=True,
                    browser_type=browser_type,
                    use_managed_browser=True,
                    user_data_dir=profile_path
                )
                
                # Set up crawler configuration
                crawl_config = CrawlerRunConfig(
                    screenshot=take_screenshot,
                    cache_mode=CacheMode.BYPASS,
                )
                
                # Initialize the crawler
                async with AsyncWebCrawler(config=browser_config) as crawler:
                    # Add a delay for potential system prompts
                    wait_time = int(input(f"Wait time for system prompts (default: {SYSTEM_PROMPT_WAIT} seconds): ") or SYSTEM_PROMPT_WAIT)
                    print(f"\nWaiting {wait_time} seconds for potential system prompts...")
                    time.sleep(wait_time)
                    
                    # Proceed with the actual crawling
                    result = await crawler.arun(url=url, config=crawl_config)
                    
                    if result.success:
                        print("\nCrawling successful!")
                        
                        # Save screenshot if available
                        if result.screenshot and take_screenshot:
                            screenshot_file = Path(f"test_{profile_name}_screenshot.png")
                            with open(screenshot_file, "wb") as f:
                                f.write(result.screenshot)
                            print(f"Screenshot saved to {screenshot_file.absolute()}")
                        
                        # Ask if user wants to save the content
                        save_content = input("\nSave crawled content? (y/n): ").strip().lower() == 'y'
                        if save_content:
                            output_file = Path(f"test_{profile_name}_content.md")
                            output_file.write_text(result.markdown)
                            print(f"Content saved to {output_file.absolute()}")
                    else:
                        print(f"\nError: {result.error_message}")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred during testing: {str(e)}")

async def main():
    """Main function that presents the interactive menu."""
    try:
        # Initialize the BrowserProfiler
        profiler = BrowserProfiler()
        
        while True:
            print("\n===== Browser Profile Manager =====")
            print("1. Create/Update Profile")
            print("2. List Available Profiles")
            print("3. Delete Profile")
            print("4. Test Profile")
            print("5. Exit")
            
            try:
                choice = input("\nEnter your choice (1-5): ").strip()
                
                if choice == '1':
                    await create_or_update_profile(profiler)
                elif choice == '2':
                    list_profiles(profiler)
                elif choice == '3':
                    delete_profile(profiler)
                elif choice == '4':
                    await test_profile(profiler)
                elif choice == '5':
                    print("Exiting Profile Manager.")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
            except Exception as e:
                print(f"Error processing menu choice: {str(e)}")
                print("Please try again.")
    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Unhandled exception: {str(e)}")
        sys.exit(1) 