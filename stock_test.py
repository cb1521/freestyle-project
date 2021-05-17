import os
import pytest

from app.stock_service import format_date, stock_growth, stock_time

CI_ENV = os.getenv("CI") == "true"

def test_date_formatting():
    assert format_date("2021-05-17T16:00:00-04:00") == "2021-05-17"

@pytest.mark.skipif(CI_ENV==True, reason="to avoid issuing HTTP requests on the CI server")
def test_stock_growth():
    results = stock_growth(symbol= "MSFT", shares= "4")
    assert len(results['stock_data']) == 1
    stock_data = results['stock_data'][0]
    assert sorted(list(stock_data.keys())) == ["change_in_value", "current_investor_value", "latest_close", "previous_investor_value"]

@pytest.mark.skipif(CI_ENV==True, reason="to avoid issuing HTTP requests on the CI server")
def test_stock_time():
    results = stock_time(symbol= "MSFT", shares= "4")
    assert len(results['investment_trends']) == 20
    investment_trends = results['investment_trends'][0]
    assert sorted(list(investment_trends.keys())) == ["daily_investment_close", "date"]