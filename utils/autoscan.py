import requests


class Autoscan:
    def __init__(self, url, api_key):
        self.url = '%s/api/%s' % (url, api_key)

    def get_queue_count(self):
        count = 0
        try:
            payload = {'cmd': 'queue_count'}
            resp = requests.post(self.url, json=payload, timeout=10)
            if 'json' in resp.headers['Content-Type'].lower() and 'queue_count' in resp.content:
                count = resp.json()['queue_count']
        except Exception:
            pass
        return count
