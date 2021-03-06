import os
from datetime import datetime
'''

перед розділенням вхідного результуючого файлу на вхід і вихід в якійсь із
останніх колонок я прописую цифри від 1 до упору, потім файл ділиться на
вхід і вихід, обробляється окремо і зливається в 1 файл, який сотрується
по даній колонці і ми можем все скопіювати за 1 раз.
'''
'''
think about:
in 4 result column called conformity are we need to write 'Yes' if cdr's are
exactly equal cause they are semi equal all the time
'''


class ResultRecord:
    '''
    міжмісто    3270    так    так    так
    cdr_set=3270 and switch_id in ('4462')    1202    3252    32
    DA_CALLS_LVV    IA_IN    "АТ ""Укртранснафта"" , м. Львів"        0
    '''
    def __init__(self, index=None, trafic_type=None, ms_cdr=None,
                 availability=None, conformity=None, dur_conformity=None,
                 load_condition=None, operator_id=None, account_number=None,
                 region=None, source_name=None, io=None, operators_name=None,
                 recipient_id=None, processing_local=None, description=None,
                 more_info=None):
        """
        index - index :))
        type - traffic type misto/ migmisto/ migmisto 800/ migmisto 800 900
               / None
        ms_cdr - all ms cdr's from what we collect data to this account
        availability(najavnist') - tak/ ni / comzal
        conformity(vidpovidnist') - does a filter conndition in ms equal to
                                    filter condition in intracotect
        dur_conformity - does sum(dur) in ms is equal to sum(dur)
                         in intraconect
        load_condition - condition of filtering data in intraconect
        operator_id
        account_number
        region
        source_name - da_calls_lvv / do_calls_lvv/ da_callo_lvv
        io(input/output) - IA_IN/ IA_OUT
        operators_name - name of operator
        recipient_id - hard to say, some data column
        processing_local - 0 - no, 1 - yes, 2 - local only
        description
        more_info

        calculated fields:
        by method $get_list_of_cdrs() we will be fill the $list_of_cdrs
        list_of_cdrs = []

        """
        self.index = index
        self.trafic_type = trafic_type
        self.ms_cdr = ms_cdr
        self.availability = availability
        self.conformity = conformity
        self.dur_conformity = dur_conformity
        self.load_condition = load_condition
        self.operator_id = operator_id
        self.account_number = account_number
        self.region = region
        self.source_name = source_name
        self.io = io
        self.operators_name = operators_name
        self.recipient_id = recipient_id
        self.processing_local = processing_local
        self.description = description
        self.more_info = more_info
        # calculated fields
        self.list_of_cdrs = []

    def __str__(self):
        '''
        s = __init__ parameters
        print('str(' + s.replace('=None, ', ') + " , " + str('))
        '''
        return (str(self.index) + " [" +
                str(self.trafic_type) + " , " + str(self.ms_cdr) + " , " +
                str(self.availability) + " , " + str(self.conformity) + " , " +
                str(self.dur_conformity) + " , " + str(self.load_condition) +
                " , " + str(self.operator_id) + " , " +
                str(self.account_number) + " , " + str(self.region) +
                " , " + str(self.source_name) + " , " + str(self.io) +
                " , " + str(self.operators_name) + " , " +
                str(self.recipient_id) + " , " + str(self.processing_local) +
                " , " + str(self.description) + " , " +
                str(self.more_info) + "]")

    def get_list_of_cdrs(self):
        cdr = self.load_condition
        # print(cdr)
        if 'cdr_set=' in cdr or 'cdr_set =' in cdr or 'cdr_set  =' in cdr:
            # print('bingo')
            cdr_to_add = (
                [self.load_condition[self.load_condition.find('=')
                                     + 1:].strip()[:4]])
            #        тут змінив закриваючу дужку була перед [:4]
            # print(cdr_to_add)
            pass

        elif 'cdr_set in' in cdr or 'cdr_set  in' in cdr:
            # print('bongo')
            first_left_open_bracket = self.load_condition.find('(')
            first_left_close_bracket = self.load_condition.find(')')
            cdrs = (self.load_condition[first_left_open_bracket + 1:
                                        first_left_close_bracket])
            cdrs = cdrs.split(',')
            # print(cdrs)
            for index in range(len(cdrs)):
                cdrs[index] = cdrs[index].strip(" ").strip("'")
            # print(cdrs)
            cdr_to_add = cdrs
            pass
        else:
            print(f"ERROR with value {self.load_condition}")
            error_file = open(log_file_name, "a")
            print(f"{datetime.now()} Error while converting cdrs from",
                  f"text to list in line number {self.index}",
                  f"with value {self.load_condition}", file=error_file)
            error_file.close()
            self.trafic_type = "Error"
            self.ms_cdr = "Error"
            self.availability = (f"{datetime.now()} Error while converting",
                                 f"cdrs from",
                                 f"text to list in line number {self.index}",
                                 f"with value {self.load_condition}")
            self.conformity = "Error"
            self.dur_conformity = "Error"
            self.list_of_cdrs.append("Error")
            return

        for index in range(len(cdr_to_add)):
            self.list_of_cdrs.append(cdr_to_add[index])


