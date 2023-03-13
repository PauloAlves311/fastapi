import xmltodict
import xml.etree.ElementTree as ET

import requests
import json


def downloadData():
    URL = "http://services.ximo.pt/export_xml_base/default.aspx?h=704ED61D-335D-46AF-813E-00DD2E2BB6F4&p=MFWLFBRPVSAXGBHWCZQLMBSDFBUJY-422377&l=en"

    response = requests.get(URL)
    content = response.content

    with open('feed.xml', 'wb') as file:
        file.write(response.content)

    root = ET.parse("feed.xml").getroot()

    xmlstring = ET.tostring(root)
    xmldict = xmltodict.parse(xmlstring)

    with open('data.json', 'w') as f:
        json.dump(xmldict, f)


# file = open('data.json')
# data = json.load(file)