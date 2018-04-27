import requests

from . import misc


class Plexpy:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    def get_stream_counts(self):
        transcodes, direct_plays, direct_streams = 0, 0, 0
        try:
            req = requests.get("{}/api/v2?apikey={}&cmd=get_activity".format(self.url, self.api_key)).json()['response']
            transcodes = req['data']['stream_count_transcode']
            direct_plays = req['data']['stream_count_direct_play']
            direct_streams = req['data']['stream_count_direct_stream']
        except Exception:
            pass
        return transcodes, direct_plays, direct_streams

    def get_stream_bandwidth(self):
        stream_bandwidth = 0
        try:
            req = requests.get("{}/api/v2?apikey={}&cmd=get_activity".format(self.url, self.api_key)).json()['response']
            stream_bandwidth = req['data']['total_bandwidth']
        except Exception:
            pass
        return misc.kbps_to_string(stream_bandwidth)