class NtkRecord:
    def __init__(self, index=None, operator_id=None, account_number=None,
                 cdr_set_id=None, call_type=None, count=None, sum_dur=None):
        '''1203    3226    3216    2    30689    6538615'''
        self.index = index
        self.operator_id = operator_id
        self.account_number = account_number
        self.cdr_set_id = cdr_set_id
        self.call_type = call_type
        self.count = count
        self.sum_dur = sum_dur

    def __str__(self):
        return (str(self.index) + " [" + str(self.operator_id) + " , " +
                str(self.account_number) + " , " + str(self.cdr_set_id) +
                " , " + str(self.call_type) + " , " + str(self.count) +
                str(self.sum_dur) + "]")

    def get_ntk_data(self, cdr, list_call_type):
        '''
        we will be sent list with one value [2,] if we need local traffic
        and list with length 2 with value [2, -55] if we need intercity
        traffic special for using in condition "not in [2,-55]"
        if len(list_call_type) > 1
        '''
        list_to_return = []
        if len(list_call_type) == 1:
            for index in range(len(ntk_records)):
                if (cdr == ntk_records[index].cdr_set_id and
                        ntk_records[index].call_type in list_call_type):
                    list_to_return.append([int(cdr),
                                           int(ntk_records[index].call_type),
                                           int(ntk_records[index].sum_dur)])
        else:  # len(list_call_type) > 1
            for index in range(len(ntk_records)):
                if (cdr == ntk_records[index].cdr_set_id and
                        ntk_records[index].call_type not in list_call_type):
                    list_to_return.append([int(cdr),
                                           int(ntk_records[index].call_type),
                                           int(ntk_records[index].sum_dur)])

        return list_to_return


class MsRecord:
    def __init__(self, index=None, station=None, cdr_set=None,
                 substr_service_type=None, count=None, sum_dur=None):
        self.index = index
        self. station = station
        self.cdr_set = cdr_set
        self.substr_service_type = substr_service_type
        self.count = count
        self.sum_dur = sum_dur

    def __str__(self):
        return (str(self.index) + " [" + str(self.station) + " , " +
                str(self.cdr_set) + " , " + str(self.substr_service_type) +
                " , " + str(self.count) + " , " + str(self.sum_dur) + "]")

    def get_ms_data(self, cdr, substr_trafic_type):
        list_to_return = []
        for index in range(len(ms_records)):
            if (ms_records[index].cdr_set == cdr and
                    ms_records[index].substr_service_type
                    in substr_trafic_type):
                list_to_return.append(
                            [int(cdr),
                             int(ms_records[index].substr_service_type),
                             int(ms_records[index].sum_dur)])
        return list_to_return


def sum_third(in_list):
    summ = 0
    for index in range(len(in_list)):
        summ += in_list[index][2]
    return summ


