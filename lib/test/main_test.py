import os
import csv

from lib.test.decorators import custom_test
from lib.analysis.main import determine_types
from lib.analysis.main import get_missing_values_indexes
from config import config
from lib.utils.constants import ColumnDataType


@custom_test(
    (
        [["year","state","month","number","date"], ["1998","Acre","Janeiro","0","1998-01-01"], ["2017","Acre","Fevereiro","1","2017-01-01"]],
        {"year": ColumnDataType.INTEGER, "state": ColumnDataType.STRING, "month": ColumnDataType.STRING, "number": ColumnDataType.INTEGER, "date": ColumnDataType.DATE}
     )
)
def test_determine_types(test_data, expected):
    tmp_file = f'{config.OUTPUT_TMP_FOLDER}/tmp.csv';
    with open(tmp_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(test_data)
        
    result = determine_types(tmp_file, ',')
    os.remove(tmp_file)

    assert result == expected
    
@custom_test(
    (
        ([["year","state","month","number","date"], ["1998","Acre","Janeiro","0","1998-01-01"], ["2017","Acre","February","1","2017-01-01"], ["2017","Acre",None,"1","2017-01-01"]], "month", ["Janeiro"]),
        [0,2]
    )
)
def test_get_missing_values_indexes(test_data, expected):
    tmp_file = f'{config.OUTPUT_TMP_FOLDER}/tmp.csv';
    with open(tmp_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(test_data[0])
        
    result = get_missing_values_indexes(tmp_file, ',', test_data[1], test_data[2])
    os.remove(tmp_file)

    assert result == expected
