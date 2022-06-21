# https://aws.amazon.com/solutions/case-studies/

from pprint import pprint
import requests
from bs4 import BeautifulSoup
import pandas
import json

resultant_json = []


def transactionInit(vendor, company_added, person, desig, quote, services_applied, url):
    onet = {
        'vendor': vendor,
        'customer': company_added,
        'transaction': {
            'company_name': company_added,
            'person_name': person,
            'designation': desig,
            'testimonial': quote,
            'aws_services': services_applied,
            'url': url,
        }
    }
    resultant_json.append(onet)
    return onet


card_links = []
successful_links = []
errored_links = []

company = []
names = []
designations = []
testimonials = []
aws_services = []

for i in range(1,24):
    json_page_link = f"https://aws.amazon.com/api/dirs/items/search?item.directoryId=customer-references&sort_by=item.additionalFields.sortDate&sort_order=desc&size=9&item.locale=en_US&page={i}"
    response = requests.get(json_page_link).json()
    # pprint(response)

    for j in range(9):
        card_url = response["items"][j]['item']['additionalFields']['headlineUrl']
        card_links.append(card_url)

    for j in range(len(card_links)):
        try:
            response = requests.get(card_links[j]).text
            soup = BeautifulSoup(response, "html.parser")

            person_name = soup.find("b").getText()
            if person_name in names:
                pass
            else:
                successful_links.append(card_links[j])

                names.append(person_name)
                print(person_name)

                testimonial = soup.find(class_="lb-txt-bold lb-txt-18 lb-none-v-margin lb-rtxt").getText()
                testimonials.append(testimonial)
                print(testimonial)

                person_details = soup.find_all("i")[9].getText()
                print(person_details)
                try:
                    comma_details = person_details
                    comma_details = comma_details.split(', ')
                    person_designation = comma_details[0]
                    company_name = comma_details[1]
                except IndexError:
                    at_details = person_details
                    if at_details.split('at')[1]:
                        at_details = at_details.split('at')
                        person_designation = at_details[0]
                        company_name = at_details[1]
                    else:
                        person_designation, company_name = person_details

                designations.append(person_designation)
                print(person_designation)
                company.append(company_name)
                print(company_name)

                services = [service.getText() for service in soup.find_all(class_="lb-txt-none lb-h3 lb-title")]
                services = services[len(services)-4:len(services)]
                for service in services:
                    if "Learn More" in service:
                        services.remove(service)
                aws_services.append(services)
                print(services)

                transactionInit("Amazon", company_name, person_name, person_designation, testimonial, services,
                                card_links[j])

        except AttributeError:
            # errored_links.append(card_links[j])
            pass

    print(len(card_links))
    print(len(successful_links))
    print(successful_links)
    # print(len(errored_links))
    # print(errored_links)
    print(len(company))
    print(company)

csv_file_content = {"Person-name": names, "card-url": successful_links}
df = pandas.DataFrame(csv_file_content)
df.to_csv('card_details.csv')

with open("Dataset.json", "w") as f:
    json.dump(resultant_json, f)

# testemonial class="lb-txt-bold lb-txt-18 lb-none-v-margin lb-rtxt"
# lb-rtxt, bold