def get_list_of_traffic_types(in_list):
    set_to_return = set()
    for element in in_list:
        if element[1] == 0:
            set_to_return.add('Міжмісто')
        elif element[1] == 8:
            set_to_return.add('800')
        elif element[1] == 9:
            set_to_return.add('900')
        else:
            set_to_return.add(str(element[1]))
            print(f"ERROR with value {element[1]} in ntk_cdrs_list",
                  f"{in_list}. Value not subscribed")
            error_file = open(log_file_name, "a")
            print(f"{datetime.now()} Error with value {element[1]} in",
                  f"ntk_cdrs_list {in_list}. Value not subscribed",
                  file=error_file)
            error_file.close()
    list_to_return = []
    if 'Міжмісто' in set_to_return:
        list_to_return.append('Міжмісто')
    if '800' in set_to_return:
        list_to_return.append('800')
    if '900' in set_to_return:
        list_to_return.append('900')
    return list_to_return


def check_for_warnings():
    '''
    type of $list_of_cdr_type will be [list_of_cdrs, 2(local)/0(intercity)]
    and than we will write to $log_file all pairs which has more than one
    record in this list, to operate them manually.
    for now lets ignore all comzal records.
    '''
    list_of_cdr_type = []
    reserve_list_of_cdr_type_with_comzal = []
    set_of_cdr_type = set()
    for index in range(len(result_in_records)):
        if result_in_records[index].processing_local in ('2', '1'):
            traffic_type = '2'
        else:
            traffic_type = '0'
        reserve_list_of_cdr_type_with_comzal.append(
                    str([result_in_records[index].list_of_cdrs, traffic_type]))
        if result_in_records[index].source_name not in (da_calls_region,
                                                        da_callo_region):
            continue
        list_of_cdr_type.append(str([result_in_records[index].list_of_cdrs,
                                     traffic_type]))
        if str(list_of_cdr_type[-1]) in set_of_cdr_type:
            error_file = open(log_file_name, "a")
            print('Warning we find same cdr_set and processing_local',
                  'inside in_result_file with value', list_of_cdr_type[-1],
                  'at lines in_result_file',
                  reserve_list_of_cdr_type_with_comzal.index(
                     str(list_of_cdr_type[-1])), 'and', index, file=error_file)
            error_file.close()
            print('-+-+-+-+ Warning add log', list_of_cdr_type[-1],
                  'at line in in_result_file',
                  reserve_list_of_cdr_type_with_comzal.index(
                  str(list_of_cdr_type[-1])), 'and', index)
        else:
            set_of_cdr_type.add(list_of_cdr_type[-1])
        print(index, list_of_cdr_type[-1])


# main()
# Swich to Lviv

#===============================================================================
# data_in_folder = "ms_ntk_compare_lvv_in"
# result_in_file_name_name = "lviv in result file.txt"
# da_callo_region = 'DA_CALLO_LVV'
# da_calls_region = 'DA_CALLS_LVV'
# ms_in_file_name_name = 'lviv ms in.txt'
# ntk_in_file_name_name = 'lviv ntk in.txt'
#===============================================================================
# Switch to Luts'k
#===============================================================================
# data_in_folder = "ms_ntk_compare_lut_in"
# result_in_file_name_name = "lut result in.txt"
# da_callo_region = 'DA_CALLO_LUT'
# da_calls_region = 'DA_CALLS_LUT'
# ms_in_file_name_name = 'ms lut vhid.txt'
# ntk_in_file_name_name = 'ntk lut vhid.txt'
#===============================================================================

# Switch to Frankivs'k

data_in_folder = "ms_ntk_compare_ivf_in"
result_in_file_name_name = "ivf_result_in.txt"
da_callo_region = 'DA_CALLO_IVF'
da_calls_region = 'DA_CALLS_IVF'
ms_in_file_name_name = 'ivf_ms_vhid.txt'
ntk_in_file_name_name = 'ivf_ntk_vhid.txt'


