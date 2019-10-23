class Print:
    """Helper class that formats and prints all console output"""
    colors = {
        'DARKGREY': '\033[90m',
        'RED': '\033[91m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'BLUE': '\033[94m',
        'PURPLE': '\033[95m',
        'CYAN': '\033[96m',
        'WHITE': '\033[97m'
    }
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def conflicting_arguments(cls):
        message = "Conflicting Arguments"
        print(message)

    @classmethod
    def format(cls, message, color='', bold=False, underline=False):
        if color.upper() in cls.colors:
            message = cls.colors[color.upper()] + message
        if bold:
            message = cls.BOLD + message
        if underline:
            message = cls.UNDERLINE + message

        if color.upper() in cls.colors or bold or underline:
            message = message + cls.ENDC

        return message

    # methods used in cli.py
    @classmethod
    def version(cls):
        message = "LyxExporter 1.3.0"
        print(message)

    @classmethod
    def invalid_directory(cls):
        message = cls.format("Invalid Directory", color='RED')
        print(message)

    # methods used in scanner.py
    @classmethod
    def scanning_directory(cls, dirname):
        message = "Scanning \"" + dirname + "\" for Lyx files..."
        print(message)

    @classmethod
    def no_lyx_files_found(cls):
        message = cls.format("no Lyx files found", color='BLUE')
        print(message)

    @classmethod
    def not_exported(cls, filename):
        message = "[" + cls.format("Not Exported", color='RED') + "] "
        message += str(filename)
        print(message)

    @classmethod
    def is_outdated(cls, filename):
        message = "[  " + cls.format("Outdated", color='YELLOW') + "  ] "
        message += str(filename)
        print(message)

    @classmethod
    def up_to_date(cls, filename):
        message = "[ " + cls.format("Up-to-date", color='GREEN') + " ] "
        message += str(filename)
        print(message)

    @classmethod
    def num_files_scanned(cls, num):
        message = cls.format(str(num) + " files scanned", bold=True)
        print(message, end=". ")

    @classmethod
    def num_not_exported(cls, num):
        message = "["
        message += cls.format(str(num), bold=True) + " "
        message += cls.format("not exported", color='RED')
        message += "]"
        print(message, end=" ")

    @classmethod
    def num_outdated(cls, num):
        message = "["
        message += cls.format(str(num), bold=True) + " "
        message += cls.format("outdated", color='YELLOW')
        message += "]"
        print(message, end=" ")

    @classmethod
    def everything_up_to_date(cls):
        message = cls.format("All Lyx files exported and up-to-date", color='GREEN')
        print(message, end="")

    @staticmethod
    def linebreak():
        print("")

    # method used in lyxfile.py
    @classmethod
    def export_failed(cls, filename):
        message = cls.format("Export failed ", color='RED')
        message += cls.format("[!] ", bold=True)
        message += filename
        print(message)

    @classmethod
    def export_successful(cls, filename):
        message = cls.format("Export successful ", color='GREEN')
        message += filename
        print(message)
