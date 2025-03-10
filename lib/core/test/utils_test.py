import pandas as pd
from lib.core.utils import UtilsError, check_columns_in_df, check_columns_types, determine_types
from lib.test.decorators import custom_test
from lib.utils.constants import ColumnDataType


@custom_test(
    (
        [{
            "year": ["1998", "2017"],
            "state": ["Acre", "Acre"],
            "month": ["Janeiro", "Fevereiro"]
        }, ["year", "state"]],
        False
    ), (
        [{
            "year": ["1998", "2017"],
            "state": ["Acre", "Acre"],
            "month": ["Janeiro", "Fevereiro"]
        }, ["year", "day"]],
        True
    )
)
def check_columns_in_df_raises_exception(test_data, raises_exception):
    # Given
    df = pd.DataFrame(test_data[0])
    try:
        # When
        check_columns_in_df(df, test_data[1])
        # Then
        assert not(raises_exception), "Should have not thrown exception"
    except Exception as e:
        assert raises_exception, "Should have thrown exception"
        if raises_exception:
            assert type(e) == UtilsError, "Should raise UtilsError exception"
            
@custom_test(
    (
        {
            "year": [1998, 2017],
            "date": ["2011-01-01", "1998-01-01"],
            "month": ["Janeiro", "Fevereiro"]
        },
        {
            "year": ColumnDataType.INTEGER,
            "date": ColumnDataType.DATE,
            "month": ColumnDataType.STRING
        }
    )
)           
def determine_types_return_column_types(test_data, expected_result):
    # Given
    df = pd.DataFrame(test_data)
    # When
    result = determine_types(df)
    # Then
    assert set(result.keys()) == set(test_data.keys()), "Should have same keys"
    for key_name in expected_result:
        assert result[key_name] == expected_result[key_name], f"Should have same column data in {key_name}"

@custom_test(
    (
        [{
            "year": [1998, 2017],
            "state": ["Acre", "Acre"],
            "month": ["Janeiro", "Fevereiro"]
        }, ["year", "state"], [ColumnDataType.INTEGER, ColumnDataType.STRING]],
        False
    ), (
        [{
            "year": [1998, 2017],
            "state": ["Acre", "Acre"],
            "month": ["Janeiro", "Fevereiro"]
        }, ["year", "month"], [ColumnDataType.FLOATING]],
        True
    ), (
        [{
            "year": [1998, 2017],
            "state": ["Acre", "Acre"],
            "month": ["Janeiro", "Fevereiro"]
        }, ["month"], [ColumnDataType.INTEGER]],
        True
    )
)
def check_columns_types_raises_exception(test_data, raises_exception):
    # Given
    df = pd.DataFrame(test_data[0])
    try:
        # When
        check_columns_types(df, test_data[1], test_data[2])
        # Then
        assert not(raises_exception), "Should have thrown exception"
    except Exception as e:
        assert raises_exception, "Should have not thrown exception"
        if raises_exception:
            assert type(e) == UtilsError, "Should raise UtilsError exception"