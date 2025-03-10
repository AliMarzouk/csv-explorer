import csv
import os
from config import config
from lib.core.analysis import determine_types
from lib.test.decorators import custom_test
from lib.utils.constants import ColumnDataType


@custom_test(
    (
        [["year","state","month","number","date"], ["1998","Acre","Janeiro","0","1998-01-01"], ["2017","Acre","Fevereiro","1","2017-01-01"]],
        {"year": ColumnDataType.INTEGER, "state": ColumnDataType.STRING, "month": ColumnDataType.STRING, "number": ColumnDataType.INTEGER, "date": ColumnDataType.DATE}
     )
)
def test_determine_types(test_data, expected):
    tmp_file = f'{config.OUTPUT_TMP_FOLDER}/tmp.csv'
    with open(tmp_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(test_data)
        
    result = determine_types(tmp_file, ',')
    os.remove(tmp_file)

    assert result == expected, "Should return expected result"