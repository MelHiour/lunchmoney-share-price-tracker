import os
import yaml
import requests

POLIGON_API = os.environ.get("POLIGON_API")
print(POLIGON_API)
LUNCHMONEY_API = os.environ.get("LUNCHMONEY_API")

POLYGON_ENDPOINT = "https://api.polygon.io/v2/aggs/ticker/"
LUNCHMONEY_ENDPOINT = "https://dev.lunchmoney.app/v1/assets/"


def parse_yaml(filename):
    with open(filename) as file:
        result = yaml.load(file, Loader=yaml.FullLoader)
    return result


def get_poligon_endpoint(stock_code, apikey):
    return POLYGON_ENDPOINT + stock_code + "/prev?adjusted=true&apiKey=" + apikey


def get_lunchmoney_endpoint(asset_id):
    return LUNCHMONEY_ENDPOINT + str(asset_id)


def get_stock_price(stock_code, apikey):
    endpoint = get_poligon_endpoint(stock_code, apikey)
    previos_close_price = requests.get(endpoint).json()["results"][0]["c"]
    return previos_close_price


def calculate_value(stock_price, amount):
    return stock_price * amount


def update_lunchmoney(asset_id, apikey, amount):
    data = {"balance": amount}
    headers = {"Authorization": apikey}
    endpoint = get_lunchmoney_endpoint(asset_id)
    return requests.put(endpoint, data=data, headers=headers).json()


def get_stock_price_and_update_lunchmoney(
    stock_code, asset_id, volume, poligon_apikey, lunchmoney_apikey
):
    stock_price = get_stock_price(stock_code, poligon_apikey)
    value = calculate_value(stock_price, volume)
    return update_lunchmoney(asset_id, lunchmoney_apikey, value)


if __name__ == "__main__":
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
