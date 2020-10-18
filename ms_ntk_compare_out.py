import os
from datetime import datetime

"""
список врнтк потрібно згрупувати по угода, рахунок, місто/міжмісто, список сдр,
каунт (*) і сум_дюр, хоча можна кожен раз пробігатись по всім угодам і
насумовувати на кожен сдр, в кінці кінців ми маєм це порівняти по тривалості
з містом/міжмістом з мс а там є вихідний сдр і місто/міжмісто давай почнем з
групування таблиці мс

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
        if self.list_of_cdrs:
            return (str(self.index) + " [" +
                    str(self.trafic_type) + " , " + str(self.ms_cdr) +
                    " , " + str(self.availability) + " , " +
                    str(self.conformity) + " , " + str(self.dur_conformity) +
                    " , " + str(self.load_condition) +
                    " , " + str(self.operator_id) + " , " +
                    str(self.account_number) + " , " + str(self.region) +
                    " , " + str(self.source_name) + " , " + str(self.io) +
                    " , " + str(self.operators_name) + " , " +
                    str(self.recipient_id) + " , " +
                    str(self.processing_local) +
                    " , " + str(self.description) + " , " +
                    str(self.more_info) + "]" + str(self.list_of_cdrs))

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
            # print('bingo')
            cdr_to_add = (
                [self.load_condition[self.load_condition.find('=')
                                     + 1:].strip()[:4]])
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

    def get_ntk_data(self, cdr_list, list_call_type):
        '''
        format of return data list is
        [cdr_list, int(call_type), int(sum_dur), recipient_id, out_tg
        '''
        list_to_return = []
        if len(list_call_type) == 1:
            for index in range(len(ntk_records)):
                if (cdr_list == ntk_records[index].list_of_cdrs and
                        ntk_records[index].call_type in list_call_type):
                    list_to_return.append([cdr_list,
                                           int(ntk_records[index].call_type),
                                           int(ntk_records[index].sum_dur),
                                           ntk_records[index].recipient_id,
                                           ntk_records[index].out_tg])
        else:  # len(list_call_type)>1-change call_type condition in to not in
            for index in range(len(ntk_records)):
                if (cdr_list == ntk_records[index].list_of_cdrs and
                        ntk_records[index].call_type not in list_call_type):
                    list_to_return.append([cdr_list,
                                           int(ntk_records[index].call_type),
                                           int(ntk_records[index].sum_dur),
                                           ntk_records[index].recipient_id,
                                           ntk_records[index].out_tg])

        return list_to_return


class MsRecord:
    def __init__(self, index=None, switch_id=None, out_tg=None,
                 cdr_set_out=None, substr_service_type=None,
                 count=None, sum_dur=None):
        '''
        switch_id, out_tg, cdr_set_out, substr(service_type,0,1),
        count (*), sum (duration)
        3200    0491    4265    2    47    3107
        '''

        self.index = index
        self.switch_id = switch_id
        self.out_tg = out_tg
        self.cdr_set_out = cdr_set_out
        self.substr_service_type = substr_service_type
        self.count = count
        self.sum_dur = sum_dur

    def __str__(self):
        return (str(self.index) + " [" + str(self.switch_id) + " , " +
                str(self.out_tg) + " , " +
                str(self.cdr_set_out) + " , " + str(self.substr_service_type) +
                " , " + str(self.count) + " , " + str(self.sum_dur) + "]")

    def get_ms_data(self, cdr, substr_trafic_type):
        '''
        format of return data list is
        [int(cdr), int(substr_srtvice_type), int(sum_dur), switch_id, out_tg]
        '''
        list_to_return = []
        for index in range(len(ms_records)):
            if (ms_records[index].cdr_set_out == cdr and
                    ms_records[index].substr_service_type
                    in substr_trafic_type):
                list_to_return.append(
                            [int(cdr),
                             int(ms_records[index].substr_service_type),
                             int(ms_records[index].sum_dur),
                             ms_records[index].switch_id,
                             ms_records[index].out_tg])
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


def sum_third(in_list):
    summ = 0
    for index in range(len(in_list)):
        summ += in_list[index][2]
    return summ


def get_list_of_traffic_types(in_list):
    set_to_return = set()
    for element in in_list:
        if element[1] == -1:
            set_to_return.add('Міжмісто')
        elif element[1] == -8:
            set_to_return.add('800')
        elif element[1] == -9:
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


def fill_empty_fields_in_result_out_records(result_out_records):
    for index in range(len(result_out_records)):
        print(str(result_out_records[index].load_condition))
        if 'Error' in str(result_out_records[index]):
            print('Error')

        elif (result_out_records[index].io == 'IA_OUT' and
                result_out_records[index].source_name == DO_CALLO_REGION):
            result_out_records[index].availability = 'Комзал'
            print('Комзал')

        elif (result_out_records[index].io == 'IA_OUT' and
                result_out_records[index].source_name == DO_CALLS_REGION):
            list_of_ms_cdrs_data = []
            list_of_ntk_cdrs_data = []
            print(f"result_out_records[{index}].list_of_cdrs =",
                  result_out_records[index].list_of_cdrs)
            # dividing analyze for city and intercity
            if result_out_records[index].processing_local == '2':
                for cdr_index in range(len(
                        result_out_records[index].list_of_cdrs)):
                    ms_result = ms_records[0].get_ms_data(
                        # second parameter ['1'] we will be check for
                        # ms_records.substr_service_type in ['1']
                        # or in ['2','3']
                        result_out_records[index].list_of_cdrs[cdr_index],
                        ['1'])
                    if ms_result:
                        list_of_ms_cdrs_data += ms_result
                # make 1 shift left cause we have same values
                #  in fields $cdr_list for records and ntk_data
                list_of_ntk_cdrs_data += (ntk_records[0].get_ntk_data(
                    # second parameter ['-2'] we will be check for
                    # nkt_records.cdr_id in ['-2'] or not in ['-2','-55']
                    # if len(second_parameter) > 1
                    result_out_records[index].list_of_cdrs,
                    ['-2']))

                print('ms')
                print(list_of_ms_cdrs_data)
                print('ntk')
                print(list_of_ntk_cdrs_data)
                if not list_of_ms_cdrs_data and not list_of_ntk_cdrs_data:
                    result_out_records[index].availability = 'Ні'
                else:
                    result_out_records[index].trafic_type = 'Місто'
                    # fill data for second column with
                    # all distinct cdrs in ms_cdrs
                    if list_of_ms_cdrs_data:
                        set_of_cdrs_with_data = set()
                        for item in list_of_ms_cdrs_data:
                            set_of_cdrs_with_data.add(str(item[0]))

                        print("set =", ','.join(set_of_cdrs_with_data))
                        result_out_records[index].ms_cdr = ','.join(
                                                        set_of_cdrs_with_data)
                    result_out_records[index].availability = 'Так'
                    result_out_records[index].conformity = 'Так'
                    if (sum_third(list_of_ms_cdrs_data) ==
                            sum_third(list_of_ntk_cdrs_data)):
                        result_out_records[index].dur_conformity = 'Так'
                        print("True")
                    else:
                        result_out_records[index].dur_conformity = 'Ні'

            else:  # result_out_records[index].processing_local != '2'
                for cdr_index in range(len(
                        result_out_records[index].list_of_cdrs)):
                    ms_result = ms_records[0].get_ms_data(
                        # second parameter ['1'] we will be check for
                        # ms_records.substr_service_type
                        # in ['1'] or in ['2','3']
                        result_out_records[index].list_of_cdrs[cdr_index],
                        ['2', '3'])
                    # By next if we filter empty lines, which could return
                    # $get_ms_data method
                    if ms_result:
                        list_of_ms_cdrs_data += ms_result
                # make 1 shift left cause we have same values
                # in fields $cdr_list for records and ntk_data
                list_of_ntk_cdrs_data += (ntk_records[0].get_ntk_data(
                    # second parameter ['-2'] we will be check for
                    # nkt_records.cdr_id in ['-2'] or not in ['-2','-55']
                    # if len(second_parameter) > 1
                    # '-55'- just random number which never could be in data
                    result_out_records[index].list_of_cdrs,
                    ['-2', '-55']))
                print('ms')
                print(list_of_ms_cdrs_data)
                print('ntk')
                print(list_of_ntk_cdrs_data)
                if not list_of_ms_cdrs_data and not list_of_ntk_cdrs_data:
                    result_out_records[index].availability = 'Ні'
                elif (result_out_records[index].io == 'IA_OUT' and
                        result_out_records[index].source_name ==
                        DO_CALLO_REGION):
                    result_out_records[index].availability = 'Комзал'
                    print('Комзал')
                elif (result_out_records[index].io == 'IA_OUT' and
                        result_out_records[index].source_name ==
                        DO_CALLS_REGION):
                    list_of_traffic_types = get_list_of_traffic_types(
                                        list_of_ntk_cdrs_data)
                    result_out_records[index].trafic_type = ','.join(
                            list_of_traffic_types)

                    if list_of_ms_cdrs_data:
                        set_of_cdrs_with_data = set()
                        for item in list_of_ms_cdrs_data:
                            set_of_cdrs_with_data.add(str(item[0]))

                        print("set =", ','.join(set_of_cdrs_with_data))
                        result_out_records[index].ms_cdr = ','.join(
                                                        set_of_cdrs_with_data)
                    result_out_records[index].availability = 'Так'
                    result_out_records[index].conformity = 'Так'

                    if (sum_third(list_of_ms_cdrs_data) ==
                            sum_third(list_of_ntk_cdrs_data)):
                        result_out_records[index].dur_conformity = 'Так'
                    else:
                        result_out_records[index].dur_conformity = 'Ні'


def check_for_warnings(result_out_records):
    '''
    Rising Warnings when in result_out_file are present more than one record
    with the same cdr and in $load_condition and same $processing_local
    (-2 or not -2) value we rise a warning to check this situation
    in future manually

    type of $list_of_cdr_type will be [list_of_cdrs, 2(local)/0(intercity)]
    and than we will write to $log_file all pairs which has more than one
    record in this list, to operate them manually.
    for now lets ignore all comzal records.
    '''
    list_of_cdr_type = []
    reserve_list_of_cdr_type_with_comzal = []
    set_of_cdr_type = set()
    for index in range(len(result_out_records)):
        if result_out_records[index].processing_local in ('2', '1'):
            traffic_type = '2'
        else:
            traffic_type = '0'
        reserve_list_of_cdr_type_with_comzal.append(
                    str([result_out_records[index].list_of_cdrs,
                         traffic_type]))
        if (result_out_records[index].source_name not in (DO_CALLO_REGION,
                                                          DO_CALLS_REGION) and
                'Error' not in str(result_out_records[index])):
            result_out_records[index].trafic_type = "Error"
            result_out_records[index].ms_cdr = "Error"
            result_out_records[index].availability = (
                                "Error. In result_out_records",
                                "at index", index, "source_name not in (",
                                DO_CALLO_REGION, ",", DO_CALLS_REGION, ")")
            result_out_records[index].conformity = "Error"
            result_out_records[index].dur_conformity = "Error"
        else:
            list_of_cdr_type.append(
                                str([result_out_records[index].list_of_cdrs,
                                     traffic_type]))
            if str(list_of_cdr_type[-1]) in set_of_cdr_type:
                error_file = open(log_file_name, "a")
                print('Warning we found same cdr_set_out and processing_local',
                      'inside out_result_file with value',
                      list_of_cdr_type[-1],
                      'at lines out_result_file',
                      reserve_list_of_cdr_type_with_comzal.index(
                          str(list_of_cdr_type[-1])),
                      'and', index, file=error_file)
                error_file.close()
                result_out_records[index].availability = (
                        'Warning we found same cdr_set_out and',
                        'processing_local',
                        'inside out_result_file with value',
                        list_of_cdr_type[-1],
                        'at lines out_result_file',
                        reserve_list_of_cdr_type_with_comzal.index(
                            str(list_of_cdr_type[-1])),
                        'and', index)
                result_out_records[index].conformity = 'Warning'
            else:
                set_of_cdr_type.add(list_of_cdr_type[-1])
            print(index, list_of_cdr_type[-1])


def export_data_into_file(result_out_records, result_out_output_file_name):
    result_out_file = open(result_out_output_file_name, "w")

    for index in range(len(result_out_records)):
        print(str(result_out_records[index].trafic_type) + "\t" +
              str(result_out_records[index].ms_cdr) + "\t" +
              str(result_out_records[index].availability) + "\t" +
              str(result_out_records[index].conformity) + "\t" +
              str(result_out_records[index].dur_conformity) + "\t" +
              str(result_out_records[index].load_condition) + "\t" +
              str(result_out_records[index].operator_id) + "\t" +
              str(result_out_records[index].account_number) + "\t" +
              str(result_out_records[index].region) + "\t" +
              str(result_out_records[index].source_name) + "\t" +
              str(result_out_records[index].io) + "\t" +
              str(result_out_records[index].operators_name) + "\t" +
              str(result_out_records[index].recipient_id) + "\t" +
              str(result_out_records[index].processing_local) + "\t" +
              str(result_out_records[index].description) + "\t" +
              str(result_out_records[index].more_info),
              file=result_out_file)
    result_out_file.close()


# main()

data_in_folder = "ms_ntk_compare_lvv_out"
RESULT_OUT_FILE_NAME_NAME = "result_out_file_lviv.txt"
NTK_FILE_NAME_NAME = "порівняня мс інтраконект тут нтк львів вихід.txt"
MS_FILE_NAME_NAME = "порівняня мс інтраконект тут мс львів вихід.txt"
ERROR_LOG_FILE_NAME = "error_log.txt"
DO_CALLS_REGION = 'DO_CALLS_LVV'
DO_CALLO_REGION = 'DO_CALLO_LVV'

result_out_input_file_name = os.path.join(os.getcwd(), data_in_folder,
                                          RESULT_OUT_FILE_NAME_NAME)
ntk_file_name = os.path.join(os.getcwd(), data_in_folder, NTK_FILE_NAME_NAME)
ms_file_name = os.path.join(os.getcwd(), data_in_folder, MS_FILE_NAME_NAME)
log_file_name = os.path.join(os.getcwd(), data_in_folder, ERROR_LOG_FILE_NAME)
result_out_output_file_name = os.path.join(os.getcwd(), data_in_folder,
                                           "result_out_file_export.txt")

result_out_records = read_result_out_file(result_out_input_file_name)
for record in result_out_records:
    print(record)

ntk_records = read_ntk_file(ntk_file_name)
for record in ntk_records:
    print(record)

ms_records = read_ms_file(ms_file_name)
for record in ms_records:
    print(record)

fill_empty_fields_in_result_out_records(result_out_records)
for record in result_out_records:
    print(record)

check_for_warnings(result_out_records)

export_data_into_file(result_out_records, result_out_output_file_name)
