#!/usr/bin/python
#encoding=utf8

import sys
import os
import re

def get_functions_from_unwind(elf_file,sort = True):
    unwind_results = os.popen("readelf -u %s" % elf_file)
    functions = {}
    for line in unwind_results.readlines():
        match_result = re.match(r'(0x[0-9a-fA-F]+)\s+<([^>]+)>:.*',line)
        if match_result is not None:
            #print "%s - %s" % (match_result.group(1),match_result.group(2))
            (func_addr, func_name) = match_result.groups()
            if functions.has_key(int(func_addr,16)):
                print >>sys.stderr,"WARING: Same addr[%s] functions found!!!" % func_addr,sys.stderr
            functions[int(func_addr,16)] = func_name
    if sort == True:
        functions = sorted(functions.iteritems())
    #print functions    
    return functions        

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "%s ELF_WITH_ARM_UNWIND ADDR_HEX" % sys.argv[0]
        exit(1);

    try:
        target_addr = int(sys.argv[2],16)
    except:
        print "bad address: %s" % sys.argv[2]
        exit(2)

    unwind_info = get_functions_from_unwind(sys.argv[1]) 

    last_one = [0,"unknown"]
    found = False
    for (addr,name) in unwind_info:
        if target_addr == addr:
            print name 
            found = True
            break
        elif target_addr > addr:
            last_one = (addr, name)
            continue
        elif target_addr < addr:
            print last_one[1]
            found = True
            break
    if not found:
        print "unknown"
            

