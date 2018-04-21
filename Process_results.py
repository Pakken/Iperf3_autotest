import yaml 
import matplotlib.pyplot as plt

##with open('results.txt','r') as results:
##    for i in results.readlines():
##        with open(i,'r') as result:
##            data = yaml.load(file,Loader=Loader)
##            for i in data:
##            print(i)

clear_data = []




def main():
    with open('results','r') as results:
        for result in results.readlines():
            with open(result.strip(),'r') as data:
                try:
                    d = data.read().replace('\t',' ').replace('}\n{','}\nUUUFFF\n{').split('UUUFFF') # prepare data
                    for i in d:         # populate clear_data
                        clear_data.append(yaml.load(i))
        ##            for i in clear_data:    # test output 
        ##                print(i['start']['test_start'])
        ##                for j in i['intervals']:
        ##                    print(j['sum']['start'])
        ##                    print(j['sum']['end'])
        ##                    print(j['sum']['bits_per_second'])
        ##                print(i['end']['sum_sent']['start'])
        ##                print(i['end']['sum_sent']['end'])
                except yaml.YAMLError as exc:
                    print(exc)

            for i in clear_data:
                time_ticks = []
                bps_ticks = []
                # create special title
                head_title = ['TEST RESULTS WITH IPERF3 PROGRAM',
                              'TEST INFO :',
                              'test file : ' + result.strip(),
                              #'system info : ' + i['start']['system_info'],
                              'test proto : ' + i['start']['test_start']['protocol'],
                              'num of streams : ' + str(i['start']['test_start']['num_streams']),
                              'reverse mode : ' + str(i['start']['test_start']['reverse'])]
                text = ['SUMMARY INFO :',
                          'Sent :',
                          'duration in sec : ' + str(i['end']['sum_sent']['seconds']),
                          'total bytes : ' + str(i['end']['sum_sent']['bytes']),
                          'average speed : ' + str(i['end']['sum_sent']['bits_per_second']),
                          'Received :',
                          'duration in sec : ' + str(i['end']['sum_received']['seconds']),
                          'total bytes : ' + str(i['end']['sum_received']['bytes']),
                          'average speed : ' + str(i['end']['sum_received']['bits_per_second'])]
                if 'retransmits' in i['end']['sum_sent']:
                    text.append('Count of retransmits : ' + str(i['end']['sum_sent']['retransmits']))
                    
                # create data for plot
                for j in i['intervals']:
                    time_ticks.append(j['sum']['end'])
                    bps_ticks.append(j['sum']['bits_per_second'])

                fig = plt.figure(figsize=(10,15))
                ax = fig.add_subplot(111)
                fig.subplots_adjust(top=0.6)
                ax.set_title('\n'.join(head_title) + '\n'.join(text),fontsize=14)
                ax.set_xlabel('time in sec')
                ax.set_ylabel('bits per second')
                ax.grid()
                ax.bar(time_ticks,
                        bps_ticks,
                        5,
                        color = [0.1,0.5,0.5],
                        align = 'center')
                plt.savefig('iperf3_test_{}_{}_{}.pdf'.format(i['start']['timestamp']['time'],
                                                              i['start']['test_start']['num_streams'],
                                                              i['start']['test_start']['reverse']))
        
if __name__ == '__main__':
    main()