# Swich to Uzhorod

#===============================================================================
# result_in_file_name_name = "result_in_file_uzh.txt"
# data_in_folder = "ms_ntk_compare_uzh_in"
# da_callo_region = 'DA_CALLO_UZH'
# da_calls_region = 'DA_CALLS_UZH'
# ms_in_file_name_name = 'uzh ms in.txt'
# ntk_in_file_name_name = 'uzh ntk in.txt'
#===============================================================================

log_file_name = os.path.join(os.getcwd(), data_in_folder, "error_log.txt")
ms_file_name = os.path.join(os.getcwd(), data_in_folder,
                            ms_in_file_name_name)
ntk_file_name = os.path.join(os.getcwd(), data_in_folder,
                             ntk_in_file_name_name)
result_in_file_name = os.path.join(os.getcwd(), data_in_folder,
                                   result_in_file_name_name)
result_out_file_name = os.path.join(os.getcwd(), data_in_folder,
                                    "result_in_file_export.txt")

# read ms file
ms_file = open(ms_file_name, "r")
ms_lines = ms_file.readlines()
size_of_result_ms_list = len(ms_lines)
ms_records = [None] * size_of_result_ms_list
in_ms_list_index = 0
out_ms_list_index = 0
while in_ms_list_index < size_of_result_ms_list:
    line_split = ms_lines[in_ms_list_index].split()
    # print(line_split)
    if len(line_split) == 5:
        ms_records[out_ms_list_index] = MsRecord(out_ms_list_index,
                                                 *line_split)
        in_ms_list_index += 1
        out_ms_list_index += 1
    else:
        print(f"Error in line from file number {in_ms_list_index} with value",
              f"{line_split}")
        error_file = open(log_file_name, "a")
        print(f"{datetime.now()} Error in file {ms_file_name} in line from",
              f"file number {in_ms_list_index}",
              f"with value {line_split} wait for 5 parameters and got",
              f"{len(line_split)}", file=error_file)
        error_file.close()
        size_of_result_ms_list -= 1
        in_ms_list_index += 1
        ms_records.pop()

# check for last None element if $ms_in_file has last empty line
if ms_records[-1] is None:
    ms_records.pop()

for record in ms_records:
    print(record)

# read ntk file
ntk_file = open(ntk_file_name)
ntk_lines = ntk_file.readlines()
size_of_result_ntk_list = len(ntk_lines)
ntk_records = [None] * size_of_result_ntk_list
in_ntk_list_index = 0
out_ntk_list_index = 0
while in_ntk_list_index < size_of_result_ntk_list:
    line_split = ntk_lines[in_ntk_list_index].split()
    # print(line_split)
    if len(line_split) == 6:
        ntk_records[out_ntk_list_index] = NtkRecord(out_ntk_list_index,
                                                    *line_split)
        in_ntk_list_index += 1
        out_ntk_list_index += 1
    else:
        print(f"Error in line from file number {in_ntk_list_index} with value",
              f"{line_split}")
        error_file = open(log_file_name, "a")
        print(f"{datetime.now()} Error in file {ntk_file_name} in line from",
              f"file number {in_ntk_list_index}",
              f"with value {line_split} wait for 5 parameters and got",
              f"{len(line_split)}", file=error_file)
        error_file.close()
        size_of_result_ntk_list -= 1
        in_ntk_list_index += 1
        ntk_records.pop()

for record in ntk_records:
    print(record)

# read result_in file
result_in_file = open(result_in_file_name)
result_in_lines = result_in_file.readlines()
size_of_result_in_list = len(result_in_lines)

# erasing '\n' in the end of lines
for index in range(size_of_result_in_list):
    result_in_lines[index] = result_in_lines[index].rstrip()

