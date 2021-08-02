'''
TO DO:
BUG: No output if someone enters single commdline ID (FIXED)
BUG: Need to differentiate between single commandline ID and FILE (possibly FIXED, althoug may be better to require .txt format or have different commands)
Error Handling:
    non-existent user id (HANDLED try...except)
    wrong input (HANDLED by ArgParse)... although maybe use new command error?
    input path bad (HANDLED?)
    no input file
    proper format for input file
    no permission for input file (HANDLED try...except)
    input file does not exist
    output path bad (HANDLED try...except with custom error)
    no output file (HANDLED try...except with custom error)
    output file exists (HANDLED try...exceot with custom error)
    no permission for output file (HANDLED try...except)

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

def main(author_ids, output_file):

    #print(args)

    ###Extract args from dictionary
    #user_ids = args['user_ids']
    #output_file = args['output_file']

    '''
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
    '''
    #Produce final .tsv file
    #produce_final_tsv(output_file, dicList)

class FilesNPathsError(Exception):
    pass

#Check input paths and process author IDs
def processInput(arg_dict):
    user_ids = arg_dict['user_ids']
    ###Check input file and path
    ####Is input a file?
    if len(user_ids) < 2:
        head, tail = os.path.split(user_ids[0])
        ####Does input path exist?
        if len(head) > 0:
            if not os.path.exists(user_ids[0]):
                try:
                    raise FilesNPathsError()
                except FilesNPathsError as e:
                    print('FilesNPathsError: Your input path is invalid. Please try again.')
                    sys.exit(1)


        ####Does file exist
        if os.path.isfile(user_ids[0]):

            ####Does user have permission to read?
            if not os.access(user_ids[0], os.R_OK):
                try:
                    raise FilesNPathsError()
                except FilesNPathsError as e:
                    print('FilesNPathsError: You do not have permission to read this file :(')
                    sys.exit(1)

            ####Process file if it exists and user has permission
            print('Processing ' + str(user_ids[0]))
            with open(user_ids[0], 'r') as in_f:
                preIdList = [id.strip() for id in in_f]
            author_ids = [id.replace(',', '') for id in preIdList]

        ####Process single ID if file does not exist
        else:
            print("Input does not appear to be a file. Therefore it will be processed as a single user ID.")
            print('Processing ID:')
            author_ids = [id.replace(',', '') for id in user_ids]
            print(author_ids[0])

    ###Process list of IDs
    else:
        print('You have entered a list of IDs.')
        print('The following ID(s) will be processed:')
        author_ids = [id.replace(',', '') for id in user_ids]
        print(*author_ids, sep='\n')
    return author_ids


#Check output file and path
def checkOutputFile(arg_dict):
    output_file = arg_dict['output_file']
    head, tail = os.path.split(output_file)
    if len(head) > 0:

        ####Does path exist?
        if not os.path.exists(head):
            try:
                raise FilesNPathsError()
            except FilesNPathsError as e:
                print('FilesNPathsError: Your output path is invalid. Please try again.')
                sys.exit(1)

        ####Does user have permissions to write to directory?
        if not os.access(output_file, os.W_OK):
            try:
                raise FilesNPathsError()
            except FilesNPathsError as e:
                print('FilesNPathsError: You do not have permission to write to this directory :(')
                sys.exit(1)

    ####Does File Already Exist?
    if os.path.isfile(output_file):
        try:
            raise FilesNPathsError()
        except:
            print("FilesNPathsError: Let's try not to overwrite existing files")
            sys.exit(1)
    return output_file

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

    user_ids = processInput(arg_dict)
    output_file = checkOutputFile(arg_dict)

    #main(author_ids, output_file)
