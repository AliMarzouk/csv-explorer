from lib.api.analysis import count_missing_values, count_values, find_outliers, get_header_infos, read_csv_file
from lib.api.manipulation import handle_missing_values
from lib.core.analysis import ProcessingError
from lib.cli.utils import input_column_names, print_success, print_warning, sanitized_input, bcolor, clear_console, open_file_selector, sanitized_input
from itertools import islice

from lib.core.manipulation import MissingValueReplaceOption
        

LIMIT_DISPLAY = 50
SECTION_DIVIDER = '-' * 50
            
class MenuInputError(BaseException):
    pass
            
class Command:
    def get_title(self):
        pass
    
    def execute(self):
        pass
    
    def print_title(self):
        print(f"{bcolor.CYAN}{self.get_title()}{bcolor.END}\n")

class Menu(Command):
    def __init__(self, title: str, choices: list[Command]):
        self.title = title
        self.choices = choices
    
    def get_title(self):
        return self.title
        
    def _print(self, error_message=""):
        clear_console()
        print(SECTION_DIVIDER)
        if error_message:
            print(SECTION_DIVIDER)
            print(bcolor.RED + error_message + ". Try again." + bcolor.END)
            print(SECTION_DIVIDER)
        self.print_title()
        print("0. Go back to previous menu.")
        for index, option in enumerate(self.choices):
            print(f"{index+1}. {option.get_title()}.")
        print(SECTION_DIVIDER)
        
    def execute(self):
        stay = True
        error_message = ""
        while stay:
            self._print(error_message)
            error_message = ""
            try:
                user_selection_str: str = sanitized_input("Enter choice")
                user_selection: int = int(user_selection_str)
                if user_selection not in range(len(self.choices) + 1):
                    raise MenuInputError()
            except (ValueError, MenuInputError) as e: 
                error_message = f"Invalid input [{user_selection_str}] (press CTRL+C to leave)"
                continue
            if user_selection == 0:
                stay = False
                continue
            try:
                self.choices[user_selection-1].execute()
            except ProcessingError as e:
                print(repr(e))
                error_message = "Something is not right. " + str(e)
                continue
            
class CountMissingValuesByCol(Command):
    def get_title(self):
        return "Count number of missing values by column"
    
    def execute(self):
        clear_console()
        self.print_title()
        column_names = input_column_names()
        additional_values = sanitized_input("You can provide a comma seperated list of values to consider as null (default=[])", '').split(',')
        missing_values = count_missing_values(column_names, additional_values)
        self.print_result(missing_values)
        
    def print_result(self, result: dict[str, int]):
        from prettytable import PrettyTable, HRuleStyle
        table = PrettyTable()
        table.hrules = HRuleStyle.ALL
        table.field_names = ["COLUMN NAME", "NUMBER OF MISSING VALUES"]
        for result_key in result.keys():
            table.add_row([result_key, result[result_key]])
        print(table)
        
class CountValuesByCol(Command):
    def get_title(self):
        return "Count number of values by column"
    def execute(self):
        clear_console()
        self.print_title()
        column_names = input_column_names()
        values_by_col_count = count_values(column_names)
        self.print_result(values_by_col_count)
        
    def print_result(self, value_count_by_col: dict[str, dict[str, int]]):
        from prettytable import PrettyTable, HRuleStyle
        table = PrettyTable()
        table.hrules = HRuleStyle.ALL
        for col_name in value_count_by_col.keys():
            count_text = '\n'.join([f"{key}: {value}" for key, value in islice(value_count_by_col[col_name].items(), 0, LIMIT_DISPLAY)])
            if len(value_count_by_col[col_name]) > LIMIT_DISPLAY:
                count_text += '\n ....(more)'
            table.add_column(col_name, [count_text])
        print(table)
        
