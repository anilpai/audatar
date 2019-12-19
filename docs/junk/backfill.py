import requests
from audatar import audatar_config
import json
import logging
import datetime

token = audatar_config.token


''' Start date is N days ago from now.'''
N = 30


start_date = datetime.datetime.now() - datetime.timedelta(days=N)
end_date = datetime.datetime.now()
page_size = 50
page_number = 1

r = requests.get('{0}/vci/?start_date={1}&end_date={2}&pageNumber={3}&pageSize={4}'.format(audatar_config.api_url,
                                                                                           start_date,
                                                                                           end_date,
                                                                                           page_number, page_size),
                 headers={'accept': 'application/json', 'Authorization': 'Bearer ' + token})

print(r.json())
count = r.json()['count']
total_pages = int(count / page_size) + 1
print(count, total_pages)
s_200 = []
s_not_200 = []

while page_number <= total_pages:

    x = 0
    while x < 50:
        r = requests.get(
            '{0}/vci/?start_date={1}&end_date={2}&pageNumber={3}&pageSize={4}'.format(audatar_config.api_url,
                                                                                      start_date,
                                                                                      end_date,
                                                                                      page_number, page_size),
            headers={'accept': 'application/json', 'Authorization': 'Bearer ' + token})

        try:
            vci_id = r.json()['data'][x]['id']
            print(vci_id)
        except Exception as e:
            print(str(e))
            print("Out of bounds")

        dr_parameters = {'vci_id': vci_id}
        """ Send Results to Data Registry"""
        s = requests.post('{0}/notification/send_ds'.format(audatar_config.api_url),
                          data=json.dumps(dr_parameters, indent=4), headers=audatar_config.headers)
        print(s.status_code)

        if not s.status_code == 200:
            s_not_200.append(vci_id)
        logging.info('Sent results to Data Registry.')
        x = x + 1
    page_number = page_number + 1


print(s_not_200)
