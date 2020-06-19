# filename: translator.py
# this script takes a txt file and translates all the necessary parts in aiml from english to dutch and its ouput
# is a txt file
# author: Franka Korpel
# date: 12-05-2020

from googletrans import Translator
import re


def main():
    translator = Translator()

    en_file = open('examplefile.txt', 'r')
    dutch_file = open('dutch_result.aiml', 'w+')

    for line in en_file:
        new_line = line.replace('>', '> ')
        new_line2 = new_line.replace('*', '* ')
        new_line3 = new_line2.strip()
        wordlist = new_line3.split(' ')

        output = []
        sentence = []
        print(wordlist)
        for word in wordlist:
            if re.match('<.*?>', word):
                output.append(word)
            elif re.match('name=".*?"', word):
                output.append(word)
            elif len(word) > 0:
                sentence.append(word)

        if len(sentence) > 0:
            sentence_string = ' '.join(sentence)
            t = translator.translate(sentence_string, src='en', dest='nl')
            output.append(t.text)

        string_output = ' '.join(output)
        dutch_file.write(string_output)
        dutch_file.write('\n')

    dutch_file.close()
    en_file.close()


if __name__ == '__main__':
    main()
