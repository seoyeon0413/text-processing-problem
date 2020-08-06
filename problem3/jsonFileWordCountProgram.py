import json
import sys
from collections import Counter

import pandas as pd
import yaml


class JsonFileWordCountProgram:

    def get_yaml_property(self):
        '''
        yaml 형태의 property 파일을 읽어들임
        :return: object 형태의 데이터
        '''
        with open("property.yml") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        return data

    def get_key_data_from_json_file(self, inputFileName, key):
        '''
        json 파일에서 해당하는 key값에만 해당하는 데이터를 가져옴
        :param inputFileName: input 파일 이름
        :param key: 가져올 key의 이름
        :return: key값에만 해당하는 데이터
        '''

        key_data = ""
        with open(inputFileName, encoding='UTF-8') as f:
            for line in f:
                json_data = json.loads(line)
                key_data += json_data[key]

        return key_data

    def split_data_by_blank(self, raw_data):
        '''
        string 형태의 input을 공백으로 나눠서 list 형태로 return
        :param raw_data: input data
        :return: 공백으로 나눠진 list 형태의 데이터
        '''

        splitted_data = raw_data.split()

        return splitted_data

    def list_to_set(self, list_data):
        '''
        list 형태의 데이터를 set 형태의 데이터로 변환
        :param list_data: list 형태의 데이터
        :return: set 형태의 데이터
        '''

        set_data = set(list_data)

        return set_data

    def get_count_by_word(self, splitted_data):
        '''
        각 단어의 개수를 셈
        :param splitted_data: 공백 단위로 나눠진 list 형태의 데이터
        :return: counted_data = 각 단어의 개수가 세어진 데이터, the_number_of_word = 파일이 가지고 있는 총 단어의 개수 (set)
        '''

        counted_data = Counter(splitted_data)
        the_number_of_word = len(self.list_to_set(splitted_data))

        return counted_data, the_number_of_word

    def sort_collections_to_list(self, property_data, counted_data, length):
        '''
        collections 형태의 데이터를 정렬하여 list 형태로 return
        :param property_data: sort option을 선택하기 위한 property data
        :param counted_data: 각 단어가 몇 개 인지 세어진 데이터
        :param length: input 파일이 가지고 있는 총 단어의 개수 (set)
        :return: 내림차순이나 오름차순으로 정렬한 list 형태의 데이터
        '''

        sort_option = property_data['sort option']
        
        if sort_option == 'descending':
            sorted_list = counted_data.most_common(n=length)   # 내림차순
        elif sort_option == 'ascending':
            sorted_list = list(reversed(counted_data.most_common(n=length)))  # 오름차순
        else:
            print("Error: property 파일에 적을 수 있는 'sort option' 내림차순과 오름차순입니다. (option: descending, ascending)")
            sys.exit()

        return sorted_list

    def list_to_dict(self, list_data):
        '''
        list 형태의 데이터를 dictionary 형태의 데이터로 변환
        :param list_data:
        :return: dictionary 형태의 데이터
        '''
        dict_data = dict((x, y) for x, y in list_data)

        return dict_data

    def dict_to_dataframe(self, dict_data, columns_name):
        '''
        dictionary 형태에서 dataframe 형태로 변환
        :param dict_data: dictionary 형태의 데이터
        :param columns_name: dataframe의 column 이름을 담은 list
        :return: dataframe 형태의 데이터
        '''
        dataframe_data = pd.DataFrame.from_dict(dict_data, orient='index', columns=columns_name)

        return dataframe_data

    def write_result_data(self, property_data, output_data):
        '''
        확장자에 맞게 최종 데이터셋 저장
        :param property_data: 옵션을 선택하기 위한 property data
        :param output_data: 최종적으로 저장할 데이터
        :return: 없음
        '''

        outputFileName = property_data['output']
        try:
            ext = outputFileName.split('.')[1]
        except IndexError as e:
            print("'property' 파일의 'output'에 파일 확장자를 붙여서 적어주시기 바랍니다: {}".format(e))

        dict_data = self.list_to_dict(output_data)
        columns = ['count']
        final_data = self.dict_to_dataframe(dict_data, columns)
        print(final_data)

        if (ext == "csv"):  # result to csv
            try:
                final_data.to_csv(outputFileName, index=True, header=['count'], encoding='UTF-8-sig')
            except PermissionError as e:
                print("해당 CSV파일을 닫아주시기 바랍니다: {}".format(e))
        elif (ext == "txt"):  # result to txt
            with open(outputFileName, 'w', encoding='UTF-8') as file:
                for c in range(len(final_data)):
                    file.writelines(str(final_data.index[c]) + ' ' + str(final_data['count'][c]) + "\n")
        elif (ext == "json"):  # result to json
            final_data.to_json(outputFileName, orient='table', encoding='UTF-8')
        else:
            print("Error: 해당되는 확장자만 적어주세요. (csv, txt, json)")
            sys.exit()

    def run(self):
        '''
        main function of this program: 단어 개수 내림차순 출력하기
        :return:
        '''

        property_data = self.get_yaml_property()
        key_data_from_json = self.get_key_data_from_json_file(property_data["input"], property_data["key"])
        split_data = self.split_data_by_blank(key_data_from_json)
        counted_data, num = self.get_count_by_word(split_data)
        sorted_list = self.sort_collections_to_list(property_data, counted_data, num)
        self.write_result_data(property_data, sorted_list)





if __name__ == "__main__":
    jsonFileWordCountProgram = JsonFileWordCountProgram()
    jsonFileWordCountProgram.run()
