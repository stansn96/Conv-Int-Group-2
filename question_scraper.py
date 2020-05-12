from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import sys


def extract_questions_and_answers(file, q_tag, questions_class, answers_class):
    """Get all questions from html file and put it in a list"""

    soup = file
    question_list = []
    answers_list = []
    writefile = open("aiml_question", "a")

    questions_html = soup.select(questions_class)
    answers_html = soup.select(answers_class)
    
    for item in questions_html:
        writefile.write(str(item)+'\n')	
    writefile.close()

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

    stripped = cleaned_sjv.strip()

    template = '<template>{0}</template>'.format(stripped)
    return template


def to_aiml_category(pattern, template):
    """Input is the pattern and the template, the output is a full category. A possible extension here is to add topic/
    that based on the url."""

    category = '<category> \n {0} \n {1} \n</category>'.format(pattern, template)
    return category


def main():
    """Call with two arguments: question-class and answer-class. For example: .rug-h5 .rug-theme--content for url:
    "https://www.rug.nl/education/faq/?tcid=verint_3_7394_7529"
    """
    # todo: make a loop for all links
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
        print(i)
        url_loop = i
        response_loop = requests.get(url_loop)
        soup_loop = BeautifulSoup(response_loop.content, "html.parser")

        correct_li = soup_loop.find_all('li', class_='rug-list--accordion__item')
        for tag in correct_li:
            a_tags = tag.find_all('a', href=re.compile('\?tcid=verint.{11,12}\d*'))
            for link in a_tags:
                href_1 = re.findall('\?tcid=verint.{11,12}\d*', str(link))
                new_url_end = '{0}{1}'.format(url, href_1[0])
                print(new_url_end)
                response_end = requests.get(new_url_end)
                soup_end = BeautifulSoup(response_end.content, "html.parser")


                # hier moet ik een if-statement maken zodat de question en answer class klopt voor beide opties.
                option_choice = soup_end.select('.rug-h5')
                print(option_choice)
                if len(option_choice) > 0:
                    questions_and_answers = extract_questions_and_answers(soup_end, 'h2', '.rug-h5',
                                                                          '.rug-theme--content')
                else:
                    questions_and_answers = extract_questions_and_answers(soup_end, 'h1', '.rug-mb-0',
                                                                          'rug-theme--content')

            qlist = questions_and_answers[0]
            alist = questions_and_answers[1]
            print(len(qlist))
            print(len(alist))
			
            """
            category_example = to_aiml_category(qlist[0], alist[0])
            print(category_example)

            aiml_list = []
            n = 0
            for i in qlist:
                category = to_aiml_category(qlist[n], alist[n])
                aiml_list.append(category)
                n = n + 1

            for i in aiml_list:
                print(i, '\n')
            """
            # hier kan ik beter naar een .txt file schrijven denk ik
            # df = pd.DataFrame(aiml_list)
            # df.to_csv()

    # res = dict(zip(qlist, alist))
    # print("Resultant dict is:" + str(res))

if __name__ == "__main__":
    main()