result_in_records = [None] * size_of_result_in_list
in_result_in_list_index = 0
out_result_in_list_index = 0
while in_result_in_list_index < size_of_result_in_list:
    line_split = result_in_lines[in_result_in_list_index].split("\t")
    if line_split[-1] == '\n':
        line_split.pop()
    print(in_result_in_list_index, "line_split =", line_split)
    if len(line_split) == 15:
        result_in_records[out_result_in_list_index] = ResultRecord(
                                                out_result_in_list_index,
                                                *line_split)
        in_result_in_list_index += 1
        out_result_in_list_index += 1
    else:
        print(f"Error in line from file number {result_in_file_name} with value",
              f"{line_split} wait for 15 parameters and got",
              f"{len(line_split)}")
        error_file = open(log_file_name, "a")
        print(f"{datetime.now()} Error in file {result_in_file_name} in line",
              f"from file number {in_result_in_list_index}",
              f"with value {line_split} wait for 15 parameters and got",
              f"{len(line_split)}", file=error_file)
        error_file.close()
        size_of_result_in_list -= 1
        in_result_in_list_index += 1
        result_in_records.pop()

# for record in result_in_records:
#     print(record)


# start work
# ['міжмісто, 800, 900', '3275', 'так', 'так', 'так', 'cdr_set in (3275, 3337)'
# , '1204', '3226', '32', 'DA_CALLS_LVV', 'IA_IN', '0', '']
for index in range(len(result_in_records)):
    # error
    if 'Error' in str(result_in_records[index]):
        print('Error')
        continue
    # comzal
    if (result_in_records[index].io == 'IA_IN' and
            result_in_records[index].source_name == da_callo_region):
        result_in_records[index].availability = 'Комзал'
        continue
    # vhid ne comzal
    # lets find list of cdr's $result_in_redord[i].load_condition

    if (result_in_records[index].io == 'IA_IN' and
            result_in_records[index].source_name == da_calls_region):
        result_in_records[index].get_list_of_cdrs()
        # lets make empty ours lists for accumulate data for all
        # for different cdr's in $result_in_records[index].load_condition
        list_of_ms_cdrs_data = []
        list_of_ntk_cdrs_data = []
        # неочевдина для мене зараз наступна умова, цей список в принципі
        # не має бути пустий тобто вона завжди виконується,
        #  хз навіщо я її писав
        if result_in_records[index].list_of_cdrs:
            print(f"result_in_records[{index}].list_of_cdrs =",
                  result_in_records[index].list_of_cdrs)
            # dividing analyze for city and intercity
            if result_in_records[index].processing_local == '2':
                for cdr_index in range(len(
                        result_in_records[index].list_of_cdrs)):
                    # ms_records[0] 0 because we didn't need exact value
                    list_of_ms_cdrs_data += (ms_records[0].get_ms_data(
                        # second parameter ['1'] we will be check for
                        # ms_records.cdr in ['1'] or in ['2','3']
                        result_in_records[index].list_of_cdrs[cdr_index],
                        ['1']))

                    list_of_ntk_cdrs_data += ntk_records[0].get_ntk_data(
                        # second parameter ['2'] we will be check for
                        # nkt_records.cdr_id in ['2'] or not in ['2','-55']
                        # if len(second_parameter) > 1
                        result_in_records[index].list_of_cdrs[cdr_index],
                        ['2'])

            # ===============================================================
            # print(index, result_in_records[index].list_of_cdrs[cdr_index])
            # print(list_of_ms_cdrs_data, sum_third(list_of_ms_cdrs_data))
            # print(list_of_ntk_cdrs_data, sum_third(list_of_ntk_cdrs_data))
            # ===============================================================

                if not list_of_ms_cdrs_data and not list_of_ntk_cdrs_data:
                    result_in_records[index].availability = 'Ні'
                    continue

                result_in_records[index].trafic_type = 'Місто'
                # fill second column with all distinct cdrs with data in ms
                if list_of_ms_cdrs_data:
                    set_of_cdrs_with_data = set()
                    for item in list_of_ms_cdrs_data:
                        set_of_cdrs_with_data.add(str(item[0]))

                    print("set =", ','.join(set_of_cdrs_with_data))
                    result_in_records[index].ms_cdr = ','.join(
                                                        set_of_cdrs_with_data)

                result_in_records[index].availability = 'Так'
                result_in_records[index].conformity = 'Так'

                if (sum_third(list_of_ms_cdrs_data) ==
                        sum_third(list_of_ntk_cdrs_data)):
                    result_in_records[index].dur_conformity = 'Так'
                    print("True")
                else:
                    result_in_records[index].dur_conformity = 'Ні'

            else:  # result_in_records[index].processing_local != '2'
                for cdr_index in range(len(
                                    result_in_records[index].list_of_cdrs)):
                    list_of_ms_cdrs_data += (ms_records[0].get_ms_data(
                            result_in_records[index].list_of_cdrs[cdr_index],
                            ['2', '3']))
                    list_of_ntk_cdrs_data += ntk_records[0].get_ntk_data(
                        result_in_records[index].list_of_cdrs[cdr_index],
                        ['2', '-55'])
                print(index, result_in_records[index].list_of_cdrs[cdr_index])
                print(list_of_ms_cdrs_data, sum_third(list_of_ms_cdrs_data))
                print(list_of_ntk_cdrs_data, sum_third(list_of_ntk_cdrs_data))
                if not list_of_ms_cdrs_data and not list_of_ntk_cdrs_data:
                    result_in_records[index].availability = 'Ні'
                    continue
                list_of_traffic_types = get_list_of_traffic_types(
                                        list_of_ntk_cdrs_data)
                result_in_records[index].trafic_type = ','.join(
                            list_of_traffic_types)
                if list_of_ms_cdrs_data:
                    set_of_cdrs_with_data = set()
                    for item in list_of_ms_cdrs_data:
                        set_of_cdrs_with_data.add(str(item[0]))

                    print("set =", ','.join(set_of_cdrs_with_data))
                    result_in_records[index].ms_cdr = ','.join(
                                                        set_of_cdrs_with_data)
                result_in_records[index].availability = 'Так'
                result_in_records[index].conformity = 'Так'
                if (sum_third(list_of_ms_cdrs_data) ==
                        sum_third(list_of_ntk_cdrs_data)):
                    result_in_records[index].dur_conformity = 'Так'
                    # print("True")
                else:
                    result_in_records[index].dur_conformity = 'Ні'

                    # print(list_of_ntk_cdrs_data)
                    # for ms_index in range(len(ms_records)):
                    #     if result_in_records[index].list_of_cdrs[cdr_index]
                    # list_of_ntk_cdrs_data = []
        # print(result_in_records[index].load_condition)
        # print(result_in_records[index].list_of_cdrs)

