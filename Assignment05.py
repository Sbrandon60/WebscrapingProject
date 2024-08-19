# CSCI 355 Web Technologies
# Summer 2024
# Brandon Sanichar
# Assignment5 - Data Scraping
# Worked by myself
# Websites used

# [1] Install and import these third-party libraries which are needed in the tasks below
import requests
import html5lib
from bs4 import BeautifulSoup
import OutputUtil as ou


# [2] Define a function to print the HTML content of a webpage at a given URL (uniform resource locator, web address)
def print_html_content(url):
    r = requests.get(url)
    print(r.content)

# [3] Define a function to parse the HTML content for a given URL.
def parse_html_content(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    print(soup.prettify())

# [4] Define a function to get the next text item from an iterator
def next_text(itr):
    return next(itr).text

# [5] Define a function to get the next int item from an iterator
def next_int(itr):
    return int(next_text(itr).replace(',', ''))


# [6] Define a function to scrape the site.
def scrape_covid_data():
    dict_country_population = get_country_population()
    url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = []
    # soup.find_all('td') will scrape every table-data element in the url's table
    data_iterator = iter(soup.find_all('td'))
    # This loop will keep repeating as long as there is data available in the iterator
    while True:
        try:
            country = next_text(data_iterator)
            if country.startswith("Japan"):
                country = "Japan"
            cases = next_int(data_iterator)
            deaths = next_int(data_iterator)
            continent = next_text(data_iterator)
            if country in dict_country_population:
                population = dict_country_population[country]  # placeholder - will be replaced in next task
                cases_per_capita = round(cases/population, 2)
                percent_deaths = round((deaths/cases) *100, 2)
                data.append([country, continent, population, cases, deaths, cases_per_capita, percent_deaths])
            else:
                print(f"Country {country} not found in population data.")

        # StopIteration error is raised when there are no more elements left for iteration
        except StopIteration:
            break

    # Sort the data by country name
    data.sort(key=lambda row: row[0])

    headers = ['Country', 'Continent', 'Population', 'Cases', 'Deaths', 'Cases per Capita', 'Percent Deaths']

    return headers, data

# [7] Define a function get_country_population(url) that will scrape this website to get country populations:  https://www.worldometers.info/world-population/population-by-country/. Build a dictionary in which the keys are country names and the values are country populations.
def get_country_population():
    dict_country_population = {}
    url = 'https://www.worldometers.info/world-population/population-by-country/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data_iterator = iter(soup.find_all('td'))

    while True:
        try:
            junk1 = next_text(data_iterator)
            country = next_text(data_iterator)
            population = next_int(data_iterator)
            junk4 = next_text(data_iterator)
            junk5 = next_text(data_iterator)
            junk6 = next_text(data_iterator)
            junk7 = next_text(data_iterator)
            junk8 = next_text(data_iterator)
            junk9 = next_text(data_iterator)
            junk10 = next_text(data_iterator)
            junk11 = next_text(data_iterator)
            junk12 = next_text(data_iterator)

            dict_country_population[country] = population

            # print(f"Junk1: {junk1}, Junk2: {country}, Junk3: {population}, Junk4: {junk4}, Junk5: {junk5}")
            # print(f"Junk6: {junk6}, Junk7: {junk7}, Junk8: {junk8}, Junk9: {junk9}, Junk10: {junk10}, Junk11: {junk11}, Junk12: {junk12}")
        # StopIteration error is raised when there are no more elements left for iteration
        except StopIteration:
            break

    return dict_country_population

# [8] Add this population data to the previously scraped data. This is important information because the numbers of COVID cases and deaths per country are more significant relative to that country's population.


def main():
    # print_html_content('https://www.google.com')
    # parse_html_content('https://www.google.com')
    headers, data = scrape_covid_data()
    title = "Covid Data by Country"
    types = ["S", "S", "N", "N", "N", "N", "N"]
    alignments = ["L", "L", "R", "R", "R", "R", "R"]
    ou.write_html_file("Assignment05.html", title, headers, types, alignments, data, True)
    ou.write_xml_file("Assignment05.xml", title, headers, data, True)



if __name__ == "__main__":
    main()
