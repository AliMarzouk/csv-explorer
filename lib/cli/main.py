from lib.cli.menus import MainMenu, read_file


if __name__ == "__main__":
    try:
        # while False:
        # print("Welcome in this amazing CSV Explorer TODO: add welcome. CTRL+D to exit")
        # read_file()
        main_menu = MainMenu()
        main_menu.execute()
    except KeyboardInterrupt:
        print("Thank you for using the csv explorer CLI.")
    