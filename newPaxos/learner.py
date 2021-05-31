import message as ms
import numpy as np

class Learner(object):
    def __init__(self, name, network):
        self.failed = False
        self.name = name
        self.network = network

    def create_matrix(self, line):
        """"Create a matrix for each letter in the alfabet from the given line."""
        # Define all characters that can occur
        characters = 'abcdefghijklmnopqrstuvwxyz '
        # Make empty matrix
        matrix = np.zeros((len(characters) + 1, len(characters) + 1))

        # Loop thru all characters in the given line and fill the matrix
        for i in range(0, len(line) - 1):
            letter = line[i].lower()
            following_character = line[i + 1].lower()

            if letter in characters:
                index_character = characters.index(letter)
            else:
                index_character = 27

            if following_character in characters:
                index_following_character = characters.index(following_character)
            else:
                index_following_character = 27

            matrix[index_character][index_following_character] += 1
        self.convert_to_percentage(matrix)

    def convert_to_percentage(self, matrix):
        """"Convert all values in matrix to percentage based on part of the total."""
        total = np.sum(matrix)
        for row in range(len(matrix)):
            for index in range(len(matrix)):
                matrix[row][index] = matrix[row][index] / total
        return matrix

    def receive_message(self, msg):
        if msg.mtype == 'succes':
            self.create_matrix('PRECIES GEEN IDEE WAAR VANDAAG')
