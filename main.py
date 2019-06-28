import os
import csv
from sendgrid import SendGridAPIClient
import json

client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY')).client
lists = json.loads(client.contactdb.lists.get().body).get('lists')

def get_all_lists() -> dict:
    return json.loads(client.contactdb.lists.get().body).get('lists')

def recipients(list_id: int, page: int) -> list:
    try:
        res = client.contactdb.lists._(list_id).recipients.get(query_params={'page': page, 'page_size':1000})
    except:
        return []

    recipants = json.loads(res.body)
    return [r.get('email') for r in recipants.get('recipients')]



def loop(list_id: int) -> set:
    mail_set = set()
    for i in range(1,3000):
        emails = recipients(list_id, i)
        if emails == []:
            break
        mail_set = mail_set | set(emails)
    return mail_set

def writecsv(name: str, mails_set: set) -> None:
    with open(f'{name}.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['email'])
        for m in sorted(list(mails_set)):
            writer.writerow([m])


if __name__ == '__main__':
    all_lists = get_all_lists()
    for lists in all_lists:
        list_id = lists['id']
        list_name = lists['name']
        member = loop(list_id)
        writecsv(list_name, member)
