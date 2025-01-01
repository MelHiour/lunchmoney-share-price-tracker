# AI generated tests! Not that bad...

import pytest # type: ignore
from unittest.mock import patch, mock_open
import yaml
import requests
from stock_updater import (
    parse_yaml,
    get_poligon_endpoint,
    get_lunchmoney_endpoint,
    get_stock_price,
    get_usd_to_eur_price,
    calculate_value,
    update_lunchmoney,
    get_stock_price_and_update_lunchmoney,
)

# Test parse_yaml function
def test_parse_yaml():
    yaml_content = """
    stocks:
      - stock_code: AAPL
        asset_id: 1
        amount: 10
    """
    with patch("builtins.open", mock_open(read_data=yaml_content)):
        result = parse_yaml("dummy.yaml")
    
    assert result == {"stocks": [{"stock_code": "AAPL", "asset_id": 1, "amount": 10}]}

# Test get_poligon_endpoint function
def test_get_poligon_endpoint():
    result = get_poligon_endpoint("AAPL", "api_key")
    assert result == "https://api.polygon.io/v2/aggs/ticker/AAPL/prev?adjusted=true&apiKey=api_key"

# Test get_lunchmoney_endpoint function
def test_get_lunchmoney_endpoint():
    result = get_lunchmoney_endpoint(123)
    assert result == "https://dev.lunchmoney.app/v1/assets/123"

# Test get_stock_price function
@patch("requests.get")
def test_get_stock_price(mock_get):
    mock_get.return_value.json.return_value = {"results": [{"c": 150.0}]}
    result = get_stock_price("AAPL", "api_key")
    assert result == 150.0
    mock_get.assert_called_once_with("https://api.polygon.io/v2/aggs/ticker/AAPL/prev?adjusted=true&apiKey=api_key")

# Test get_usd_to_eur_price function
@patch("requests.get")
def test_get_usd_to_eur_price(mock_get):
    mock_get.return_value.json.return_value = {"results": [{"c": 0.85}]}
    result = get_usd_to_eur_price("api_key")
    assert result == 0.85
    mock_get.assert_called_once_with("https://api.polygon.io/v2/aggs/ticker/C:USDEUR/prev?adjusted=true&apiKey=api_key")

# Test calculate_value function
def test_calculate_value():
    result = calculate_value(100, 10, 0.85)
    assert result == 850

# Test update_lunchmoney function
@patch("requests.put")
def test_update_lunchmoney(mock_put):
    mock_put.return_value.json.return_value = {"success": True}
    result = update_lunchmoney(123, "api_key", 1000)
    assert result == {"success": True}
    mock_put.assert_called_once_with(
        "https://dev.lunchmoney.app/v1/assets/123",
        data={"balance": 1000},
        headers={"Authorization": "Bearer api_key"}
    )

# Test get_stock_price_and_update_lunchmoney function
@patch("stock_updater.get_stock_price")
@patch("stock_updater.get_usd_to_eur_price")
@patch("stock_updater.update_lunchmoney")
def test_get_stock_price_and_update_lunchmoney(mock_update, mock_usd_eur, mock_stock_price):
    mock_stock_price.return_value = 100
    mock_usd_eur.return_value = 0.85
    mock_update.return_value = {"success": True}

    result = get_stock_price_and_update_lunchmoney("AAPL", 123, 10, "polygon_key", "lunchmoney_key")

    assert result == {"success": True}
    mock_stock_price.assert_called_once_with("AAPL", "polygon_key")
    mock_usd_eur.assert_called_once_with("polygon_key")
    mock_update.assert_called_once_with(123, "lunchmoney_key", 850)
