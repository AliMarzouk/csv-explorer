import os
import csv

from .main import determine_types
import config.config as config
from lib.utils.constants import ColumnDataType

def test_determine_types():
    test_data = ([["year","state","month","number","date"], ["1998","Acre","Janeiro","0","1998-01-01"], ["2017","Acre","Fevereiro","1","2017-01-01"]], ',')
    expected = {"year": ColumnDataType.INTEGER, "state": ColumnDataType.STRING, "month": ColumnDataType.STRING, "number": ColumnDataType.INTEGER, "date": ColumnDataType.DATE}

    tmp_file = f'{config.OUTPUT_TMP_FOLDER}/tmp.csv';
    with open(tmp_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(test_data[0])
        
    result = determine_types(tmp_file, test_data[1])
    os.remove(tmp_file)

    assert result == expected
    
test_determine_types()
