#!/usr/bin/python

#the Settings for the uva-manager
import settings
#argparse for cli
from argparse import ArgumentParser
#urllib for webpage handeling
import urllib.request as urlrequest
from urllib.parse import urlencode
#regex for fun
import re
#sys for precheck
import sys
#os for filepaths and so on
import os

def init_parser():
    parser = ArgumentParser() 
    command_parsers = parser.add_subparsers(help="")
    #the parser for the new command
    parser_new = command_parsers.add_parser("new",help="creates a new problem \
            folder")
    parser_new.add_argument("id",help="the id of the problem",type=int)
    parser_new.set_defaults(func=new_problem)
    return parser


def new_problem(args):
    pages_text = lookup_problem(args.id)
    title = parse_title(pages_text)
    (in_file,out_file) = parse_in_out(pages_text)
    env = {"id":args.id,"title":title,"in_file":in_file,"out_file":out_file}
    new_problem_folder(env)


def new_problem_folder(env):
    print("new Problem")
    folder = settings.SRCFOLDER
    folder_title = settings.NAMEINGSTRING.format(id=env['id'],\
            title=env['title'])
    path = folder+folder_title
    #create new problem set folder
    if folder_title not in os.listdir(folder):
        os.mkdir(path)
        in_file = open(path+"/in","w")
        out_file = open(path+"/out","w")
        in_file.write(env['in_file'])
        out_file.write(env['out_file'])
        in_file.close()
        out_file.close()
    pass



def parse_title(text):
    title_pattern = r"<META NAME=\"description\" CONTENT=\"\D*\">\\n<META NAME=\"keywords\""
    title_sub_pattern =r"<META NAME=\"description\" CONTENT=\"|\">\\n<META NAME=\"keywords\""
    matcher = re.compile(title_pattern)
    remover = re.compile(title_sub_pattern)
    title_raw = matcher.findall(text)[0]
    title = remover.sub("",title_raw)
    return str(title)

def parse_input(text):
    pattern_input_text_raw = r"Sample Input.*</PRE>\\n<P>\\n<H2>"
    pattern_input_text= r"Sample Input</A></FONT></H2>\\n<P>\\n<PRE>|</PRE>\\n<P>\\n<H2>"
    input_text_raw_matcher = re.compile(pattern_input_text_raw)
    input_text_matcher = re.compile(pattern_input_text)
    input_text_raw = input_text_raw_matcher.findall(text)[0]
    return input_text_matcher.sub("",input_text_raw).replace("\\n","\n")

def parse_output(text):
    pattern_output_text_raw = r"Sample Output</A></FONT></H2>\\n<P>\\n<PRE>.*</PRE>\\n"
    pattern_output_text= r"Sample Output</A></FONT></H2>\\n<P>\\n<PRE>|</PRE>\\n"
    output_text_raw_matcher = re.compile(pattern_output_text_raw)
    output_text_matcher = re.compile(pattern_output_text)
    output_text_raw = output_text_raw_matcher.findall(text)[0]
    return output_text_matcher.sub("",output_text_raw).replace("\\n","\n")

def parse_in_out(text):
    input = parse_input(text)
    output = parse_output(text)
    return(input,output)


def lookup_problem(id):
    webpage = "http://acm.uva.es/local/online_judge/gotosearch_uva.php"
    text_params = {'p':id,'goto':"Go to"}
    text_data = urlencode(text_params)
    text_binary_data = text_data.encode("utf8")
    text_page = urlrequest.urlopen(webpage,text_binary_data)
    return str(text_page.read())



def main(): 
    parser = init_parser()
    args = parser.parse_args()
    if(len(sys.argv) == 1):
        parser.print_help()
        return
    args.func(args)
    




#start working in main funktion
if __name__ == "__main__":
    main()




