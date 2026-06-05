import requests
import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)

class HRApiClient:
    """
    REST API client for fetching external HR and
    labor market data to enrich internal analytics.
    """

    def __init__(self, base_url: str, timeout: int = 10):
        # store base_url and timeout
        # initialize a requests.Session()
        # log initialization
        # Store the base URL and timeout as instance attributes
        self.base_url = base_url
        self.timeout = timeout

        # Initialize a persistent requests Session
        self.session = requests.Session()

       
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

        # Log that the client has been initialized successfully
        logger.info(f"HRApiClient initialized for base URL: {self.base_url} (Timeout: {self.timeout}s)")

    def _make_request(self, endpoint: str, params: dict = None) -> Optional[dict]:
        """
        Private method: make a GET request with error handling.
        Retries once on failure before returning None.
        Never crashes the pipeline.
        """
        # Construct the full URL by combining base_url and endpoint or take full URL
        if endpoint.startswith(("http://", "https://")):
            url = endpoint
        else:
            url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        # Max attempts = 2 (Original attempt + 1 retry)
        max_attempts = 2
        
        for attempt in range(1, max_attempts + 1):
            try:
                logger.info(f"Making GET request to {url} (Attempt {attempt}/{max_attempts})")
                
                # Use the session initialized in __init__
                response = self.session.get(url, params=params, timeout=self.timeout)
                
                # Raises an HTTPError if the status code is 4XX or 5XX
                response.raise_for_status()
                
                # If successful, parse and return the JSON data
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt} failed. Error: {e}")
                
                # If this was the first attempt, wait briefly before retrying
                if attempt < max_attempts:
                    time.sleep(2)  # Pause for 2 seconds to let network stabilize
                else:
                    # Explanatory log if all attempts completely fail
                    logger.error(f"All attempts failed for {url}. Returning None to keep pipeline alive.")
        
        return None
        

    def get_exchange_rate(self, base: str = 'USD', target: str = 'SAR') -> Optional[float]:
        """
        Fetch current USD to SAR exchange rate.
        Used to normalize any USD compensation data to SAR.
        """
        # the link 
        endpoint = f"latest/{base}"
        # send request
        data = self._make_request(endpoint)

        if data is None: 
            return None
        # extract it
        rates_dict = data.get("rates")
        rate = rates_dict.get(target)
        if rate is not None: 
            return float(rate)
        else: 
            return None

    def get_labor_market_index(self) -> Optional[dict]:
        """
        Fetch Saudi labor market indicators.
        Returns dict with unemployment rate and sector growth.
        Simulated endpoint — use mock data if API unavailable.
        """
        # the link
        url = "https://api.worldbank.org/v2/country/SAU/indicator/SL.UEM.TOTL.ZS"
        params ={
            "format": 'json', 
            "mrv": 1
        }
        # send request 
        data =self._make_request(url, params)
        if data is None:
            return None
        # extract it
        value =data[1][0]
        summary ={
            "country": value["country"]["value"],
            "year": value["date"], 
            "saudi_unemployment_rate": value["value"], 
            "source": "World Bank "
        }
        return summary