import requests

class Scraper:
    def __init__(self, url, payload, filepath):
        response = self.scrape_website(url, payload)
        if response is not None:
            self.html_to_file(response, filepath)
            self.raw_data = filepath

    # Get html from a web page
    def scrape_website(self, url, payload:None):
        try:
            response = requests.get(url, params=payload, timeout=10)
        except Exception as e:
            print("Request failed to retrieve the page. ", repr(e))
            return None
        else:
            print("Page has been scraped")
            return response.text


    # Save raw html into a file for later processing of data
    def html_to_file(self, raw_html, filepath):
        with open(filepath, "x") as file:
            file.write(raw_html)
        print("Raw html saved in file: " + filepath)
