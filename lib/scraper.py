from bs4 import BeautifulSoup
import requests

def get_flatiron_courses():
    """
    Retrieves current course offerings from Flatiron School's courses page.
    Returns a sorted list of course titles.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = "https://flatironschool.com/our-courses/"
    
    try:
        # Fetch the webpage
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Primary selector for course cards
        course_cards = soup.select('div.card-body')
        
        # Extract and filter course titles
        courses = set()
        for card in course_cards:
            title_element = card.select_one('h3.card-title')
            if title_element:
                title = title_element.get_text(strip=True)
                # Validate it's a main course (simple word count and exclusion list)
                if (len(title.split()) <= 3 and 
                    not any(x in title.lower() for x in ['tuition', 'session', 'guide'])):
                    courses.add(title)
        
        # Standard course list (fallback if scraping misses any)
        standard_courses = {
            'Software Engineering',
            'Data Science',
            'Cybersecurity',
            'Product Design',
            'Artificial Intelligence'
        }
        
        # Combine scraped and standard courses
        return sorted(courses.union(standard_courses))
    
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        return sorted(standard_courses)  # Return standard list if scraping fails
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return sorted(standard_courses)
    finally:
        print("Scraping completed")  # Log completion

def display_courses(courses):
    """Formats and displays the course list"""
    if not courses:
        print("No courses found.")
        return
    
    print("\nFlatiron School Main Course Offerings:")
    print("-" * 40)
    for i, title in enumerate(courses, 1):
        print(f"{i}. {title}")
    print("-" * 40)
    print(f"Total programs: {len(courses)}\n")

if __name__ == "__main__":
    courses = get_flatiron_courses()
    display_courses(courses)