import string
import os
import re
from tkinter import *
import numpy as np
import pandas as pd


class problem1:
    def __init__(self):
        # 문자열에서 영문, 숫자를 제외한 문자열 제거하기
        pass

    # remove punctuation :https://towardsdatascience.com/nlp-for-beginners-cleaning-preprocessing-text-data-ae8e306bef0f
    def remove_punctuation(self, text):
        no_punct = "".join([c for c in text if c not in string.punctuation])
        return no_punct

    # get input punctuation and remove them
    def input_remove_punctuation(self, text, punc):
        punc += '\n'
        no_punct = "".join([c for c in text if c not in punc])
        return no_punct

    # substitute punctuation to '\n'
    def replace_punctuation(self, text):
        """
        punc = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
        no_punct = re.sub("[^A-Za-z0-9-' '-'\'-\'-']+", ' ', text)
        punc = string.punctuation + "'" + '-' + ','
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        no_punct = " ".join(word.strip(punc) for word in text.split())
        print(no_punct)
        no_punct = re.sub(punc, ' ', text)
        no_punct = text.translate({ord(x): y for (x, y) in zip(punc, len(punc)*' ')})
        """
        no_punct = re.sub(r'[^\w\s]', ' ', text)
        no_punct = re.sub(r'\_', '', no_punct)
        no_punct = re.sub(r'\n', '', no_punct)

        return no_punct

    # input extension option
    def getResultOption(self):
        fileName = input("[file name with extension]\n"
                         "(extension: csv, txt, json)\n")
        fName = fileName.split('.')[0]
        extension = fileName.split('.')[1]
        print(fName, extension)

        return fName, extension

    # save result by extension option
    def getResult(self, data):
        fn, ext = self.getResultOption()
        if (ext == "csv"):
            # result to csv
            data.to_csv(fn + '.csv', index=False, header=['docNum', 'text'])
        elif (ext == "txt"):
            # result to txt
            fn = fn + '.txt'
            with open(fn, 'w') as f:
                f.write(data.to_string(header=False, index=False))
        elif (ext == "json"):
            # result to json
            fn = fn + '.json'
            data.to_json(fn, orient='table')
        else:
            print("Error: Write Another Extension (csv, txt, json)")
            self.getResult(data)

    def main(self):
        fname, ext = os.path.splitext('input.txt')
        # print(fname)
        # print(ext)
        fileName = fname + ext
        fileName = input("- Input file name with extension: ")

        # read txt file
        try:
            with open(fileName, 'r') as file:
                a = file.readlines()
        except FileNotFoundError as e:
            print(e)

        # get document number & remove doc number in text
        fNum = []
        index = 0
        for line in a:
            if line.split(' ')[0].isdigit() == True:
                fNum.append(int(line.split(' ')[0]))
                a[index] = line.replace(line.split(' ')[0], '')
                index += 1

        data = {'docNum': fNum, 'text': a}
        data = pd.DataFrame(data)
        # print(data)
        # print(string.punctuation)

        punc = int(input("1 - punctuation directly setting (Remove punctuation)\n"
                         "2 - existed punctuation usage (Replace to spacebard)\n"))

        if (punc == 1):
            punc = input("[Punctuation]\n"
                         "(just write each punctuation without spacebar and write Enter key when you are done)\n")
            data['text'] = data['text'].apply(lambda x: self.input_remove_punctuation(x, punc))
        elif (punc == 2):
            data['text'] = data['text'].apply(lambda x: self.replace_punctuation(x))

        # data['text'] = data['text'].apply(lambda x: self.remove_punctuation(x))
        # print(data.iloc[3])
        print(data)

        self.getResult(data)


P = problem1()
P.main()
