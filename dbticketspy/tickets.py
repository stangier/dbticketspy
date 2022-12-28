import requests

from dataclasses import dataclass
import xml.etree.ElementTree as ET

API_ENDPOINT = "https://fahrkarten.bahn.de/mobile/dbc/xs.go?"

@dataclass
class Train:
    type: str
    number: int
    departure: str
    destination: str

@dataclass
class Ticket:
    ticketNumber: str
    orderNumber: str
    barcode: str
    trains: list[Train]

def query_ticket(orderNumber: str, lastName: str) -> Ticket:
    """Get ticket information from the DB website, based on a order number and a last name.

    Args:
        orderNumber (str): The order numbver of the ticket (e.g. ASDQWE).
        lastName (str): The last name of the person who booked the ticket.

    Raises:
        KeyError: Raised if the ticket number and last name combination is not found.

    Returns:
        Ticket: A Ticket object containing the ticket information.
    """    

    headers = {
        "User-Agent": "dbticketspy",
        "Accept-Language": "de-DE,de,q=0.9",
    }

    request_body = '<?xml version="1.0"?><rqorderdetails version="1.0">' \
        + '<rqheader tnr="61743782011" ts="2022-07-15T22:29:00" l="de" v="22060000" d="iPhone13,1" os="iOS_15.5" app="NAVIGATOR"/>' \
        + f'<rqorder on="{orderNumber}"/><authname tln="{lastName}"/></rqorderdetails>'

    response = requests.post(url=API_ENDPOINT, data=request_body, headers=headers)

    xml_tree = ET.fromstring(response.text)

    if xml_tree.tag == "rperror":
        raise KeyError("Ticket/Name combination not found")

    header = xml_tree.find("rpheader")
    order = xml_tree.find("order")
    
    order_number = order.attrib["on"]
    barcode = order.find("tcklist").find("tck").find("htdata").find("ht").text
    ticket_number = header.attrib["tnr"]

    trainlist = order.find("schedulelist").find("out").find("trainlist")
    trains = []
    for train in trainlist.findall("train"):
        trains.append(Train(train.find("gat").text,
                            train.find("zugnr").text,
                            train.find("dep").find("n").text,
                            train.find("arr").find("n").text))

    return Ticket(ticket_number, order_number, barcode, trains)

