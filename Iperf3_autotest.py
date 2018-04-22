from subprocess import call
from datetime import datetime

IPERF3_SERV = input('Enter server ip: ')
ENV_NAME = input('Input test environvent name: ')
TIME_TEST_VAR = input('Input time to test: ') # Seconds
BYTES_VAR = 1000000000*float(input('Input Gigabytes to test: '))
BYTES_TEST_VAR = str(BYTES_VAR)# Gigabytes
MAX_FLOW_NUM = 6
TIMESTAMP = str(10)
TESTS = [['iperf3','-c',IPERF3_SERV,'-i',TIMESTAMP,'-t',TIME_TEST_VAR,'-J','-P'],
         ['iperf3','-c',IPERF3_SERV,'-i',TIMESTAMP,'-n',BYTES_TEST_VAR,'-J','-P']]

FILE_NAME = 'iperf3_test_{}_{}_{}'


def main():
    with open('results','a+') as results :
        for i in TESTS:
            res_file_name = FILE_NAME.format(ENV_NAME,datetime.today().strftime('%H:%M_%d:%m:%Y'),i[5])
            results.writelines(res_file_name + '\n')
            with open(res_file_name,'w+') as f:
                for j in range(0,MAX_FLOW_NUM,4):
                    try:
                        i.append(str(j+1))
                        call(i,stdout = f)
                    except:
                        print('Error')
                    try:
                        i.append('-R')
                        call(i,stdout = f)
                        i.remove('-R')
                        i.remove(str(j+1))
                    except:
                        print('Error')

if __name__ == '__main__':
    main()
