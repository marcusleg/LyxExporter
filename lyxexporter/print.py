class Print:
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
    def format(self, message, color='', bold=False, underline=False):
        if color.upper() in self.colors:
            message = self.colors[color.upper()] + message
        if bold:
            message = self.BOLD + message
        if underline:
            message = self.UNDERLINE + message

        if color.upper() in self.colors or bold or underline:
            message = message + self.ENDC

        return message

    # methods used in cli.py
    @classmethod
    def invalid_directory(self):
        message = self.format("Invalid Directory", color='RED')
        print(message)

    # methods used in scanner.py
    @classmethod
    def scanning_directory(self, dir):
        message = "Scanning \"" + dir + "\" for Lyx files..."
        print(message)

    @classmethod
    def no_lyx_files_found(self):
        message = self.format("no Lyx files found", color='BLUE')
        print(message)

    @classmethod
    def not_exported(self, filename):
        message = "[" + self.format("Not Exported", color='RED') + "] "
        message += str(filename)
        print(message)

    @classmethod
    def is_outdated(self, filename):
        message = "[  " + self.format("Outdated", color='YELLOW') + "  ] "
        message += str(filename)
        print(message)

    @classmethod
    def up_to_date(self, filename):
        message = "[ " + self.format("Up-to-date", color='GREEN') + " ] "
        message += str(filename)
        print(message)

    @classmethod
    def num_files_scanned(self, num):
        message = self.format(str(num) + " files scanned", bold=True)
        print(message, end=". ")

    @classmethod
    def num_not_exported(self, num):
        message = "["
        message += self.format(str(num), bold=True) + " "
        message += self.format("not exported", color='RED')
        message += "]"
        print(message, end=" ")

    @classmethod
    def num_outdated(self, num):
        message = "["
        message += self.format(str(num), bold=True) + " "
        message += self.format("outdated", color='YELLOW')
        message += "]"
        print(message, end=" ")

    @classmethod
    def everything_up_to_date(self):
        message = self.format("All Lyx files exported and up-to-date", color='GREEN')
        print(message, end="")

    @staticmethod
    def linebreak():
        print("")

    # method used in lyxfile.py
    @classmethod
    def export_failed(self, filename):
        message = self.format("Export failed " , color='RED')
        message += self.format("[!] ", bold=True)
        message += filename
        print(message)

    @classmethod
    def export_successful(self, filename):
        message = self.format("Export successful ", color='GREEN')
        message += filename
        print(message)