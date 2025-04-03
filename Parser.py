from bs4 import BeautifulSoup
from csv import DictWriter

class Parser:
    def __init__(self, raw_html_file, selector):
        self.soup = BeautifulSoup(raw_html_file, features="html.parser")
        self.tags = self.find_tags(selector)
        self.scraped_data = []

    # Retrieve a list of html tags
    def find_tags(self, selector):
        tags_found = self.soup.select(selector)
        if not tags_found:
            print("No elements found with tag "+ selector)
            return None
        self.tags = tags_found
        return tags_found


    # Retrieve text from a list of tags
    def extract_text(self, tags):
        return [tag.text for tag in tags]


    # Retrieve attributes content from a list of tags
    def extract_attribute(self, attribute, tags):
        return [tag.get(attribute) for tag in tags]


    # Organise scraped data in dictionaries
    def get_contents(self, keys):
        for tag in self.tags:
            for key in keys:
                pass
    

    def setup_csv_file(self, new_csv_file, fieldnames):
        self.fieldnames = fieldnames
        self.writer = DictWriter(csvfile, fieldnames=fieldnames)
        with open(new_csv_file, "w") as csvfile:
            self.writer.writeheader() 

    def save_lead_to_csv(file, lead):
        with open(file, mode="a") as csvfile:
            fieldnames = ["practice", "city", "email", "website"]
            writer = DictWriter(csvfile,fieldnames=fieldnames)
            writer.writerow(lead)


raw_data = "raw_data/index1.html"
selector = "div.directory-preview > a"
attribute = 'href'
keys = [{'path': 'href', 'type': 'attribute'}]

with open(raw_data) as file:
    p = Parser(file, selector)
    print(p.extract_attribute(tags=p.tags, attribute=attribute))