'''
Rising Warnings when in result_in_file present more than one record with
the same cdr and in $load_condition and same $processing_local(2 or not 2)
value we rise an warning to check this situation manually
'''
check_for_warnings()


for record in result_in_records:
    print(record)


result_out_file_for_vrntk_in = open(result_out_file_name, "w")

for index in range(len(result_in_records)):
    print(str(result_in_records[index].trafic_type) + "\t" +
          str(result_in_records[index].ms_cdr) + "\t" +
          str(result_in_records[index].availability) + "\t" +
          str(result_in_records[index].conformity) + "\t" +
          str(result_in_records[index].dur_conformity) + "\t" +
          str(result_in_records[index].load_condition) + "\t" +
          str(result_in_records[index].operator_id) + "\t" +
          str(result_in_records[index].account_number) + "\t" +
          str(result_in_records[index].region) + "\t" +
          str(result_in_records[index].source_name) + "\t" +
          str(result_in_records[index].io) + "\t" +
          str(result_in_records[index].operators_name) + "\t" +
          str(result_in_records[index].recipient_id) + "\t" +
          str(result_in_records[index].processing_local) + "\t" +
          str(result_in_records[index].description) + "\t" +
          str(result_in_records[index].more_info),
          file=result_out_file_for_vrntk_in)
result_out_file_for_vrntk_in.close()
