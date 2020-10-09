import os
from datetime import datetime


class ResultRecord:
    # місто    3216    так    так    так    cdr_set =3216    1203    3226    32
    #  DA_CALLS_LVV    IA_IN    2
    def __init__(self, index=None, trafic_type=None, ms_cdr=None,
                 availability=None, conformity=None, dur_conformity=None,
                 load_condition=None, operator_id=None, account_number=None,
                 region=None, source_name=None, io=None, processing_local=None,
                 description=None, more_info=None):
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
                " , " + str(self.processing_local) + " , " +
                str(self.description) + " , " + str(self.more_info) + "]")

    def get_list_of_cdrs(self):
        cdr = self.load_condition
        # print(cdr)
        if 'cdr_set=' in cdr or 'cdr_set =' in cdr:
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
        and list with length 2 with value [2, -53] if we need intercity
        traffic special for using in condition "not in [2,-53]"
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
                list_to_return.append([int(cdr),
                                       int(ms_records[index].substr_service_type),
                                       int(ms_records[index].sum_dur)])
        return list_to_return
        pass


def sum_third(in_list):
    summ = 0
    for index in range(len(in_list)):
        summ += in_list[index][2]
    return summ


log_file_name = os.path.join(os.getcwd(), "ms_ntk_compare", "error_log.txt")
ms_file_name = os.path.join(os.getcwd(), "ms_ntk_compare",
                            "порівняння_мс_нтк_вхід_мс.txt")
ntk_file_name = os.path.join(os.getcwd(), "ms_ntk_compare",
                             "порівняння_мс_нтк_вхід_нтк.txt")
result_in_file_name = os.path.join(os.getcwd(), "ms_ntk_compare",
                                   "out_file_just_in_lviv.txt")

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
result_in_records = [None] * size_of_result_in_list
in_result_in_list_index = 0
out_result_in_list_index = 0
while in_result_in_list_index < size_of_result_in_list:
    line_split = result_in_lines[in_result_in_list_index].split("\t")
    if line_split[-1] == '\n':
        line_split.pop()
    # print(line_split)
    if len(line_split) == 13:
        result_in_records[out_result_in_list_index] = ResultRecord(
                                                out_result_in_list_index,
                                                *line_split)
        in_result_in_list_index += 1
        out_result_in_list_index += 1
    else:
        print(f"Error in line from file number {in_ntk_list_index} with value",
              f"{line_split}")
        error_file = open(log_file_name, "a")
        print(f"{datetime.now()} Error in file {result_in_file_name} in line",
              f"from file number {in_result_in_list_index}",
              f"with value {line_split} wait for 14 parameters and got",
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
    # comzal
    if (result_in_records[index].io == 'IA_IN' and
            result_in_records[index].source_name == 'DA_CALLO_LVV'):
        result_in_records[index].availability = '(Комзал)'
        continue
    # vhid ne comzal
    # lets find list of cdr's $result_in_redord[i].load_condition

    if (result_in_records[index].io == 'IA_IN' and
            result_in_records[index].source_name == 'DA_CALLS_LVV'):
        result_in_records[index].get_list_of_cdrs()
        # lets make empty ours lists for accumulate data for all
        # for different cdr's in $result_in_records[index].load_condition
        list_of_ntk_cdrs_data = []
        list_of_ms_cdrs_data = []
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

                print(index, result_in_records[index].list_of_cdrs[cdr_index])
                print(list_of_ms_cdrs_data, sum_third(list_of_ms_cdrs_data))
                print(list_of_ntk_cdrs_data, sum_third(list_of_ntk_cdrs_data))

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

                    # print(list_of_ntk_cdrs_data)
                    # for ms_index in range(len(ms_records)):
                    #     if result_in_records[index].list_of_cdrs[cdr_index]
                    # list_of_ntk_cdrs_data = []
        # print(result_in_records[index].load_condition)
        # print(result_in_records[index].list_of_cdrs)

for record in result_in_records:
    print(record)
