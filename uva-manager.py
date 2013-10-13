#!/usr/bin/python


"""
uva-manger new id|name


"""





#the Settings for the uva-manager
import settings

from argparse import ArgumentParser
import urllib.request as urlrequest
from urllib.parse import urlencode
import re

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
    print("NEW PROBLEM {}".format(args.id))
    pages_text = lookup_problem(args.id)
    title = parse_title(pages_text[0])
    (in_file,out_file) = parse_in_out(pages_text[1])
    #print(title)
    #print(in_file)
    print(out_file)

def parse_title(text):
    pattern = r"(<p><font size=\"5\" color=\"red\"><b>|</b></font></p>|\\t\\n\\n|\s)"
    matcher = re.compile(pattern)
    text = matcher.sub("",text)
    return str(text)

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
    title_params = {'p' : id,'info':'info'}
    title_data = urlencode(title_params)
    title_binary_data = title_data.encode("utf8")
    title_page = urlrequest.urlopen(webpage,title_binary_data)
    text_params = {'p':id,'goto':"Go to"}
    text_data = urlencode(text_params)
    text_binary_data = text_data.encode("utf8")
    text_page = urlrequest.urlopen(webpage,text_binary_data)
    return (str(title_page.read()),str(text_page.read()))



def main(): 
    parser = init_parser()
    args = parser.parse_args()
    args.func(args)
    




#start working in main funktion
if __name__ == "__main__":
    main()




