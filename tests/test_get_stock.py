import pytest
import helper as app

def test_get_stock():
    result = app.get_price("Voo")
    assert result == 480.5

def test_check_db():
    result = app.check_db()
    assert result == True

def test_get_all_stocks():
    assert app.get_all_stocks(1) == []

def test_get_login_username():
    assert app.get_login_username("huypham") == "HUYPHAM"

def test_get_login_username_false():
    assert app.get_login_username("huypham1") == None

