import message as ms
import numpy as np


class Learner(object):
    def __init__(self, name, network):
        self.failed = False
        self.name = name
        self.network = network
        self.nl_matrix = self.create_matrix()
        self.en_matrix = self.create_matrix()

    def create_matrix(self):
        """"Create a matrix for each letter in the alfabet from the given line."""
        # Define all characters that can occur
        characters = 'abcdefghijklmnopqrstuvwxyz '
        # Make empty matrix
        matrix = np.zeros((len(characters) + 1, len(characters) + 1))
        return matrix

    def update_matrix(self, message):
        """ Update matrix based on the value given in the message """
        value = message.value[1]
        cell = self.get_correct_cell(value[3:])
        if value[0:2] == 'nl':
            self.nl_matrix[cell[0]][cell[1]] += 1
        elif value[0:2] == 'en':
            self.en_matrix[cell[0]][cell[1]] += 1

        return f"Predicted: {value}"

    def get_correct_cell(self, chars):
        """ Get the correct cell for an matrix based on the characters given """
        characters = 'abcdefghijklmnopqrstuvwxyz '
        for i in range(0, len(chars) - 1):
            letter = chars[i].lower()
            following_character = chars[i + 1].lower()

            if letter in characters:
                index_character = characters.index(letter)
            else:
                index_character = 27

            if following_character in characters:
                index_following_character = characters.index(following_character)
            else:
                index_following_character = 27

            return [index_character, index_following_character]

    def receive_message(self, message):
        lower_case = message.mtype.lower()
        if lower_case == 'succes':
            self.update_matrix(message)

