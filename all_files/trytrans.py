from googletrans import Translator


def main():

    translator = Translator()

    totrans = [
        [" with you ", " with me "],
        [" with me ", " with you "],
        [" to you ", " to me "],
        [" to me ", " to you "],
        [" of you ", " of me "],
        [" of me ", " of you "],
        [" for you ", " for me "],
        [" for me ", " for you "],
        [" give you ", " give me "],
        [" give me ", " give you "],
        [" giving you ", " giving me "],
        [" giving me ", " giving you "],
        [" gave you ", " gave me "],
        [" gave me ", " gave you "],
        [" make you ", " make me "],
        [" make me ", " make you "],
        [" made you ", " made me "],
        [" made me ", " made you "],
        [" take you ", " take me "],
        [" take me ", " take you "],
        [" save you ", " save me "],
        [" save me ", " save you "],
        [" tell you ", " tell me "],
        [" tell me ", " tell you "],
        [" telling you ", " telling me "],
        [" telling me ", " telling you "],
        [" told you ", " told me "],
        [" told me ", " told you "],
        [" are you ", " am I "],
        [" am I ", " are you "],
        [" you are ", " I am "],
        [" I am ", " you are "],
        [" you ", " me "],
        [" me ", " you "],
        [" your ", " my "],
        [" my ", " your "],
        [" yours ", " mine "],
        [" mine ", " yours "],
        [" yourself ", " myself "],
        [" myself ", " yourself "],
        [" I was ", " you were "],
        [" you were ", " I was "],
        [" I am ", " you are "],
        [" you are ", " I am "],
        [" I ", " you "],
        [" me ", " you "],
        [" my ", " your "],
        [" your ", " my "]
    ]

    new_list = []
    for item in totrans:
        string_1 = item[0]
        string_2 = item[1]


        t1 = translator.translate(string_1, src='en', dest='nl')
        t2 = translator.translate(string_2, src='en', dest='nl')

        new_item = [t1.text, t2.text]
        new_list.append(new_item)

    print(new_list)


if __name__ == "__main__":
    main()

