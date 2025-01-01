import sys
import yaml
import requests

POLYGON_ENDPOINT: str = "https://api.polygon.io/v2/aggs/ticker/"
LUNCHMONEY_ENDPOINT: str = "https://dev.lunchmoney.app/v1/assets/"


def parse_yaml(filename: str) -> dict:
    with open(filename) as file:
        result = yaml.load(file, Loader=yaml.FullLoader)
    return result


def get_poligon_endpoint(stock_code: str, apikey: str) -> str:
    return POLYGON_ENDPOINT + stock_code + "/prev?adjusted=true&apiKey=" + apikey


def get_lunchmoney_endpoint(asset_id: int) -> str:
    return LUNCHMONEY_ENDPOINT + str(asset_id)


def get_stock_price(stock_code: str, apikey: str) -> int:
    endpoint = get_poligon_endpoint(stock_code, apikey)
    previos_close_price = requests.get(endpoint).json()["results"][0]["c"]
    return previos_close_price


def get_usd_to_eur_price(apikey: str) -> int:
    currency_pair = "C:USDEUR"
    endpoint = get_poligon_endpoint(currency_pair, apikey)
    previos_close_price = requests.get(endpoint).json()["results"][0]["c"]
    return previos_close_price


def calculate_value(stock_price: int, amount: int, ust_to_eur: int) -> int:
    return stock_price * amount * ust_to_eur


def update_lunchmoney(asset_id: int, apikey: str, amount: int) -> dict:
    data = {"balance": amount}
    headers = {"Authorization": "Bearer " + apikey}
    endpoint = get_lunchmoney_endpoint(asset_id)
    return requests.put(endpoint, data=data, headers=headers).json()


def get_stock_price_and_update_lunchmoney(
    stock_code: str,
    asset_id: int,
    volume: int,
    poligon_apikey: str,
    lunchmoney_apikey: str,
) -> dict:
    stock_price = get_stock_price(stock_code, poligon_apikey)
    usd_to_eur = get_usd_to_eur_price(poligon_apikey)
    value = calculate_value(stock_price, volume, usd_to_eur)
    return update_lunchmoney(asset_id, lunchmoney_apikey, value)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        POLIGON_API = sys.argv[1]
        LUNCHMONEY_API = sys.argv[2]
        stocks_to_process = parse_yaml("config.yaml")
        for stock in stocks_to_process["stocks"]:
            result = get_stock_price_and_update_lunchmoney(
                stock["stock_code"],
                stock["asset_id"],
                stock["amount"],
                POLIGON_API,
                LUNCHMONEY_API,
            )
            print(result)
    else:
        raise BaseException("Too less attributes...")
