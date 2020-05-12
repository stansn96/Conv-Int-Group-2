from googletrans import Translator
import re


def clean_aiml(text):
    """First makes all capitals, then replaces tags with <pattern>, then replaces closing <pattern> with </pattern>
    and it removes question marks. The output is a string. """
    text = text.upper()

    clean_o = re.compile('<.*?>')
    cleaned_o = re.sub(clean_o, '<pattern>', text)

    clean_c = re.compile('<pattern>$')
    cleaned_c = re.sub(clean_c, '</pattern>', cleaned_o)

    clean_qm = re.compile('\?')
    pattern = re.sub(clean_qm, '', cleaned_c)
    return pattern


def html_to_aiml_template(text):
    """This function transforms the html answers to templates. It removes div, p and br tags and the 'Stel je vraag'
    part. It also strips the string from whitespaces and adds the aiml template tags. It returns a string."""

    clean_divs = re.compile('<.*?div.*?>')
    cleaned_divs = re.sub(clean_divs, '', text)

    clean_p = re.compile('<p>')
    cleaned_p = re.sub(clean_p, '', cleaned_divs)

    clean_pc = re.compile('</p>')
    cleaned_pc = re.sub(clean_pc, '', cleaned_p)

    clean_br = re.compile('<br>')
    cleaned_br = re.sub(clean_br, '', cleaned_pc)

    clean_brc = re.compile('<br/>')
    cleaned_brc = re.sub(clean_brc, '', cleaned_br)

    clean_sjv = re.compile('<.*?form\=true.*?./a>')
    cleaned_sjv = re.sub(clean_sjv, '', cleaned_brc)

    stripped = cleaned_sjv.strip()

    template = '<template>{0}</template>'.format(stripped)
    return template


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

    # text = '<category><pattern>THIS CONVERSATION *</pattern><template>I was rather enjoying it <think>   <set name="it">     <set name="topic">       this conversation     </set>   </set> </think></template></category>'

    # new_text = text.replace('>', '> ')
    # new_text1 = new_text.replace('*', '* ')
    # wordlist = new_text1.split(' ')
    # print(wordlist)
    #
    # output = []
    # for word in wordlist:
    #     if re.match('<.*?>', word):
    #         output.append(word)
    #     elif re.match('name=".*?"', word):
    #         output.append(word)
    #     elif len(word) > 0:
    #         t = translator.translate(word, src='en', dest='nl')
    #         output.append(t.text)
    #
    #
    #
    # print(' '.join(output))

if __name__ == '__main__':
    main()