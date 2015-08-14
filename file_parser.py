import os
import re
import unicodecsv as csv
import logging
from datetime import datetime
    
def flatfile_maker(infile,outdir='csvs'):
    logging.basicConfig(filename='filemaker.log',level=logging.DEBUG)
    logging.info('{0} :: Logging initiated.'.format(
        datetime.strftime(datetime.today(),'%Y-%m-%d %H:%M')))
    preProcessor(infile,'FullDataFileClean.txt')
    DataFile('FullDataFileClean.txt',outdir)
    
    
class preProcessor(object):

    re_error_1 = r'DB-LIBRARY error:'
    re_error_2 = r"\tSome character\(s\) could not be converted into client's character set.  Unconverted bytes were changed to question marks \('\?'\)"
    re_error_3 = r"Operating-system error:"
    re_error_4 = r"\tSuccess"
    # Get rid of any newline that isn't followed by a valid line start:
    re_badline = r"(?![ABFH12RDE]{1}\|)"

    pat_e1,pat_e2,pat_e3,pat_e4= \
      [re.compile(x) for x in [re_error_1,re_error_2,re_error_3,re_error_4]]

    bad_pat = re.compile(re_badline)

    def chunkfile(self,file_object,chunk_size=1024):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def preprocessfile(self,infilepath,outfilepath='FullDataFileClean.txt'):
        old_file = open(infilepath,'r')
        new_file = open(outfilepath,'w')
        fullfile = old_file.read()
        fullfile = fullfile.replace('\r\n',' ')
        fullfile = fullfile.replace('(return status = 0)','')
        full_list = fullfile.split('\n')
        full_list.pop(-1)
        for num,line in enumerate(full_list):
            for item in [self.pat_e1,self.pat_e2,self.pat_e3,self.pat_e4]:
                if item.match(line):
                    logging.info('Deleting bad line: {0}'.format(item.pattern))
                    full_list[num] = item.sub('',line)

        full_list = [x for x in full_list if x]
        # Make a complete second pass without finding a problem.
        items_remaining = len(full_list) * 2
        while items_remaining > 0:
            enumerated = enumerate(full_list)
            for num,line in enumerated:
                if self.bad_pat.match(line):
                    if num == 0:
                        raise Exception
                    else:
                        logging.info(
                            'Fixing weirdness on line {0}:\n{1}'.format(
                                num,line))
                        full_list[num-1] = full_list[num-1] + full_list.pop(num)
                else:
                    items_remaining -= 1
            logging.info(
                'Completed a loop. Items remaining:'.format(items_remaining))
                
        for line in full_list:
            new_file.write(line + '\n')

        old_file.close()
        new_file.close()
        logging.info('Files closed')

    def __init__(self,filepath,outpath='FullDataFileClean.txt'):
        logging.info('Parsing {0}'.format(filepath))
        self.preprocessfile(filepath)
        logging.info('Parsing complete.')
    
"""
This set of scripts parses the full text of the IRS' political files
into a series of databases.

These are the form types in the full dump:
* "H"    (Header record - mostly useless)
* "1" - 8871 - (Form 8871 - lists organizational stuff like address)
* "D" - Directors and Officers Form - from 8871s
* "R" - Related entities form - from 8817s
* "E" - Election Authority Identification Number
* "2" - Form 8872 header data - begin/end date, etc.
* "A" - Form 8872 Schedule A data (contributions)
* "B" - Form 8872 Schedule B data (expenditures)
* "F" - Footer record (also mostly useless - but includes record count)
"""

