import pytest
import config
from bigQuery import addParams, queryJob

def test_addParams():
    query = "testParameter"
    assert addParams(query, testParameter = "parameterValue") == "parameterValue"

def test_queryJob():
    assert isinstance(queryJob(config.QUERY), list)