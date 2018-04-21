from subprocess import call
from datetime import datetime

IPERF3_SERV = '127.0.0.2'
TIME_TEST_VAR = '100'
BYTES_TEST_VAR = '100000000000'# Gigabytes
#PACKETS_TEST_VAR = str(2*10^9) # Gigapackets
MAX_FLOW_NUM = 2
TIMESTAMP = str(10)
TESTS = [['iperf3','-c',IPERF3_SERV,'-i',TIMESTAMP,'-t',TIME_TEST_VAR,'-J','-P'],
         ['iperf3','-c',IPERF3_SERV,'-i',TIMESTAMP,'-n',BYTES_TEST_VAR,'-J','-P']]

FILE_NAME = 'iperf3_test_{}_{}'


def main():
    with open('results','a+') as results :
        for i in TESTS:
            res_file_name = FILE_NAME.format(datetime.today().strftime('%H:%M_%d:%m:%Y'),i[5])
            results.writelines(res_file_name + '\n')
            with open(res_file_name,'w+') as f:
                for j in range(MAX_FLOW_NUM):
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
