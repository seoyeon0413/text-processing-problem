import string
from tkinter import *
import pandas as pd


class Problem1:

    def __init__(self):
        pass

    def remove_specialCharacter(self, text):
        '''
        remove punctuation :https://towardsdatascience.com/nlp-for-beginners-cleaning-preprocessing-text-data-ae8e306bef0f
        :param text: text data with dataframe type
        :return: text removed special characters
        '''

        no_sc = "".join([c for c in text if c not in string.punctuation])
        return no_sc

    def input_remove_specialCharacter(self, text, sc):
        '''
        get input punctuation and remove them
        :param text: text data with dataframe type
        :param sc: special characters getting from input
        :return: text removed special characters
        '''

        sc += '\n'
        ### list comprehension외에 다른 방식으로 처리할 수 있는지 고민할 것
        no_sc = "".join([c for c in text if c not in sc])
        return no_sc

    def replace_specialCharacter(self, text):
        '''
        replace punctuation to spacebar character
        :param text: text data with dataframe type
        :return: text replaced special characters to spacebar character
        '''

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
        no_sc = re.sub(r'[^\w\s]', ' ', text)
        no_sc = re.sub(r'\_', '', no_sc)
        no_sc = re.sub(r'\n', '', no_sc)

        return no_sc

    def getResultOption(self):
        '''
        input file name and extension option
        :return: file name and extension option
        '''

        fileName = input("[file name with extension]\n"
                         "(extension: csv, txt, json)\n")
        fName = fileName.split('.')[0]
        extension = fileName.split('.')[1]
        print(fName, extension)

        return fName, extension

    def writeData(self, data):
        '''
        save results by extension option
        :param data: results that have to save
        :return: nothing
        '''

        fn, ext = self.getResultOption()
        if (ext == "csv"):  # result to csv
            data.to_csv(fn + '.csv', index=False, header=['docNum', 'text'])
        elif (ext == "txt"):    # result to txt
            fn = fn + '.txt'
            with open(fn, 'w') as f:
                f.write(data.to_string(header=False, index=False))
        elif (ext == "json"):   # result to json
            fn = fn + '.json'
            data.to_json(fn, orient='table')
        else:
            print("Error: Write Another Extension (csv, txt, json)")
            self.writeData(data)

    def getInputName(self):
        '''
        get input file name
        :return: file name
        '''

        # fname, ext = os.path.splitext('input.txt')
        # print(fname)
        # print(ext)
        # fileName = fname + ext
        fileName = input("- Input file name with extension: ")

        return fileName

    def readFile(self, fn):
        '''
        read text file from directory
        :param fn: file name
        :return: data from file
        '''

        try:
            with open(fn, 'r') as file:
                readAllFile = file.readlines()
        except FileNotFoundError as e:
            print('해당하는 파일이 없습니다: {}.format'.format(e))

        return readAllFile

    def splitData(self, d):
        '''
        get document number & remove doc number in text
        :param d: data from file
        :return: data converted to dataframe type
        '''

        fNum = []
        index = 0
        for line in d:
            if line.split(' ')[0].isdigit() == True:
                fNum.append(int(line.split(' ')[0]))
                d[index] = line.replace(line.split(' ')[0], '')
                index += 1

        data = {'docNum': fNum, 'text': d}
        data = pd.DataFrame(data)

        return data

    def run(self):
        '''
        main function of this program: 문자열에서 영문, 숫자를 제외한 문자열 제거하기
        :return: nothing
        '''

        fileName = self.getInputName()
        rf = self.readFile(fileName)
        data = self.splitData(rf)

        ### 솔루션에서는 키보드 입력보다는 property 파일을 만들어서 실행 시키는 것이 좋음
        ### 키보드 입력받으면 중간중간 사용자가 입력을 해 줘야 하기 때문에 interupt가 걸림
        punc = int(input("1 - punctuation directly setting (Remove punctuation)\n"
                         "2 - existed punctuation usage (Replace to spacebard)\n"))

        if (punc == 1):
            punc = input("[Punctuation]\n"
                         "(just write each punctuation without spacebar and write Enter key when you are done)\n")
            data['text'] = data['text'].apply(lambda x: self.input_remove_specialCharacter(x, punc))
        elif (punc == 2):
            data['text'] = data['text'].apply(lambda x: self.replace_specialCharacter(x))

        # data['text'] = data['text'].apply(lambda x: self.remove_specialCharacter(x))
        # print(data)
        print(data)

        self.writeData(data)


if __name__ == "__main__":
    p = Problem1()
    p.run()