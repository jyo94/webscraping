import requests
from bs4 import BeautifulSoup
import json



base_url = "https://theamikusqriae.com/legal-articles/"
num_pages = 5

def clean_text(text):
    cleaned_text = text.strip()
    cleaned_text = ' '.join(cleaned_text.split())
    #U+00a0 #U+002d #U+2013
    cleaned_text = cleaned_text.replace(u'\xa0', '')
    cleaned_text = cleaned_text.replace(u'\u002d', '')
    cleaned_text = cleaned_text.replace(u'\u2013', '')
    return cleaned_text


def scrape_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")
            #class_="elementor-post__title"
            title_element = soup.find_all("h5", class_="elementor-post__title")
            titles = [clean_text(title.get_text()) for title in title_element]
            #class="elementor-post__excerpt"
            content_element = soup.find_all(class_="elementor-post__excerpt")
            contents = [clean_text(content.get_text()) for content in content_element]
            data = [{"title": title, "content": content} for title, content in zip(titles, contents)]
            return data
        else:
            print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while scraping {url}: {str(e)}")
        return None

#function to paginate and scrape multiple pages
def scrape_multiple_pages(base_url, num_pages):
    all_data = []
    for page_num in range(1, num_pages + 1):
        url = f"{base_url}page/{page_num}/"
        data = scrape_page(url)
        if data:
            all_data.append(data)
    return all_data

def main():
    scraped_data = scrape_multiple_pages(base_url, num_pages)
    # Write to JSON
    with open("scraped_data.json", "w", encoding="utf-8") as json_file:
        json.dump(scraped_data, json_file, ensure_ascii=False, indent=4)
    print("Scraping completed. Data saved to scraped_data.json")

if __name__ == "__main__":
    main()
