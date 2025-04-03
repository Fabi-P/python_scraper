import requests
from bs4 import BeautifulSoup
import json
import time
import os
from dotenv import load_dotenv
import csv
import re

load_dotenv()

# Get html from url and return a soup obj
def scrape_website(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return []
    
    return BeautifulSoup(response.text, 'html.parser')


def soup_to_file(soup, filename):
    with open(filename, "w") as file:
        file.write(str(soup))

def soup_from_file(file):
    with open(file) as file:
        return BeautifulSoup(file)

def get_target_links(soup):
    container = os.getenv("TARGET_CONTAINER")
    container_class = os.getenv("TARGET_CONTAINER_CLASS")

    links = []
    
    entries = soup.find_all(container, class_=container_class)
    name = "N/A"
    place = "N/A"
    link = "N/A"

    for entry in entries:
        try:
            name = entry.find(os.getenv("TARGET_NAME_ELEMENT")).contents[0]
            place = entry.find(os.getenv("TARGET_PLACE_ELEMENT")).contents[0]
            link = entry.find(os.getenv("TARGET_LINK_ELEMENT")).get(os.getenv("TARGET_LINK_ATTRIBUTE"))
        except IndexError:
            print("entry detail not found in index page for entry")
        finally:
            links.append({"practice": name, "city": place, "website": link})
    return links

def get_data_from_link(link):
    dynamic_url = os.getenv("BASE_URL") + link["website"]
    soup = scrape_website(dynamic_url)
    soup_to_file(soup=soup, filename="data.html")
    #soup = soup_from_file("data.html")
    email = "N/A"
    website = "N/A"
    try:
        container = soup.find("div", class_="container-fluid directory-info-block")
        email = container.find("a", attrs={"href": re.compile("^mailto:")}).contents[0]
        website = container.find("a", attrs={"href": re.compile("^http")}).contents[0]
    except AttributeError:
        print("error at finding attributes for "+ link["practice"])
    finally:
        link["email"] = email
        link["website"] = website

    return link

def setup_csv_file(file):
    with open(file, "w") as csvfile:
        fieldnames = ["practice", "city", "email", "website"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()   

def save_lead_to_csv(file, lead):
    with open(file, mode="a") as csvfile:
        fieldnames = ["practice", "city", "email", "website"]
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writerow(lead)

if __name__ == "__main__":
    # soup = scrape_website("https://www.rias.org.uk/for-the-public/practices?offset=192&location=Edinburgh&distance=24&practicename=&specialism=")
    # soup_to_file(soup=soup, filename="index5.html")
    soup = soup_from_file("index1.html")
    links = get_target_links(soup)
    for i in range(0, 1):
        save_lead_to_csv(file="leads.csv", lead=get_data_from_link(links[i]))
