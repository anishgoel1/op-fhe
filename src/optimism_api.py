import requests
from logger import Logger
from typing import Any, Dict, Optional, Union

class OptimismAPI:
    def __init__(self, api_key: str) -> None:
        """
        Initialize the OptimismAPI with the given API key.

        :param api_key: The API key for authenticating requests.
        """
        self.api_key = api_key
        self.base_url = "https://api-optimistic.etherscan.io/api"
        self.logger = Logger()

    def fetch_data(self, module: str, action: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Fetch data from the Optimism API.

        :param module: The module to query.
        :param action: The action to perform.
        :param params: Additional parameters for the request.
        :return: The JSON response as a dictionary if successful, None otherwise.
        """
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

    def get_block_rewards(self, blockno: int) -> Optional[Dict[str, Any]]:
        """
        Get block rewards for a specific block number.

        :param blockno: The block number.
        :return: The JSON response as a dictionary if successful, None otherwise.
        """
        return self.fetch_data("block", "getblockreward", {"blockno": blockno})

    def get_daily_avg_block_time(self, startdate: str, enddate: str) -> Optional[Dict[str, Any]]:
        """
        Get the daily average block time between two dates.

        :param startdate: The start date in YYYY-MM-DD format.
        :param enddate: The end date in YYYY-MM-DD format.
        :return: The JSON response as a dictionary if successful, None otherwise.
        """
        return self.fetch_data("stats", "dailyavgblocktime", {"startdate": startdate, "enddate": enddate})

    def get_daily_block_rewards(self, startdate: str, enddate: str) -> Optional[Dict[str, Any]]:
        """
        Get the daily block rewards between two dates.

        :param startdate: The start date in YYYY-MM-DD format.
        :param enddate: The end date in YYYY-MM-DD format.
        :return: The JSON response as a dictionary if successful, None otherwise.
        """
        return self.fetch_data("stats", "dailyblockrewards", {"startdate": startdate, "enddate": enddate})

    def get_block_by_number(self, blockno: Union[int, str]) -> Optional[Dict[str, Any]]:
        """
        Get block details by block number.

        :param blockno: The block number or 'latest' for the latest block.
        :return: The JSON response as a dictionary if successful, None otherwise.
        """
        if blockno == 'latest':
            return self.fetch_data("proxy", "eth_blockNumber", {})
        else:
            return self.fetch_data("proxy", "eth_getBlockByNumber", {"tag": hex(blockno), "boolean": "true"})

    def get_block_countdown(self, blockno: int) -> Optional[Dict[str, Any]]:
        """
        Get the countdown for a specific block number.

        :param blockno: The block number.
        :return: The JSON response as a dictionary if successful, None otherwise.
        """
        return self.fetch_data("block", "getblockcountdown", {"blockno": blockno})

    def get_block_number_by_time(self, timestamp: int) -> Optional[Dict[str, Any]]:
        """
        Get the block number closest to a specific timestamp.

        :param timestamp: The timestamp in seconds since the Unix epoch.
        :return: The JSON response as a dictionary if successful, None otherwise.
        """
        return self.fetch_data("block", "getblocknobytime", {"timestamp": timestamp, "closest": "before"})