class FindOutliers(Command):
    def get_title(self):
        return "Find Outliers by column"
    def execute(self):
        clear_console()
        self.print_title()
        column_names = input_column_names()
        outliers_by_col = find_outliers(column_names)
        self.print_result(outliers_by_col)
        
    def print_result(self, outliers_by_col: dict[str, list[str]]):
        from prettytable import PrettyTable, HRuleStyle
        table = PrettyTable()
        table.hrules = HRuleStyle.ALL
        table.field_names = ['', *outliers_by_col.keys()]
        table.add_row(['OUTLIERS COUNT', *[len(outliers_by_col[col_name]) for col_name in outliers_by_col.keys()]])
        table.add_row(['VALUES', *['\n'.join(map(str,[*outliers_by_col[col_name][:LIMIT_DISPLAY], '' if len(outliers_by_col[col_name]) <= LIMIT_DISPLAY else '... (more)'])) for col_name in outliers_by_col.keys()]])
        print(table)

class DisplayHeaders(Command):
    def get_title(self):
        return "Display headers"

    def execute(self):
        clear_console()
        self.print_title()
        headers_info = get_header_infos()
        self.print_result(headers_info)
        
    def print_result(self, headers_info: dict[str, list[str]]):
        from prettytable import PrettyTable, HRuleStyle
        table = PrettyTable()
        table.hrules = HRuleStyle.ALL
        table.field_names = ['', *headers_info.keys()]
        table.add_row(['COLUMN TYPE', *[data[0] for data in headers_info.values()]])
        table.add_row(['NUMBER MISSING VALUES', *[data[1] for data in headers_info.values()]])
        table.add_row(['ROWS COUNT', *[data[2] for data in headers_info.values()]])
        print(table)
        
class ReplaceMissingValuesCommand(Command):
    def __init__(self, replace_missing_values_by: MissingValueReplaceOption):
        self.replace_missing_values_by = replace_missing_values_by 
        super().__init__()
    
    def get_title(self):
        title = "Fill missing values with "
        if not self.replace_missing_values_by:
            raise MenuInputError("Replacement value cannot be null")
        elif self.replace_missing_values_by == MissingValueReplaceOption.MEAN:
            return title + "column mean value"
        elif self.replace_missing_values_by == MissingValueReplaceOption.MEDIAN:
            return title + "column median value"
        elif self.replace_missing_values_by == MissingValueReplaceOption.PANDAS_LINEAR_INTERPOLATE:
            return title + "data linear interpolation"
        elif self.replace_missing_values_by == MissingValueReplaceOption.CUSTOM_STRING_VALUE:
            return title + "custom input value" 
        
    def execute(self):
        clear_console()
        self.print_title()
        replace_value = None
        column_names = input_column_names()
        if self.replace_missing_values_by == MissingValueReplaceOption.CUSTOM_STRING_VALUE:
            replace_value = sanitized_input("Value to replaced by")
        handle_missing_values(column_names, replace_by=replace_value or self.replace_missing_values_by)
        print_success("Missing values successfully processed!")
        
class RemoveMissingValues(Command):
    def get_title(self):
        return "Remove lines with missing values"

    def execute(self):
        clear_console()
        self.print_title()
        print_warning("WARNING: This command drops the whole line of the csv file when a missing vlaue is found in the one of the given columns.")
        column_names = input_column_names()
        handle_missing_values(column_names)
        print_success("Missing values successfully processed!")
        
class ReplaceMissingValuesMenu(Menu):
    def __init__(self):
        title = "Handle missing values"
        super().__init__(title, [ReplaceMissingValuesCommand(MissingValueReplaceOption.MEAN), 
                                 ReplaceMissingValuesCommand(MissingValueReplaceOption.MEDIAN), 
                                 ReplaceMissingValuesCommand(MissingValueReplaceOption.PANDAS_LINEAR_INTERPOLATE),
                                 ReplaceMissingValuesCommand(MissingValueReplaceOption.CUSTOM_STRING_VALUE),
                                 RemoveMissingValues()])

class MainMenu(Menu):
    def __init__(self):
        title = "Main menu"
        super().__init__(title, [CountMissingValuesByCol(), CountValuesByCol(), FindOutliers(), DisplayHeaders(), ReplaceMissingValuesMenu()])

def read_file():
    sanitized_input("First you need to select a CSV file, press enter to continue")
    file_path = open_file_selector()
    delimiter = sanitized_input("Please specify the delimiter of the file (default=,)", ',') 
    read_csv_file(file_path, delimiter)