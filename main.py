# https://aws.amazon.com/solutions/case-studies/

from pprint import pprint
import requests
from bs4 import BeautifulSoup

card_links = []
errored = []

for i in range(1,240):
    json_page_link = f"https://aws.amazon.com/api/dirs/items/search?item.directoryId=customer-references&sort_by=itemadditionalFields.sortDate&sort_order=desc&size=100&item.locale=en_US&page={i}"
    response = requests.get(json_page_link).json()
    # pprint(response)

    for j in range(9):
        card_links.append(response["items"][j]['item']['additionalFields']['headlineUrl'])

    for j in range(len(card_links)):
        try:
            response = requests.get(card_links[j]).text
            soup = BeautifulSoup(response, "html.parser")
            # print(soup)

            testimonial = soup.find(class_="lb-txt-bold lb-txt-18 lb-none-v-margin lb-rtxt").getText()
            print(testimonial)
            person_name = soup.find("b").getText()
            print(person_name)

            person_designation = soup.find_all("i")[9].getText()
            print(person_designation)

            aws_services = [service.getText() for service in soup.find_all(class_="lb-txt-none lb-h3 lb-title")]
            aws_services = aws_services[3:len(aws_services)]
            print(aws_services)
        except AttributeError:
            errored.append(card_links[j])

print(len(card_links))
print(card_links)
print(len(errored))
print(errored)

# testemonial class="lb-txt-bold lb-txt-18 lb-none-v-margin lb-rtxt"
# lb-rtxt, bold