class DataFile(object):
    def linereader(self,filepath):
        with open(filepath,'r') as afile:
            for line in afile:
                yield line

    headers_head = ['trans_date','trans_time','file_id','empty_field']
    ones_head = ['form_type','form_id_num','initial_report',
                 'amended_report','final_report',
                 'EIN','organization_name','mailing_address_1',
                 'mailing_address_2','mailing_address_city',
                 'mailing_address_state','mailing_address_zip',
                 'mailing_address_zip_ext','email',
                 'established_date','custodian_name',
                 'custodian_address_1','custodian_address_2',
                 'custodian_address_city','custodian_address_state',
                 'custodian_address_zip','custodian_address_zip_ext',
                 'contact_person_name','contact_address_1',
                 'contact_address_2','contact_address_city',
                 'contact_address_state','contact_address_zip',
                 'contact_address_zip_ext','business_address_1',
                 'business_address_2','business_address_city',
                 'business_address_state','business_address_zip',
                 'business_address_zip_ext','exempt_8872',
                 'exempt_state','exempt_990','purpose',
                 'material_change_date','insert_datetime',
                 'related_entity_bypass','eain_bypass']
    d_head = ['form_id_num','director_id','org_name',
                  'EIN','entity_name','entity_title',
                  'entity_address_1',
                  'entity_address_2','entity_address_city',
                  'entity_address_state','entity_address_zip',
                  'entity_address_zip_ext','empty_field']
    r_head = ['form_id_num','entity_id','org_name',
                  'EIN',
                  'entity_name','entity_relationship',
                  'entity_address_1','entity_address_2',
                  'entity_address_city','entity_address_st',
                  'entity_address_zip','entity_address_zip_ext',
                  'empty_field']
    e_head = ['form_id_num','eain_id',
                  'election_authority_id_num',
                  'state_issued','empty_field']
    twos_head = ['form_type','form_id_num',
                     'period_begin_date',
                     'period_end_date','initial_report',
                     'amended_report','final_report',
                     'change_of_address','organization_name',
                     'EIN','mailing_address_1','mailing_address_2',
                     'mailing_address_city','mailing_address_state',
                     'mailing_address_zip','mailing_address_zip_ext',
                     'email','org_formation_date','custodian_name',
                     'custodian_address_1','custodian_address_2',
                     'custodian_address_city',
                     'custodian_address_state','custodian_address_zip',
                     'custodian_address_zip_ext','contact_person_name',
                     'contact_address_1','contact_address_2',
                     'contact_address_city','contact_address_state',
                     'contact_address_zip','contact_address_zip_ext',
                     'business_address_1','business_address_2',
                     'business_address_city','business_address_state',
                     'business_address_zip','business_address_zip_ext',
                     'qtr_indicator','monthly_rpt_month',
                     'pre_elect_type','pre_or_post_elect_date',
                     'pre_or_post_elect_state',
                     'sched_a_ind','total_sched_a',
                     'sched_b_ind','total_sched_b',
                     'insert_datetime','empty_field']
    a_head = ['form_id_num','sched_a_id',
                      'org_name','EIN',
                      'contributor_name','contributor_address_1',
                      'contributor_address_2',
                      'contributor_address_city',
                      'contributor_address_state',
                      'contributor_address_zip',
                      'contributor_address_zip_ext','contributor_emp',
                      'contribution_amt','contributor_occupation',
                      'agg_contrib_ytd','contribution_date','empty_field']
    b_head = ['form_id_num','sched_b_id',
                      'org_name','EIN',
                      'recipient_name','recipient_address_1',
                      'recipient_address_2','recipient_address_city',
                      'recipient_address_state',
                      'recipient_address_zip',
                      'recipient_address_zip_ext','recipient_employer',
                      'expenditure_amt','recipient_occupation',
                      'expenditure_date','expenditure_purpose','empty_field']
    footer_head = ['transmission_date',
                           'transmission_time','record_count','empty_field']
                     

    def __init__(self,inpath,outdir):
        self.lines = self.linereader(inpath)
        headers = aForm('headers.csv',self.headers_head)
        ones = aForm('8871s.csv',self.ones_head)
        d = aForm('directors.csv',self.d_head)
        r = aForm('related_entities.csv',self.r_head)
        e = aForm('elex_authority.csv',self.e_head)
        twos = aForm('8872s.csv',self.twos_head)
        a = aForm('schedule_a.csv',self.a_head)
        b = aForm('schedule_b.csv',self.b_head)
        f = aForm('footers.csv',self.footer_head)

        type_map = {
            'H':headers,
            '1':ones,
            'D':d,
            'R':r,
            'E':e,
            '2':twos,
            'A':a,
            'B':b,
            'F':f
            }
        for num,row in enumerate(self.lines):
            row = row.strip().strip('\n').split('|')
            if row[0] not in type_map.keys():
                logging.warn('Bad line: {0}\n{1}'.format(num,row))
            else:
                type_map[row[0]].add(row[1:])
            if num % 100000 == 0:
                logging.info('Parsed through line {0}.'.format(str(num)))
        logging.debug('Writing done.')
        for handler in type_map.values():
            handler.close()
        logging.debug('Files closed.')
            
class aForm(object):

    def writer_object(self):
        self.csvfile = open(self.outpath,'w')
        self.writer = csv.writer(self.csvfile,encoding='utf8')
        
    def write_header(self):
        self.writer.writerow(self.header_column)

    def add(self,a_row):
        row_clean = [unicode(i,errors='ignore') for i in a_row]
        coldiff = len(row_clean) - len(self.header_column)
        if coldiff > 0:
            raise Exception, 'Too many items in row:\n{0}'.format(a_row)
        elif coldiff < 0:
            logging.warn('Adding empty values to truncated row:\n{0}'.
                         format(a_row))
            row_clean = row_clean + [u'' for x in xrange(abs(coldiff))]
        else:
            self.writer.writerow(row_clean)
        coldiff = len(row_clean) - len(self.header_column)
        if coldiff != 0:
            logging.warn('Attempt to fix too many/few fields for row failed:\n{0}'.
                         format(a_row))

    def close(self):
        self.csvfile.close()

    def __init__(self,outfile,header,outdir='csvs'):
        self.header_column = header
        self.outpath = os.path.join(outdir,outfile)
        self.writer_object()
        self.write_header()

