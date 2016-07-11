#!/usr/bin/python

import sys
import re
import os

#call graph need sudo apt-get install graphviz
 
function_start_regex = re.compile("^([a-f\d]+)\s+<(.*)>:$")
op_line_regex = re.compile("^\s*([a-f\d]+):\s+[a-f\d]+\s+[^<]*(<([^\+]+)>)*$") 
functions_size = {}
functions_static_call = {} 
class Func:
    def __init__(self,start,end):
        self.start = start
        self.end = end
class CallerFunc:
    def __init__(self,name,addr):
        self.name = name
        self.addr = addr

def main():
    if len(sys.argv) < 2:
        print "not enough args."
        exit(1)
    dis_file_path = sys.argv[1]
    operation = None 
    if len(sys.argv) > 2:
        operation = sys.argv[2]
        #print operation
    
    dis_file = open(dis_file_path)
    total_size = 0
    current_func = ""
    current_func_start_addr = 0x0
    current_addr = 0x0
    for line in dis_file:
        match = function_start_regex.match(line)
        if match is None:
            match = op_line_regex.match(line)
            if match is None:
                continue
            else:
                if current_func == "":
                    current_func = "bootcode"
                    current_func_start_addr = int(match.group(1),16)
                current_addr = int(match.group(1),16)
                if match.group(3) is not None:
                    if functions_static_call.has_key(match.group(3)):
                        functions_static_call[match.group(3)].append(CallerFunc(current_func,current_addr))
                    else:
                        functions_static_call[match.group(3)] = [CallerFunc(current_func,current_addr)] 
        else:
            if current_func == "":
                current_func = match.group(2)
                current_func_start_addr = int(match.group(1),16)
                current_addr = int(match.group(1),16)
                continue
            
            else:
                func_size = current_addr - current_func_start_addr + 4
                #if func_size == 4:
                #    print line
                total_size += func_size
                #print "%s\t%d" % (current_func,func_size)
                functions_size[current_func] = func_size

                current_addr = int(match.group(1),16)
                current_func = match.group(2)
                current_func_start_addr = int(match.group(1),16)
    func_size = current_addr - current_func_start_addr + 4
    functions_size[current_func] = func_size
    total_size += func_size
    #print "%s\t%d" % (current_func,func_size)
    #print "---------------------------"
    #print "total: %d [0x%x]" % (total_size,total_size)
    if operation is None or operation.upper() == "CSV":
        for func_name in functions_size.keys():
            static_called = ""
            if functions_static_call.has_key(func_name):
                static_called = ""
            else:
                static_called = "NoStaticCall"
            print "%s\t%d\t%s" % (func_name, functions_size[func_name],static_called)
            pass 
    if (operation is not None) and operation.upper() == "CALLGRAPH":
        print "gen call graph in current dir..."
        if len(sys.argv) == 4:
            callGraph(sys.argv[3])
        else:
            callGraph();
call_relation_rescusion_list = [];
def getCallRelation(func_name):
    contents = ""
    if func_name is None:
        for callee in functions_static_call.keys():
            caller_string=" "
            for caller in functions_static_call[callee]:
                contents += ('''"%s" -> "%s" '''+"\n") % (caller.name,callee)
        return contents
    if func_name in call_relation_rescusion_list:
        return ""
    else:
        call_relation_rescusion_list.append(func_name)
    if not functions_static_call.has_key(func_name):
        return ""
    
    callers = functions_static_call[func_name]

    for caller in callers:
        contents += getCallRelation(caller.name)
        contents += ('''"%s" -> "%s" '''+"\n") % (caller.name,func_name)
    
    return contents


def callGraph(func_name = None):
    dot_template = '''
digraph G{
    #size="4.4";
    node[shape=box];
    //rankdir=LR;

    //layout=twopi;
    %s
}
''' 
    contents = "" #"main[shape=box];sub[shape=box];main->sub;sub->main" 
    if func_name is not None:
        contents += "\"%s\"[color=blue];\n" % func_name
    contents += getCallRelation(func_name)
        



    output = open("/tmp/func_analyzer_call_graph.dot","w")
    output.write(dot_template % contents)
    output.close()
    gen_res = os.system("dot -Tsvg /tmp/func_analyzer_call_graph.dot > func_analyzer_call_graph.svg") 
    #gen_res = os.system("dot -Tpng /tmp/func_analyzer_call_graph.dot > func_analyzer_call_graph.png") 
    gen_res = os.system("dot -Tpdf /tmp/func_analyzer_call_graph.dot > func_analyzer_call_graph.pdf") 
    #os.system("dot -Tjpg /tmp/func_analyzer_call_graph.dot > func_analyzer_call_graph.jpg")    
    if gen_res == 0:
        print "gen OK."
    else:
        print "gen fail."
if __name__ == "__main__":
    main()
