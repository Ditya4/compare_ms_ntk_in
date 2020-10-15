import os
from datetime import datetime
"""
в файлі мс_нтк в нас є оператор, рахунок, тип трафіку і сдри а в вибірці з інтраконекту є оператор рахунок і дані
а порівнювати маєм з мсом де є сдр і дані(при чому сумоване по угоді, тобто різні сдри, які сідають на одну угоду
нам не принципово розділяти), тобто потрібно прописати сдри на відповідні угоди з типом трафіку 
далі, в нас будуть на деяких угодах тоді по 2-5 сдрів замість одного, який був раніше
для сумування воно б мало не впливати, але як прописувати потрібна ідея
приклади сдрів з файлу мс_нтк 
cdr_set_out=3233
cdr_set_out in ('3267','3265')
cdr_set_out=3274
cdr_set_out in ('4221','3264','3274', '3265')
в нас в ін_файл_рекордс є ліст із даних сідіарів для кожного запису але як взнати який з них, скоріше за все потрібно  буде
писати даний ліст як ідентифікатор в нтк_рекордс 
"""


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
            
            
# main()

data_in_folder = "ms_ntk_compare_lvv_out"
#result_in_file_name_name = "lviv_in_all_4_12.10.txt"
DO_CALLS_LVV = 'DO_CALLS_LVV'


log_file_name = os.path.join(os.getcwd(), data_in_folder, "error_log.txt")
ms_file_name = os.path.join(os.getcwd(), data_in_folder,
                            "порівняння_мс_нтк_вхід_мс.txt")
ntk_file_name = os.path.join(os.getcwd(), data_in_folder,
                             "порівняння_мс_нтк_вхід_нтк.txt")
result_in_file_name = os.path.join(os.getcwd(), data_in_folder,
                                   result_in_file_name_name)
result_out_file_name = os.path.join(os.getcwd(), data_in_folder,
                                    "result_in_file.txt")


