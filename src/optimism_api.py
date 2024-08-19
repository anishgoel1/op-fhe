import requests
from logger import Logger

class OptimismAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api-optimistic.etherscan.io/api"
        self.logger = Logger()

    def fetch_data(self, module, action, params):
        try:
            url = "{}?module={}&action={}&apikey={}".format(self.base_url, module, action, self.api_key)
            for key, value in params.items():
                url += "&{}={}".format(key, value)
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.log_error("Failed to fetch data: {}".format(response.status_code))
                return None
        except requests.exceptions.RequestException as e:
            self.logger.log_error("Request failed: {}".format(e))
            return None

    def get_block_rewards(self, blockno):
        return self.fetch_data("block", "getblockreward", {"blockno": blockno})

    def get_daily_avg_block_time(self, startdate, enddate):
        return self.fetch_data("stats", "dailyavgblocktime", {"startdate": startdate, "enddate": enddate})

    def get_daily_block_rewards(self, startdate, enddate):
        return self.fetch_data("stats", "dailyblockrewards", {"startdate": startdate, "enddate": enddate})

    def get_block_by_number(self, blockno):
        if blockno == 'latest':
            return self.fetch_data("proxy", "eth_blockNumber", {})
        else:
            return self.fetch_data("proxy", "eth_getBlockByNumber", {"tag": hex(blockno), "boolean": "true"})

    def get_block_countdown(self, blockno):
        return self.fetch_data("block", "getblockcountdown", {"blockno": blockno})

    def get_block_number_by_time(self, timestamp):
        return self.fetch_data("block", "getblocknobytime", {"timestamp": timestamp, "closest": "before"})