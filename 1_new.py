import os
import sys
import re
import commands
#import subprocess as sub

    
def main():
    #global list_my
    list_my = []
    f = open('/home/fmuser2/scripts/eric_bsc_utiliz/bsc_output.csv','w')
    cmd = "/opt/ericsson/bin/eac_esi_config -nelist | grep 'APG' | egrep '[B][0-9]' | awk '{print $1}'"
    #
    (status, output) = commands.getstatusoutput(cmd)
    print('hello')
    bsc_list = output.split('\n') # production code
    print('bsc_list',bsc_list)
    cmd1 = "'SAAEP:SAE=ALL;'"
    funcs_dict1 = {'Q-ty_of_Cell':'298','Q-ty_of_TRX':'1153'}
    
    cmd2 = "'exemp:rp=all,em=all;'"
    funcs_dict2 = {'Q-ty_of_TRH':'RHTRH','Q-ty_of_PCU':'RTGPHDV','Q-ty_of_AGW':'RTIPAGW','Q-ty_of_PGW':'RTIPPGW'}
    
    cmd3 = "'NTSTP:SNT=all;'"
    funcs_dict3 = {'Q-ty_of_TRH_board_RPG3':'RHSNT-','Q-ty_of_TRH_board_GARP2':'RHSNT34-','Q-ty_of_PCU_board_RPP_divided_by_2':'RTSNT-', 'Q-ty_of_PCU_board_GARP2':'RTSNT34-'}
    
    cmd4 = "'raclp;'"
    funcs_dict4 = {'Q-ty_of_Licence_PCU':'EGPRSBPCLIMIT','Q-ty_of_Licence_AGW':'AOIP','Q-ty_of_Licence_PGW':'ABISIPCL','Q-ty_of_Licence_RUS_RBS_40':'MCTRPWR40','Q-ty_of_Licence_RUS_RBS_60':'MCTRPWR60','Q-ty_of_Licence_RUS_RBS_80':'MCTRPWR80','Q-ty_of_Licence_RUS_RBS_TRX':'MCTRTRX'}
    
    #bsc_list = ['VNIB1','KIEB5'] # only for test
    funcs = set()
    #funcs.clear()
    for bsc in bsc_list:
        #print(bsc)
        
        ## "'SAAEP:SAE=ALL;'"  "--Q-ty_of_Cell--" and ## "--Q-ty_of_TRX--"
        cmd1_1 = 'cfi -N NE=%s -1 %s' % (bsc, cmd1)
        print('cmd1_1', cmd1_1)
        (status, output) = commands.getstatusoutput(cmd1_1)
        #result = "%s, %s" % (bsc, output)
        matched = re.search(r'^[\s+]*?(298|1153).+?MANUAL\s+(\d+)\s+(\d+).*$', output)
        if matched:
            if matched.group(1) == '298':
                matched = 'Q-ty_of_Cell' + ',' + bsc + ',' + matched.group(2) + ',' + matched.group(3)
                print(matched)
            elif matched.group(1) == '1153':
                matched = 'Q-ty_of_TRX' + ',' + bsc + ',' + matched.group(2) + ',' + matched.group(3)
                print(matched)
            else:
                matched = 'Q-ty_of_NULL' + ',' + bsc + ',' + matched.group(2) + ',' + matched.group(3)
                print(matched)
            list_my.append(matched)
        
        exit()
        
        ## "'SAAEP:SAE=ALL;'"  "--Q-ty_of_Cell--" and ## "--Q-ty_of_TRX--"
        cmd1_1 = 'cfi -N NE=%s -1 %s' % (bsc, cmd1)
        print('cmd1_1', cmd1_1)
        (status, output) = commands.getstatusoutput(cmd1_1)
        #result = "%s, %s" % (bsc, output)
        matched = re.search(r'^[\s+]*?(298|1153).+?MANUAL\s+(\d+)\s+(\d+).*$', output)
        if matched:
            if matched.group(1) == '298':
                matched = 'Q-ty_of_Cell' + ',' + bsc + ',' + matched.group(2) + ',' + matched.group(3)
                print(matched)
            elif matched.group(1) == '1153':
                matched = 'Q-ty_of_TRX' + ',' + bsc + ',' + matched.group(2) + ',' + matched.group(3)
                print(matched)
            else:
                matched = 'Q-ty_of_NULL' + ',' + bsc + ',' + matched.group(2) + ',' + matched.group(3)
                print(matched)
            list_my.append(matched)
            
        ##'exemp:rp=all,em=all;'   "--Q-ty_of_TRH--" and "--Q-ty_of_PCU--" and "--Q-ty_of_AGW--" and "--Q-ty_of_PGW--"
        cmd2_1 = 'cfi -N NE=%s -1 %s' % (bsc, cmd2)    
        (status, output) = commands.getstatusoutput(cmd2_1)
        for each_f in funcs_list:
            result = output.count(each_f)
            matched = each_f  + ',' + bsc + ',' + str(result)
            list_my.append(matched)
            
        ##'exemp:rp=all,em=all;'   "--Q-ty_of_TRH--" and "--Q-ty_of_PCU--" and "--Q-ty_of_AGW--" and "--Q-ty_of_PGW--"
        cmd3_1 = 'cfi -N NE=%s -1 %s' % (bsc, cmd3)    
        (status, output) = commands.getstatusoutput(cmd3_1)
        for each_f in funcs_list:
            result = output.count(each_f)
            matched = each_f  + ',' + bsc + ',' + str(result)
            list_my.append(matched)
          

        
        ##'NTSTP:SNT=all;'  "--Q-ty_of_TRH_board_(RPG3)--" and "--Q-ty_of_TRH_board_(GARP2)--" and "--Q-ty_of_PCU_board_(RPP)_(divided_by_2)--" and "--Q-ty_of_PCU_board_(GARP2)--"
        
        ## "--Q-ty_of_Licence_PCU--" and "--Q-ty_of_Licence_AGW--" and "--Q-ty_of_Licence_PGW--" and "--Q-ty_of_Licence_RUS_(RBS_40)--"" and "--Q-ty_of_Licence_RUS_(RBS_60)--""
        # and "--Q-ty_of_Licence_RUS_(RBS_80)--"" and "--Q-ty_of_Licence_RUS_(RBS_TRX)--""

"""        
    for each in list_my:
        #print('each = ' + each)
        f.write("%s, %s" % (each, '\n'))
    f.close()    
    exit()
""" 
    
if __name__ == '__main__':
  main()
