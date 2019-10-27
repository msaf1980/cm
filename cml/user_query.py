class UserQuery:
    """Interface for interactively asking the user a question"""

    def ask(self, msg, default = ''):
        """Ask the user a question (get a string)

        Args:
            msg (string): Message to ask
            default (string): Default value if user does not enter anything

        Returns:
            string: Value the user provided

        """

        # Read from terminal
        return input('{} (\'{}\'): '.format(msg, default)) or default

    def confirm(self, msg, default = False):
        """Ask the user a yes/no-question (get a boolean=

        Args:
            msg (string): Message to ask
            default (Boolean): Default value if user does not enter anything

        Returns:
            Boolean: Value the user provided

        """

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
