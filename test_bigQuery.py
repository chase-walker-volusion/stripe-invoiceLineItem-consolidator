import pytest
import config
from bigQuery import addParams, queryJob

def test_addParams():
    query = "testParameter"
    assert addParams(query, testParameter = "parameterValue") == "parameterValue"

def test_queryJob():
    assert isinstance(queryJob(config.QUERY), list)

def test_uploadJob():
    from google.cloud import bigquery
    backupDataSet = bigquery_client.dataset('dev_chasew')
    backupTable = backupDataSet.table('stripe_lineItem_backup')
    
    assert isinstance(uploadJob(backup.json, backupTable), list)