from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import sys
import os
from sklearn.externals import joblib

def extract_questions_and_answers(file, question_class):
    """Get all questions from html file and put it in a list"""
    soup = file
    question_list = []
    answers_list = []

    questions_html = soup.select(question_class)
    answers_html = soup.select('.rug-theme--content')

    for i in questions_html:
        pattern = html_to_aiml_pattern(str(i))
        question_list.append(pattern)

    for i in answers_html:
        template = html_to_aiml_template(str(i))
        answers_list.append(template)

    return question_list, answers_list


def html_to_aiml_pattern(text):
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
    
    clean_ul = re.compile('<ul class="rug-list--bullets rug-mv-xs">')
    cleaned_ul = re.sub(clean_ul, '<ul>', cleaned_sjv)
    
    clean_li = re.compile('<li class="rug-list--bullets__item">')
    cleaned_li = re.sub(clean_li, '<li>', cleaned_ul)
    
    clean_str = re.compile('<strong>')
    cleaned_str = re.sub(clean_str, '', cleaned_li)

    clean_strc = re.compile('</strong>')
    cleaned_strc = re.sub(clean_strc, '', cleaned_str)
    
    clean_span = re.compile('<span>')
    cleaned_span = re.sub(clean_span, '', cleaned_strc)
    
    clean_spanc = re.compile('</span>')
    cleaned_spanc = re.sub(clean_spanc, '', cleaned_span)
    
    clean_em = re.compile('<em>')
    cleaned_em = re.sub(clean_em, '', cleaned_spanc)
    
    clean_emc = re.compile('</span>')
    cleaned_emc = re.sub(clean_emc, '', cleaned_em)
    
    stripped = cleaned_emc.strip()

    template = '<template>\n{0}\n\t\t</template>'.format(stripped)
    return template


def to_aiml_category(pattern, template):
    """Input is the pattern and the template, the output is a full category. A possible extension here is to add topic/
    that based on the url."""

    category = '\t<category>\n\t\t{0}\n\t\t{1}\n\t</category>\n'.format(pattern, template)
    return category


def main():
    """Call with only filename and it retrieves all questions and their answers from all the links form the RUG  faq
    and it outputs it as aiml categories in aiml files. For every topic a new aiml file is created and put into the
    folders aiml_files"""

    tagger = joblib.load('POS_Tag_NL.pkl')
    pos_tag = tagger.tag

    # here the url content is fetched and the soup is the result
    url = "https://www.rug.nl/education/faq/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # first loop for links
    first_links = soup.find_all('a', class_='rug-nav--secondary__sub__link')
    topic_links = first_links[1:10]
    first_loop_links = []

    for i in topic_links:
        # extract href and text to pass on the next filter
        href = re.findall('\?tcid=verint.{11,12}\d*', str(i))
        new_link = '{0}{1}'.format(url, href[0])
        first_loop_links.append(new_link)

    #second loop for links
    for i in first_loop_links:
        #print("first loop link")
        #print(i)
        url_loop = i
        response_loop = requests.get(url_loop)
        soup_loop = BeautifulSoup(response_loop.content, "html.parser")

        correct_li = soup_loop.find_all('li', class_='rug-list--accordion__item')

        for tag in correct_li:
            a_tags = tag.find_all('a', href=re.compile('\?tcid=verint.{11,12}\d*'))
            for link in a_tags:
                #print('anddd again')
                href_1 = re.findall('\?tcid=verint.{11,12}\d*', str(link))
                new_url_end = '{0}{1}'.format(url, href_1[0])
                #print('new url', new_url_end)
                response_end = requests.get(new_url_end)
                soup_end = BeautifulSoup(response_end.content, "html.parser")

                option_choice = soup_end.select('.rug-h5')
                #print(option_choice)
                if len(option_choice) > 0:
                    questionclass = 'h2.rug-h5'
                    #print('option1')
                    # extract topic which in this case is in <h1> .rug-mb-0
                    topic = soup_end.select('h1.rug-mb-0')
                    topic_clean = (topic[0].string).replace('/', '-')
                    topic_cleaner = topic_clean.replace(' ', '_')
                    filename = 'symred_files/{0}.aiml'.format(topic_cleaner)
                else:
                    questionclass = 'h1.rug-mb-0'
                    #print('option2')

                    breadcrumbs = soup_end.select('a.rug-breadcrumbs__link')
                    topic_last = breadcrumbs[-1:]

                    topic = topic_last[0].string
                    topic_clean = topic.replace('/', '-')
                    topic_cleaner = topic_clean.replace(' ', '_')
                    filename = 'symred_files/|{0}.aiml'.format(topic_cleaner)
                    print(filename)


                #print('i am out the if-else')

                questions_and_answers = extract_questions_and_answers(soup_end, questionclass)
                qlist = questions_and_answers[0]
                alist = questions_and_answers[1]
                
                symredqlist = []
                for sentence in qlist:
                    realstring = sentence[9:-10]
                    splitsent = realstring.lower().split()
                    tagsent = pos_tag(splitsent)
                    for index, item in enumerate(tagsent):
                        if item[1] != 'noun' and item[1]!= 'verb' and item[1]!= 'adv':
                            tagsent[index] = '*'
                        if item[0].lower() == 'ik':
                            tagsent[index] = '*'

                    outsent = [v for i, v in enumerate(tagsent) if i == 0 or v != tagsent[i-1]]
                    normalsent = []
                    for item in outsent:
                        normalsent.append(item[0])
                    normalstring = ' '.join(normalsent)
                    completestring = "<pattern>"+normalstring.upper()+"</pattern>"
                    symredqlist.append(completestring)

                aiml_list = []
                n = 0
                for i in symredqlist:
                    category = to_aiml_category(symredqlist[n], alist[n])
                    aiml_list.append(category)
                    n = n + 1

                if os.path.exists(filename):
                    print(filename)
                    if '|' in filename:
                        print("appending to file {0}".format(filename))
                        with open(filename, 'r') as file:
                            print(file)
                            lst = []
                            for line in file:
                                if "</aiml>" in line:
                                    print("here it is")
                                    print(line)
                                    line = line.strip().replace("</aiml>", "\n")
                                lst.append(line)
                            file.close()
                            f = open(filename, 'w')
                            for line in lst:
                                f.write(line)

                            for i in aiml_list:
                                f.write(i)
                                f.write('\n')

                            f.write("</aiml>")
                            f.close()
                    else:
                        print('File already exists and should not do anything.')


                else:
                    with open(filename, 'w+') as f:
                        print(f)
                        f.write('<?xml version="1.0" encoding="UTF-8"?> \n<aiml version="2.0"> \n')

                        for i in aiml_list:
                            f.write(i)
                            f.write('\n')

                        f.write("</aiml>")
                        f.close()


                print('On to the next link!')

if __name__ == "__main__":
    main()
