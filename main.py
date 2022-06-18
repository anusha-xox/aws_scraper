from pprint import pprint
import requests
from bs4 import BeautifulSoup

json_page_link = "https://aws.amazon.com/api/dirs/items/search?item.directoryId=customer-references&sort_by=item" \
                 ".additionalFields.sortDate&sort_order=desc&size=100&item.locale=en_US&page=3 "
response = requests.get(json_page_link).json()
# pprint(response)

card_links = []
for i in range(9):
    card_links.append(response["items"][i]['item']['additionalFields']['headlineUrl'])
print(card_links)

for i in range(len(card_links)):
    response = requests.get(card_links[i]).text
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
