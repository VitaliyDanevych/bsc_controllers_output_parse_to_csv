import re
import commands


def main():
    list_my = []
    cmd = "/opt/ericsson/bin/eac_esi_config -nelist | grep 'APG' | egrep '[B][0-9]' | awk '{print $1}'"
    output = commands.getoutput(cmd)
    bsc_list = output.split('\n')  # production code##print('bsc_list', bsc_list)

    cmd1 = "'SAAEP:SAE=ALL;'"
    funcs_dict1 = {'Q-ty_of_Cell': '298',
                   'Q-ty_of_TRX': '1153'}

    cmd2 = "'exemp:rp=all,em=all;'"
    funcs_dict2 = {'Q-ty_of_TRH': 'RHTRH',
                   'Q-ty_of_PCU': 'RTGPHDV',
                   'Q-ty_of_AGW': 'RTIPAGW',
                   'Q-ty_of_PGW': 'RTIPPGW'}

    cmd3 = "'NTSTP:SNT=all;'"
    funcs_dict3 = {'Q-ty_of_TRH_board_RPG3': 'RHSNT-',
                   'Q-ty_of_TRH_board_GARP2': 'RHSNT34-',
                   'Q-ty_of_PCU_board_RPP_divided_by_2': 'RTSNT-',
                   'Q-ty_of_PCU_board_GARP2': 'RTSNT34-'}

    cmd4 = "'raclp;'"
    funcs_dict4 = {'Q-ty_of_Licence_PCU': 'EGPRSBPCLIMIT',
                   'Q-ty_of_Licence_AGW': 'AOIP',
                   'Q-ty_of_Licence_PGW': 'ABISIPCL',
                   'Q-ty_of_Licence_RUS_RBS_40': 'MCTRPWR40',
                   'Q-ty_of_Licence_RUS_RBS_60': 'MCTRPWR60',
                   'Q-ty_of_Licence_RUS_RBS_80': 'MCTRPWR80',
                   'Q-ty_of_Licence_RUS_RBS_TRX': 'MCTRTRX'}

    #bsc_list = ['KIEB1']  # only for test
    for bsc in bsc_list:

        ## "'SAAEP:SAE=ALL;'"  "--Q-ty_of_Cell--" and ## "--Q-ty_of_TRX--"
        cmd1_1 = 'cfi -N NE=%s -1 %s' % (bsc, cmd1)
        #print('cmd1_1', cmd1_1)
        output = commands.getoutput(cmd1_1)
        for each_func in funcs_dict1:
            key = funcs_dict1.get(each_func)
            pat = r'^[\s+]*?%s.+?MANUAL\s+(\d+)\s+(\d+).*$' % key
            #print('pat: ', pat)
            pattern = re.compile(pat, re.MULTILINE)
            matched = re.findall(pattern, output)  #<type 'list'>: ['2048', '1371')]
            line = each_func + ',' + bsc + ',' + ",".join([",".join(tup) for tup in matched])
            list_my.append(line)
            #print('line: ', line)  #('line: ', 'KIEB1,Q-ty_of_Cell,298,2048,1371')
        
        ## 'exemp:rp=all,em=all;'   "--Q-ty_of_TRH--" and "--Q-ty_of_PCU--" and "--Q-ty_of_AGW--" and "--Q-ty_of_PGW--"
        cmd2_1 = 'cfi -N NE=%s -1 %s' % (bsc, cmd2)
        #print('cmd2_1', cmd2_1)
        output = commands.getoutput(cmd2_1)
        for each_func in funcs_dict2:
            key = funcs_dict2.get(each_func)
            result = output.count(key)
            line = each_func + ',' + bsc + ',' + str(result)
            list_my.append(line)
            #print('line: ', line)

        ## 'NTSTP:SNT=all;'  "--Q-ty_of_TRH_board_(RPG3)--" and "--Q-ty_of_TRH_board_(GARP2)--" and "--Q-ty_of_PCU_board_(RPP)_(divided_by_2)--" and "--Q-ty_of_PCU_board_(GARP2)--"
        cmd3_1 = 'cfi -N NE=%s -1 %s' % (bsc, cmd3)
        #print('cmd3_1', cmd3_1)
        output = commands.getoutput(cmd3_1)
        for each_func in funcs_dict3:
            key = funcs_dict3.get(each_func)
            result = output.count(key)
            if each_func == 'Q-ty_of_PCU_board_RPP_divided_by_2':
                result = "%2g" % float(result/2)
            line = each_func + ',' + bsc + ',' + str(result)
            list_my.append(line)
            #print('line: ', line)

        ## 'raclp;' 'Q-ty_of_Licence_PCU' & 'Q-ty_of_Licence_AGW' & 'Q-ty_of_Licence_PGW' & 'Q-ty_of_Licence_RUS_RBS_40'& 'Q-ty_of_Licence_RUS_RBS_60'
        ##  'Q-ty_of_Licence_RUS_RBS_80'  & 'Q-ty_of_Licence_RUS_RBS_TRX'
        cmd4_1 = 'cfi -N NE=%s -1 %s' % (bsc, cmd4)
        #print('cmd4_1', cmd4_1)
        output = commands.getoutput(cmd4_1)
        for each_func in funcs_dict4:
            key = funcs_dict4.get(each_func)
            pat = r'^%s.+?(\d+)\s+(\d+)[\s+]*?$' % key
            #print('pat: ', pat)
            pattern = re.compile(pat, re.MULTILINE)
            matched = re.findall(pattern, output)
            line = each_func + ',' + bsc + ',' + ",".join([",".join(tup) for tup in matched])
            list_my.append(line)
            #print('line: ', line)

    with open('/home/fmuser2/scripts/eric_bsc_utiliz/bsc_output2.csv', 'w') as f:
        for each in list_my:
            f.write("%s, %s" % (each, '\n'))


if __name__ == '__main__':
    main()
