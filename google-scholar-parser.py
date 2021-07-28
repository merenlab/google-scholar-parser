'''
TO DO:
BUG: No output if someone enters single commdline ID
Error Handling:
    non-existent user id
    wrong input
    output path bad
    no permission for output file

Rename
Upload properly to GitHub
Update Meren

'''
###Imports
import argparse
import csv
import os
import pathlib
from random import *
import re
from scholarly import scholarly #https://scholarly.readthedocs.io/en/latest/quickstart.html
                                #search-for-an-author-by-the-id-visible-in-the-url-of-an-authors-profile
                                #make adjustments with instructions found below:
                                    #https://github.com/scholarly-python-package/scholarly/issues/297
                                    #Adjustments made in July 16 and 20  versions
                                #July 16 and 20 version trigger error messages with fake_useragent
                                    #Make adjustments with instructions found below
                                        #https://github.com/hellysmile/fake-useragent/pull/110/commits/d8ca49d341829adb1f0efa7a309337bdc1c2b978
import sys
import time
from time import sleep

__author__ = "Daniel Adam Nuccio"
__copyright__ = "X"
__liscense__ = "X"
__maintainer__ = "Daniel Adam Nuccio"
__email__ = "z1741403@students.niu.edu"
__requires__ = ["--user-ids", "--output-file"]
__provides__ = ["author-publication-information.tsv"]
__description__ =("A set of Python utilities to parse Google Scholar data")

def main(args):

    print(args)

    ###Extract args from dictionary
    user_ids = args['user_ids']
    output_file = args['output_file']

    ###Process User IDs
    author_ids = []
    if len(user_ids) < 2:
        possible_file = pathlib.Path(user_ids[0])
        if possible_file.exists():
            print('Processing ' + str(possible_file))
            with open(user_ids[0], 'r') as in_f:
                preIdList = [id.strip() for id in in_f]
            author_ids = [id.replace(',', '') for id in preIdList]
        else:
            print('Processing ID(s)')
            author_ids = [id.replace(',', '') for id in user_ids]
            print(author_ids)
    else:
        print('Processing ID(s)')
        author_ids = [id.replace(',', '') for id in user_ids]
        print(author_ids)


    #Retrieve the author's data, fill-in, and return list of dictionaryies containing author and pub info
    dicList = []
    for a_id in author_ids:
        print('Processing:')
        print(a_id)

        #Process valid IDs while flagging invalid IDs
        try:
            id = scholarly.search_author_id(a_id)
            name = id['name']
            print(name)

            author = scholarly.fill(id) #Fill author by ID
            numPub = len(author['publications'])
            print(name + ' has ' + str(numPub) + ' publications')

            random_intervals = genRandList(numPub) # See genRandList

            dicList = gather_pub_info(author, random_intervals, dicList)

        except AttributeError:
            print('An AttributeError occurred for ' + a_id)
            print('Please check to make sure this ID is correct.')

    #Produce final .tsv file
    #produce_final_tsv(output_file, dicList)

#Generate random intervals for time between accessing publications
#as means to avoid upsetting Goliath
def genRandList(number_of_publications):
    randList = []
    n = 0
    while n < number_of_publications:
        n = n + 1
        ran = randint(30, 150)
        randList.append(ran)
    return randList

#Gather publication info
def gather_pub_info(author, random_intervals, dicList):
    i = 0
    for publication in author['publications']:
        if i < 1: #use for testing purposes
        #if i < len(author['publications']):
            nPub = scholarly.fill(author['publications'][i])
            print(nPub)
            dicList.append(nPub)
            i = i + 1
            print("Printed pub " + str(i))

            t = random_intervals[i]
            print("Sleep for " + str(t) + " seconds")
            time.sleep(t)
    return dicList

#Write publication info to a .tsv file
def produce_final_tsv(output_file, dicList):
    with open(output_file, 'wt') as o_file:
        tsv_writer = csv.writer(o_file, delimiter='\t')
        tsv_writer.writerow(['Title', 'Authors', 'Year', 'Journal', 'Volume', 'Number', 'Pages'])
        for v in dicList:
            title = ''
            auth = ''
            year = ''
            jour = ''
            volu = ''
            numb = ''
            page = ''
            if 'title' in v['bib']:
                title = v['bib']['title']
                print(title)
            else:
                title = 'NA'
            if 'author' in v['bib']:
                auth = v['bib']['author']
            else:
                auth = 'NA'
            if 'pub_year' in v['bib']:
                year = v['bib']['pub_year']
            else:
                year = 'NA'
            if 'journal' in v['bib']:
                jour = v['bib']['journal']
            else:
                jour = 'NA'
            if 'volume' in v['bib']:
                volu = v['bib']['volume']
            else:
                volu = 'NA'
            if 'number' in v['bib']:
                numb = v['bib']['number']
            else:
                numb = 'NA'
            if 'pages' in v['bib']:
                page = v['bib']['pages']
            else:
                page = 'NA'
            tsv_writer.writerow([title, auth, year, jour, volu, numb, page])
#def check_paths(arg_dict):
#    input = arg_dict['user_ids']
#    output= arg['output_file']


if __name__ == "__main__":
    ###Use Argparse to Take In Commandline Arguments
    parser = argparse.ArgumentParser(description = __description__, allow_abbrev= False) #provide description
                                                                                         #disable abbreviated args

    #group = parser.add_mutually_exclusive_group()
    #group.add_argument("--user-ids", nargs = "+", help = "One or more IDs entered via the commandline")
    #group.add_argument("--in-file", help = "File of scholar author IDs entered via the commdline. File should contain one ID per row")
    requiredNamed = parser.add_argument_group('Required Arguments')
    requiredNamed.add_argument('--user-ids', nargs = "+", required=True,
                                help = "One or more IDs entered via the commandline or in a file")
    requiredNamed.add_argument("--output-file", required = True,
                                help = "Output file with publication info in .tsv format")

    args = parser.parse_args()
    arg_dict = args.__dict__

    main(arg_dict)
