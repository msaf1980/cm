class UserQuery:
    """Interface for interactively asking the user a question"""

    def ask(self, msg, default = ''):
        """Ask the user a question (get a string)"""

        # Read from terminal
        return input('{} (\'{}\'): '.format(msg, default)) or default

    def confirm(self, msg, default = False):
        """Ask the user a yes/no-question (get a boolean)"""

        # Determine default
        if default:
            defaults = 'Y/n'
        else:
            defaults = 'y/N'

        # Read from terminal
        value = input('{} ({}): '.format(msg, defaults))
        print(value)
        if value in [ 'y', 'Y', 'yes', 'YES', 'Yes' ]:
            return True
        elif value in [ 'n', 'N', 'no', 'NO', 'No' ]:
            return False
        else:
            return default
