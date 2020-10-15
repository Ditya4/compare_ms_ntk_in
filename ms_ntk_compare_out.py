import os
from datetime import datetime

"""
в файлі мс_нтк в нас є оператор, рахунок, тип трафіку і сдри а в вибірці
з інтраконекту є оператор рахунок і дані
а порівнювати маєм з мсом де є сдр і дані(при чому сумоване по угоді,
тобто різні сдри, які сідають на одну угоду
нам не принципово розділяти), тобто потрібно прописати сдри на відповідні угоди
з типом трафіку далі, в нас будуть на деяких угодах тоді по 2-5 сдрів замість
одного, який був раніше для сумування воно б мало не впливати, але як
прописувати потрібна ідея
приклади сдрів з файлу мс_нтк
cdr_set_out=3233
cdr_set_out in ('3267','3265')
cdr_set_out=3274
cdr_set_out in ('4221','3264','3274', '3265')
в нас в ін_файл_рекордс є ліст із даних сідіарів для кожного запису але як
взнати який з них, скоріше за все потрібно буде
писати даний ліст як ідентифікатор в нтк_рекордс
"""


class ResultRecord:
    '''
    міжмісто    3270    так    так    так
    cdr_set_out=3270 and switch_id in ('4462')    1202    3252    32
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
        print(cdr)
        if 'cdr_set_out=' in cdr or 'cdr_set_out =' in cdr:
            print('bingo')
            cdr_to_add = (
                [self.load_condition[self.load_condition.find('=')
                                     + 1:].strip()[:4]])
            #        тут змінив закриваючу дужку була перед [:4]
            # print(cdr_to_add)
            pass

        elif 'cdr_set_out in' in cdr or 'cdr_set_out  in' in cdr:
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
            self.availability = "Error"
            self.conformity = "Error"
            self.dur_conformity = "Error"
            self.list_of_cdrs.append("Error")
            return

        for index in range(len(cdr_to_add)):
            self.list_of_cdrs.append(cdr_to_add[index])


class NtkRecord:
    def __init__(self, index=None, operator_id=None, account_number=None,
                 recipient_id=None, out_tg=None, call_type=None, count=None,
                 sum_dur=None):
        '''
        operator_id, account_number, recipient_id, out_tg,
        call_type, count (*), sum(duration)
        1202    3252    4462    1490    -1    1011    29283
        '''
        self.index = index
        self.operator_id = operator_id
        self.account_number = account_number
        self.recipient_id = recipient_id
        self.out_tg = out_tg
        self.call_type = call_type
        self.count = count
        self.sum_dur = sum_dur

        # calculated fields
        self.list_of_cdrs = []
        self.fill_list_of_cdrs()

    def __str__(self):
        if self.list_of_cdrs:
            return (str(self.index) + " [" + str(self.operator_id) + " , " +
                    str(self.account_number) + " , " + str(self.recipient_id) +
                    " , " + str(self.out_tg) + " , " + str(self.call_type) +
                    " , " + str(self.count) + " , " + str(self.sum_dur) + "]" +
                    " " + str(self.list_of_cdrs))
        else:
            return (str(self.index) + " [" + str(self.operator_id) + " , " +
                    str(self.account_number) + " , " + str(self.recipient_id) +
                    " , " + str(self.out_tg) + " , " + str(self.call_type) +
                    " , " + str(self.count) + " , " + str(self.sum_dur) + "]")

    def fill_list_of_cdrs(self):
        for index in range(len(result_out_records)):
            if (result_out_records[index].operator_id == self.operator_id and
                    (result_out_records[index].account_number ==
                     self.account_number)):
                if self.call_type in ('-2'):
                    if result_out_records[index].processing_local == '2':
                        self.list_of_cdrs = (
                            result_out_records[index].list_of_cdrs)
                elif self.call_type not in ('-2'):
                    if result_out_records[index].processing_local not in ('2'):
                        self.list_of_cdrs = (
                            result_out_records[index].list_of_cdrs)

    def get_ntk_data(self, cdr, list_call_type):
        pass

        '''
        all comments in this method are False

        we will be sent list with one value [2,] if we need local traffic
        and list with length 2 with value [2, -55] if we need intercity
        traffic special for using in condition "not in [2,-55]"
        if len(list_call_type) > 1
        '''
        """
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
        """


class MsRecord:
    def __init__(self, index=None, station=None, out_tg=None, cdr_set_out=None,
                 substr_service_type=None, count=None, sum_dur=None):
        '''
        switch_id, out_tg, cdr_set_out, substr(service_type,0,1),
        count (*), sum (duration)
        3200    0491    4265    2    47    3107
        '''

        self.index = index
        self. station = station
        self.out_tg = out_tg
        self.cdr_set_out = cdr_set_out
        self.substr_service_type = substr_service_type
        self.count = count
        self.sum_dur = sum_dur

    def __str__(self):
        return (str(self.index) + " [" + str(self.station) + " , " +
                str(self.out_tg) + " , " +
                str(self.cdr_set_out) + " , " + str(self.substr_service_type) +
                " , " + str(self.count) + " , " + str(self.sum_dur) + "]")

    def get_ms_data(self, cdr, substr_trafic_type):
        list_to_return = []
        for index in range(len(ms_records)):
            if (ms_records[index].cdr_set_out == cdr and
                    ms_records[index].substr_service_type
                    in substr_trafic_type):
                list_to_return.append(
                            [int(cdr),
                             int(ms_records[index].substr_service_type),
                             int(ms_records[index].sum_dur)])
        return list_to_return


def read_result_out_file(result_out_input_file_name):
    result_out_file = open(result_out_input_file_name)
    result_out_lines = result_out_file.readlines()
    size_of_result_out_list = len(result_out_lines)

    # erasing '\n' in the end of lines
    for index in range(size_of_result_out_list):
        result_out_lines[index] = result_out_lines[index].rstrip()

    result_out_records = [None] * size_of_result_out_list
    in_result_out_list_index = 0
    out_result_out_list_index = 0
    while in_result_out_list_index < size_of_result_out_list:
        line_split = result_out_lines[in_result_out_list_index].split("\t")
        if line_split[-1] == '\n':
            line_split.pop()
        print(in_result_out_list_index, "line_split =", line_split)
        if len(line_split) == 14:
            result_out_records[out_result_out_list_index] = ResultRecord(
                                                    out_result_out_list_index,
                                                    *line_split)
            result_out_records[out_result_out_list_index].get_list_of_cdrs()
            in_result_out_list_index += 1
            out_result_out_list_index += 1
        else:
            # ===================================================================
            # print(f"Error in line from file number {in_ntk_list_index} with",
            #       f"value {line_split} wait for 14 parameters and got",
            #       f"{len(line_split)}")
            # ===================================================================
            error_file = open(log_file_name, "a")
            print(f"{datetime.now()} Error in file",
                  f"{result_out_input_file_name}",
                  f"in line from file number {in_result_out_list_index}",
                  f"with value {line_split} wait for 14 parameters and got",
                  f"{len(line_split)}", file=error_file)
            error_file.close()
            size_of_result_out_list -= 1
            in_result_out_list_index += 1
            result_out_records.pop()

    return result_out_records


def read_ntk_file(ntk_file_name):
    ntk_file = open(ntk_file_name)
    ntk_lines = ntk_file.readlines()
    size_of_result_ntk_list = len(ntk_lines)
    ntk_records = [None] * size_of_result_ntk_list
    in_ntk_list_index = 0
    out_ntk_list_index = 0
    while in_ntk_list_index < size_of_result_ntk_list:
        line_split = ntk_lines[in_ntk_list_index].split()
        # print(line_split)
        if len(line_split) == 7:
            ntk_records[out_ntk_list_index] = NtkRecord(out_ntk_list_index,
                                                        *line_split)
            in_ntk_list_index += 1
            out_ntk_list_index += 1
        else:
            print(f"Error in line from file number {in_ntk_list_index}",
                  f"with value {line_split}")
            error_file = open(log_file_name, "a")
            print(f"{datetime.now()} Error in file {ntk_file_name} in",
                  f"line from file number {in_ntk_list_index}",
                  f"with value {line_split} wait for 7 parameters and got",
                  f"{len(line_split)}", file=error_file)
            error_file.close()
            size_of_result_ntk_list -= 1
            in_ntk_list_index += 1
            ntk_records.pop()
    return ntk_records


def read_ms_file(ms_file_name):
    ms_file = open(ms_file_name, "r")
    ms_lines = ms_file.readlines()
    size_of_result_ms_list = len(ms_lines)
    ms_records = [None] * size_of_result_ms_list
    in_ms_list_index = 0
    out_ms_list_index = 0
    while in_ms_list_index < size_of_result_ms_list:
        line_split = ms_lines[in_ms_list_index].split()
        # print(line_split)
        if len(line_split) == 6:
            ms_records[out_ms_list_index] = MsRecord(out_ms_list_index,
                                                     *line_split)
            in_ms_list_index += 1
            out_ms_list_index += 1
        else:
            print(f"Error in line from file number {in_ms_list_index}",
                  f"with value {line_split}")
            error_file = open(log_file_name, "a")
            print(f"{datetime.now()} Error in file {ms_file_name}",
                  f"in line from file number {in_ms_list_index}",
                  f"with value {line_split} wait for 6 parameters and got",
                  f"{len(line_split)}", file=error_file)
            error_file.close()
            size_of_result_ms_list -= 1
            in_ms_list_index += 1
            ms_records.pop()
    # check and erase all last None-elements in $ms_records list
    while ms_records[-1] is None:
        ms_records.pop()
    return ms_records


# main()

data_in_folder = "ms_ntk_compare_lvv_out"
result_out_file_name_name = "result_out_file_lviv.txt"
ntk_file_name_name = "порівняня мс інтраконект тут нтк львів вихід.txt"
ms_file_name_name = "порівняня мс інтраконект тут мс львів вихід.txt"
DO_CALLS_LVV = 'DO_CALLS_LVV'
DO_CALLO_LVV = 'DO_CALLO_LVV'

result_out_input_file_name = os.path.join(os.getcwd(), data_in_folder,
                                          result_out_file_name_name)
ntk_file_name = os.path.join(os.getcwd(), data_in_folder, ntk_file_name_name)
ms_file_name = os.path.join(os.getcwd(), data_in_folder, ms_file_name_name)
log_file_name = os.path.join(os.getcwd(), data_in_folder, "error_log.txt")

'''
ms_file_name = os.path.join(os.getcwd(), data_in_folder,
                            "порівняння_мс_нтк_вхід_мс.txt")
ntk_file_name = os.path.join(os.getcwd(), data_in_folder,
                             "порівняння_мс_нтк_вхід_нтк.txt")

# result_out_input_file_name = os.path.join(os.getcwd(), data_in_folder,
#                                    "result_out_file.txt")
'''
result_out_records = read_result_out_file(result_out_input_file_name)
for record in result_out_records:
    print(record)

ntk_records = read_ntk_file(ntk_file_name)
for record in ntk_records:
    print(record)

ms_records = read_ms_file(ms_file_name)
for record in ms_records:
    print(record)
