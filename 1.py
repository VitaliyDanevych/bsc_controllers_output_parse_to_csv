#!/usr/bin/python2.7
#  #!/usr/bin/env python
#Программа для Олега Короленко по выполнению команд на контроллеры BSC, парсинге аутпута и записи результата в файл.
__AUTHOR__='Danevych V.'
__COPYRIGHT__='Danevych V. 2017 Kiev, Ukraine'
#vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os
import sys
import commands
import re
#import subprocess as sub

def get_output_parce(name,cmd,bsc): #name,output):
    (status, output) = commands.getstatusoutput(cmd)
    result = "%s, %s, %s" % (bsc, name, output)
    if (name == 'Q-ty_of_Cell') or (name == 'Q-ty_of_TRX'):
        matched = re.search(r'^.*MANUAL\s+(\d+)\s+(\d+).*', output)
        if matched:
            matched = name + ',' + bsc + ',' + matched.group(1) + ',' + matched.group(2)
        else:
            matched = name + ',' + bsc + ',' + 'NULL' + ',' + 'NULL'
        list_my.append(matched)
        print(name + ' cmd_output =' + output)
        print(matched)

    if (name == 'Q-ty_of_TRH') or (name == 'Q-ty_of_TRH_board_RPG3') or (name == 'Q-ty_of_TRH_board_GARP2') or (name == 'Q-ty_of_PCU') or  (name == 'Q-ty_of_AGW')\
        or (name == 'Q-ty_of_PCU_board_GARP2') or (name == 'Q-ty_of_PGW'):
        matched = re.search(r'^(\d+).*$', output)
        if matched:
            matched = name + ',' + bsc + ',' + matched.group(1)
        else:
            matched = name + ',' + bsc + ',' + 'NULL'
        list_my.append(matched)
        print(name + ' cmd_output =' + output)
        print(matched)

    if (name == 'Q-ty_of_Licence_AGW') or (name == 'Q-ty_of_Licence_PCU') or (name == 'Q-ty_of_Licence_PGW') or (name == 'Q-ty_of_Licence_RUS_RBS_40')\
        or (name == 'Q-ty_of_Licence_RUS_RBS_60') or (name == 'Q-ty_of_Licence_RUS_RBS_80') or (name == 'Q-ty_of_Licence_RUS_RBS_TRX'):
        matched = re.search(r'^.*\s+(\d+)\s+(\d+).*$', output)
        if matched:
            matched = name + ',' + bsc + ',' + matched.group(1) + ',' + matched.group(2)
        else:
            matched = name + ',' + bsc + ',' + 'NULL' + ',' + 'NULL'
        list_my.append(matched)
        print(name + ' cmd_output =' + output)
        print(matched)

    if (name == 'Q-ty_of_PCU_board_RPP_divided_by_2'):
        matched = re.search(r'^(\d+).*$', output)
        if matched:
            if matched.group(1).isdigit():
                x = float(matched.group(1)) / 2
                x = "%2g" % (x)
            matched = name + ',' + bsc + ',' + str(x)
        else:
            matched = name + ',' + bsc + ',' + 'NULL'
        list_my.append(matched)
        print(name + ' cmd_output =' + output)
        print(matched)

