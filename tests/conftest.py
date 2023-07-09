import pytest
from flask import Flask
from project import create_app

@pytest.fixture(scope="module")
def app():
    """Instance of main flask app"""
    return create_app()
