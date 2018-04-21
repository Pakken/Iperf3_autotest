import yaml 
import matplotlib

##with open('results.txt','r') as results:
##    for i in results.readlines():
##        with open(i,'r') as result:
##            data = yaml.load(file,Loader=Loader)
##            for i in data:
##            print(i)

clear_data = []




def main():
    with open('iperf3-t','r') as data:
        try:
            d = data.read().replace('\t',' ').replace('}\n{','}\nUUUFFF\n{').split('UUUFFF') # prepare data
            for i in d:         # populate clear_data
                clear_data.append(yaml.load(i))
            for i in clear_data:    # test output 
                print(i['start']['test_start'])
                for j in i['intervals']:
                    print(j['sum']['start'])
                    print(j['sum']['end'])
                    print(j['sum']['bits_per_second'])
                print(i['end']['sum_sent']['start'])
                print(i['end']['sum_sent']['end'])
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':
    main()