def main():
    global list_my
    list_my = []
    f = open('/home/vdanevyc/scripts/bsc_controllers_output_to_csv/bsc_output.csv','w')
    cmd = '/opt/ericsson/bin/eac_esi_config -nelist | grep "APG" | egrep "[B][0-9]" | awk \'{print $1}\''
    (status, output) = commands.getstatusoutput(cmd)
    bsc_list = output.split('\n') # production code
    #bsc_list = ['VNIB1','KIEB5'] # only for test
    for bsc in bsc_list:
        #print(bsc)
        ## "--Q-ty_of_Cell--"
        name = 'Q-ty_of_Cell'
        cmd = "cfi -N NE=%s -1 'SAAEP:SAE=298;' |  egrep ' 298 '" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_TRX--"
        name = 'Q-ty_of_TRX'
        cmd = "cfi -N NE=%s -1 'SAAEP:SAE=1153;|' | egrep '1153 '" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_TRH--"
        name = 'Q-ty_of_TRH'
        cmd = "cfi -N NE=%s -1 'exemp:rp=all,em=all;' | egrep -c 'RHTRH'" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_TRH_board_(RPG3)--"
        name = 'Q-ty_of_TRH_board_RPG3'
        cmd = "cfi -N NE=%s -1 'NTSTP:SNT=all;' | egrep -c 'RHSNT-'" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_TRH_board_(GARP2)--"
        name = 'Q-ty_of_TRH_board_GARP2'
        cmd = "cfi -N NE=%s -1 'NTSTP:SNT=all;' | egrep -c 'RHSNT34-'" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_PCU--"
        name = 'Q-ty_of_PCU'
        cmd = "cfi -N NE=%s -1 'exemp:rp=all,em=all;' | egrep -c 'RTGPHDV'" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_PCU_board_(RPP)_(divided_by_2)--"
        name = 'Q-ty_of_PCU_board_RPP_divided_by_2'
        cmd = "cfi -N NE=%s -1 'NTSTP:SNT=all;' | egrep -c 'RTSNT-'" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_PCU_board_(GARP2)--"
        name = 'Q-ty_of_PCU_board_GARP2'
        cmd = "cfi -N NE=%s -1 'NTSTP:SNT=all;' | egrep -c 'RTSNT34-'" % bsc
        get_output_parce(name,cmd,bsc)

         ## "--Q-ty_of_Licence_PCU--"
        name = 'Q-ty_of_Licence_PCU'
        cmd = "cfi -N NE=%s -1 'raclp;|' | egrep 'EGPRSBPCLIMIT'" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_AGW--"
        name = 'Q-ty_of_AGW'
        cmd = "cfi -N NE=%s -1 'exemp:rp=all,em=all;' | egrep -c 'RTIPAGW'" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_Licence_AGW--"
        name = 'Q-ty_of_Licence_AGW'
        cmd = "cfi -N NE=%s -1 'raclp;|' | egrep 'AOIP'" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_PGW--"
        name = 'Q-ty_of_PGW'
        cmd = "cfi -N NE=%s -1 'exemp:rp=all,em=all;' | egrep -c 'RTIPPGW'" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_Licence_PGW--"
        name = 'Q-ty_of_Licence_PGW'
        cmd = "cfi -N NE=%s -1 'raclp;|' | egrep 'ABISIPCL'" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_Licence_RUS_(RBS_40)--""
        name = 'Q-ty_of_Licence_RUS_RBS_40'
        cmd = "cfi -N NE=%s -1 'raclp;|' | egrep 'MCTRPWR40'" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_Licence_RUS_(RBS_60)--""
        name = 'Q-ty_of_Licence_RUS_RBS_60'
        cmd = "cfi -N NE=%s -1 'raclp;|' | egrep 'MCTRPWR60'" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_Licence_RUS_(RBS_80)--""
        name = 'Q-ty_of_Licence_RUS_RBS_80'
        cmd = "cfi -N NE=%s -1 'raclp;|' | egrep 'MCTRPWR80'" % bsc
        get_output_parce(name,cmd,bsc)

        ## "--Q-ty_of_Licence_RUS_(RBS_TRX)--""
        name = 'Q-ty_of_Licence_RUS_RBS_TRX'
        cmd = "cfi -N NE=%s -1 'raclp;|' | egrep 'MCTRTRX'" % bsc
        get_output_parce(name,cmd,bsc)

    for each in list_my:
        #print('each = ' + each)
        f.write("%s, %s" % (each, '\n'))
    f.close()
    exit()

if __name__ == '__main__':
  main()
