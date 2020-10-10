s =             '''str(self.index) 
                str(self.trafic_type) + " , " + str(self.ms_cdr) + " , " +
                str(self.availability) + " , " + str(self.conformity) + " , " +
                str(self.dur_conformity) + " , " + str(self.load_condition) +
                " , " + str(self.operator_id) + " , " +
                str(self.account_number) + " , " + str(self.region) +
                " , " + str(self.source_name) + " , " + str(self.io) +
                " , " + str(self.processing_local) + " , " +
                str(self.description) + " , " + str(self.more_info)'''
s = (s.replace('\n', '').replace('+ " , " + ', '').replace('" , " ', '').replace('  ',' ').replace('+', ''))
s = s.replace('self', 'result_in_records[index]')
s = s.split()
s = ' + "\\t" +\n'.join(s)
print(s)
