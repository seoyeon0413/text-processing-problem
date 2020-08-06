import gc
import os
import json
import sys
import time
from collections import Counter

import numpy as np
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

    def get_key_data_from_json_file(self, input_file_name, key):
        '''
        json 파일에서 해당하는 key값에만 해당하는 데이터를 가져옴
        :param inputFileName: input 파일 이름
        :param key: 가져올 key의 이름
        :return: key값에만 해당하는 2차원 list 형태의 데이터
        '''

        key_data = []
        with open(input_file_name, encoding='UTF-8') as f:
            for line in f:
                json_data = json.loads(line)
                key_data.append(json_data[key])


        # chunk_size = 10000
        # for chunk in pd.read_json(input_file_name, encoding='utf-8', lines = True, chunksize=chunk_size):
        #     for i in range(chunk_size):
        #         key_data += str(chunk.iloc[i,2])
        #         print(chunk.iloc[i,2])

        return key_data

    def split_data_by_blank(self, data):
        '''
        string 형태의 input을 공백으로 나눠서 2차원 list 형태로 return
        :param raw_data: input 데이터
        :return: 공백으로 나눠진 2차원 list 형태의 데이터
        '''

        for index in range(len(data)):
            data[index] = data[index].split()

        return data

    def get_count_by_word(self, splitted_data):
        '''
        각 단어의 개수를 셈
        :param splitted_data: 공백 단위로 나눠진 list 형태의 데이터
        :return: counted_data = 각 단어의 개수가 세어진 데이터, the_number_of_word = 파일이 가지고 있는 총 단어의 개수 (set)
        '''

        counted_data = Counter()
        for index in range(len(splitted_data)):
            counted_data.update(splitted_data[index])

        the_number_of_word = len([key for key, value in counted_data.items()])

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
        :return: 없음
        '''

        now = time.localtime()
        print("시작 시간: %04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))

        start_time1 = time.time()
        property_data = self.get_yaml_property()
        end_time1 = time.time()
        total_time1 = end_time1 - start_time1
        print("self.get_yaml_property: {} sec".format(total_time1))

        start_time2 = time.time()
        key_data_from_json = self.get_key_data_from_json_file(property_data["input"], property_data["key"])
        end_time2 = time.time()
        total_time2 = end_time2 - start_time2
        print("self.get_key_data_from_json_file: {} sec".format(total_time2))

        start_time3 = time.time()
        split_data = self.split_data_by_blank(key_data_from_json)
        end_time3 = time.time()
        total_time3 = end_time3 - start_time3
        print("self.split_data_by_blank: {} sec".format(total_time3))

        start_time4 = time.time()
        counted_data, num = self.get_count_by_word(split_data)
        end_time4 = time.time()
        total_time4 = end_time4 - start_time4
        print("self.get_count_by_word: {} sec".format(total_time4))

        start_time5 = time.time()
        sorted_list = self.sort_collections_to_list(property_data, counted_data, num)
        end_time5 = time.time()
        total_time5 = end_time5 - start_time5
        print("self.sort_collections_to_list: {} sec".format(total_time5))

        start_time6 = time.time()
        self.write_result_data(property_data, sorted_list)
        end_time6 = time.time()
        total_time6 = end_time6 - start_time6
        print("self.write_result_data: {} sec".format(total_time6))

        print("[프로그램 종료]")
        print("걸린 시간: {}".format(total_time1 + total_time2 + total_time3 + total_time4 + total_time5 + total_time6))





if __name__ == "__main__":
    jsonFileWordCountProgram = JsonFileWordCountProgram()
    jsonFileWordCountProgram.run()
