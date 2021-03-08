from datetime import datetime
import markovify
import os.path
import random
import requests

"""
Helper file for the bot run.py file. Used to keep the run file clean while adding new features and methods.
"""

EXECUTE_COUNT_FILE = 'ExecuteCount.txt'
QUOTES_FILE = 'quotes.txt'
STRETCH_BREAK_FOLDER = 'gifs/stretch_break/'
LOG_FILE = f"{os.getcwd()}/logs/{datetime.now().strftime('%Y')}/{datetime.now().strftime('%B')}/{datetime.now().date()}.log"


class Helper:
    def __init__(self, author):
        self.author = author

    def add_quote(self, quote):
        """
        Appends a new quote from Bohn on a new line
        :param quote: String of the new quote
        :return: Integer value of the line the quote was added to
        """
        self.log(f'User {self.author} added a new quote: {quote}')
        quotes = self.get_quotes()
        open(QUOTES_FILE, 'w', encoding="utf8")\
            .write('\n'.join(map(str, quotes)) + f"\n{quote}\n")
        return len(quotes) + 1

    def check_for_count_file(self):
        if not os.path.isfile(EXECUTE_COUNT_FILE):
            open(EXECUTE_COUNT_FILE, "w+")

    def get_count(self):
        self.check_for_count_file()
        count = open(EXECUTE_COUNT_FILE, "r").read()
        return int(count) if count else 0

    def get_quotes(self):
        """
        Gets all the quotes from Bohn stored currently in a text file
        :return: list of quotes
        """
        with open(QUOTES_FILE, 'r', encoding="utf8") as f:
            return [x.strip() for x in f.readlines()]

    def increment_count(self):
        self.check_for_count_file()
        current_count = self.get_count()
        open(EXECUTE_COUNT_FILE, "w").write(str(current_count + 1))

    def log(self, text):
        if not os.path.isfile(LOG_FILE):
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
            open(LOG_FILE, "w+")
        logs = open(LOG_FILE, "r").read()
        open(LOG_FILE, "w").write(logs + f"{datetime.now()}: {text}\n")

    def markov(self):
        """
        Creates a Markov chain from the quotes.txt file to create generated Bohn messages
        :return: String
        """
        with open(QUOTES_FILE, encoding="utf8") as f:
            text = f.read()

        text_model = markovify.NewlineText(text)

        return text_model.make_sentence(tries=100, state_size=3)

    def quine(self):
        """
        Sends a message of the python code of this program
        :return: List of messages
        """
        # Get the repository
        git_remote = os.popen("git remote get-url origin").read().strip().split(':')[-1].replace('.git', '')
        git_url = f"https://api.github.com/repos/{git_remote}/contents/"
        files_json = requests.get(git_url).json()
        # Create a list of messages for the python code
        result = ['https://en.wikipedia.org/wiki/Quine_(computing)']
        for file_json in files_json:
            file_name = file_json['name']
            if '.py' in file_name:
                file = requests.get(file_json['download_url']).text
                result.extend(self.string_to_code(file_name, file, 'Python'))
        return result

    def random_quote(self):
        """
        Gets a random quote from Bohn
        :return: String random quote
        """
        quotes = self.get_quotes()
        chosen = random.randint(0, len(quotes) - 1)
        return quotes[chosen]

    def remove_quote(self, line):
        """
        Removes a quote from a line in the text file
        :param line: Integer line in the text file
        """
        quotes = self.get_quotes()
        self.log(f'User {self.author} removed quote on line {line}. Text: {quotes[line - 1]}')
        del quotes[line - 1]
        open(QUOTES_FILE, 'w', encoding="utf8").write('\n'.join(map(str, quotes)))

    def show_all_quotes(self):
        quotes = self.get_quotes()
        formatted_quotes = ''
        for n, line in enumerate(quotes, start=1):
            formatted_quotes = formatted_quotes + f"{n}. {line}\n"
        return formatted_quotes

    def string_to_code(self, file_name, contents, file_type):
        """
        Converts a String into Discord readable code
        :param file_name: String name of the file
        :param contents: String of the contents of the file
        :param file_type: String name of the file type
        :returns: List split up to fit within the 2000 letter limit if necessary
        """
        result = [f"`{file_name}`:"]
        max_length = 1999 - (8 + len(file_type))
        while len(contents) > 0:
            result.append(f"```{file_type}\n{contents[0:max_length]}\n```")
            contents = contents[max_length:]
        return result

    def random_stretch_break(self):
        return random.choice([os.path.join(STRETCH_BREAK_FOLDER, f) for f in os.listdir(STRETCH_BREAK_FOLDER)])
