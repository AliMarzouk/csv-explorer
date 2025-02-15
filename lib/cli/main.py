from lib.cli.menus import MainMenu, read_file
from lib.cli.utils import bcolor


if __name__ == "__main__":
    try:
        while True:
            print("Welcome in this amazing CSV Explorer add welcome. CTRL+D to exit")
            read_file()
            main_menu = MainMenu()
            main_menu.execute()
    except KeyboardInterrupt:
        print(bcolor.GREEN + "\nThank you for using the csv explorer CLI." + bcolor.END)
    