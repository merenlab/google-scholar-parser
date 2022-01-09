# A parser for Google Scholar

The command line tool `google-scholar-parser` allows users to collect publication information for for one or more authors from [Google Scholar](https://scholar.google.com/). It is developed by Daniel Adam Nuccio, a graduate student at Northern Illinois University, as a side project to help those who may be interested in automated access to the public information stored in Google Scholar. Google Scholar does have the functionality to export TSV files, however, they may truncate the author list for papers that contain many authors.

Essentially, for a given list of Google Scholar user IDs, `google-scholar-parser` returns a TAB-delimited text file that lists key information about their publications, including the list of authors, publication title, journal, etc.

# Installation

To use `google-scholar-parser` you can create a new [conda](https://docs.conda.io/en/latest/miniconda.html) environment with Python 3.9. You can run the following lines to set up a new `google-scholar-parser` environment, and install its dependencies:

```bash
# create a new conda environment with Python 3.9:
conda create -y --name google-scholar-parser python=3.9

# activate the conda environment
conda activate google-scholar-parser

# create a directory on your disk to store the code for
# google-scholar-parser and go into it
mkdir -p ~/github
cd ~/github

# get a copy of the code and go into it
git clone https://github.com/merenlab/google-scholar-parser.git
cd google-scholar-parser

# install all the dependencies
pip install -r requirements.txt
```

Please remember: if you restart your terminal, you will need to run the following commands to activate the  `google-scholar-parser` environment:

```bash
conda activate google-scholar-parser
cd ~/github/google-scholar-parser
```

# Tests

To confirm that `google-scholar-parser` was set up successfully, you can run the following from the command line:

``` bash
python google-scholar-parser --user-ids dqKtzxQAAAAJ \
                             --output-file shaiber-google-scholar.txt \
                             --article-limit-precaution 5
```

If successful, a TAB-delimited flat text file will be produced with five articles authored by Alon Shaiber.

Although `google-scholar-parser` may not always be capable of retrieving information for every field, at minimum it should contain title and author data for each article and a DOI for publications with a Levenshtein score equal to or greater than 0.95.

# Usage

## Basic use

At minimum `google-scholar-parser` requires user input for two command line arguments:

- `--user-ids` : *one or more Google Scholar user ids entered on the command line or a single plain text file with a .txt extension with one user id per line*
- `--output-file`: *the desired name for your output file or the output path for the .txt file produced by `google-scholar-parser`*

For basic use you may run `google-scholar-parser` as shown below:

- `python google-scholar-parser --user-ids USERID1 --output-file OUTPUT.txt`
- `python google-scholar-parser --user-ids USERID1 USERID2 USERID3 --output-file OUTPUT.txt`
- `python google-scholar-parser --user-ids USERIDFILE.txt --output-file OUTPUT.txt`
- `python google-scholar-parser --user-ids USERID1 --output-file OUTPUT/FILE/PATH/OUTPUT.txt`

## Occasional personal use

If you plan to use `google-scholar-parser` occasionally to gather publication information for a very limited number of Google Scholar users with a limited number of publications, you can likely achieve this using any of the 'Basic use' examples above.

However, if you intend to engage in the bulk collection of data for Google Scholar users and their publications, you may wish to check out some of the 'Bulk collection' options below.  

## Bulk collection

`google-scholar-parser` uses the module [scholarly](https://pypi.org/project/scholarly/) and the [CrossRef Rest API](https://github.com/CrossRef/rest-api-doc) to retrieve publication data for Google Scholar IDs. However, bulk collection will cause problems with DOI retrieval via CrossRef Rest API after retrieving about 75-180 DOIs and eventually upset the all-powerful Google which will eventually block you.

If you do not care about DOIs, you can probably get away with 'Basic use' options longer than if you do (essentially DOI collection will be blocked by CrossRef Rest API long before Google blocks you).

### Random Interval Precaution

If you do not care about time, you can utilize `--random-interval-precaution` to put `google-scholar-parser` to sleep for 30s-150s between each attempt to gather data for a publication and then another 30s-150s when retrieving each DOI. Please note though, even for a single id, this can increase the required time to run the program from minutes to hours if that ID is associated with even just a few dozen publications.

You can run `google-scholar-parser` with `--random-interval-precaution` as follows (although be warned, it is not clear how long it will take for the all-knowing Google to catch on):

``` bash
python google-scholar-parser --user-ids USERID1 \
                             --output-file OUTPUT.txt \
                             --random-interval-precaution Yes
```

### Scraper API

However, if you are engaging in very large collections of data and are concerned either about time or that you cannot outrun Google forever, you will need to utilize [Scraper API](https://www.scraperapi.com/).

Initially, Scraper API will generously give you 5000 free API calls. Later, however, this is cut to 1000 per month. Therefore, please note, if you are doing data collection for publications on a large enough scale to need Scraper API or intend to do bulk collections long term, you will likely need a paid account.

In either case, this is how you would run `google-scholar-parser` with Scraper API:

```bash
python google-scholar-parser --user-ids USERID1 \
                             --output-file OUTPUT.txt \
                             --api-key YOURAPIKEY
```

## Advanced options

`google-scholar-parser` only requires that you enter arguments for `--user-ids` and `--output-file` . For larger collections it is recommended that you utilize `--random-interval-precaution` or set up an account with Scraper API. This should be sufficient for successfully running `google-scholar-parser`.

However, depending on your personal preferences and what you are specifically trying to do, there are some more advanced features available.

### Article limit precaution

You have seen this argument before in the 'Tests' section of this document.

Options include **None**, **1**, and **5**.

The default is **None**.

This option was built in largely for testing purposes to ensure `google-scholar-parser` is working without having to wait extended periods for full collections of data for one or more authors.

```bash
python google-scholar-parser --user-ids USERID1 \
                             --output-file OUTPUT.txt \
                             --article-limit-precaution 5
```

### Verbosity

The `--verbosity` argument is intended to allow users (and the developers) to customize how much output concerning the progress of their data collection is printed to the terminal window on their computer and in the resulting output file.

Options include **0**, **1**, and **2**.

- **0** greatly minimizes the amount of output printed in the terminal window, while still allowing for major warning and error messages (as well as a couple less important ones).
- **1** provides the user with regular updates concerning the progress of their data collection. Although not necessarily essential, these can be useful for users who want to easily track the progress of their data collection and can be beneficial for troubleshooting purposes in the event that `google-scholar-parser` gets stuck, fails, etc. (Ultimately a steady flow of time-stamped progress updates can provide more peace of mind than a program that seems to run indefinitely without telling you anything ).
- **2** outputs considerably more information to the terminal window. This is mainly comprised of unparsed publication info that will ultimately end up in your output file, but in a cleaner format. This information may be beneficial for troubleshooting or testing purposes, especially if it appears `google-scholar-parser` is not returning all the data it should, but may ultimately may make output to the terminal window seem more cluttered and harder to follow in most other circumstances. (Yes, there can be too much of a good thing :wink: ). This option also provides additional information (e.g. Levenshtein scores and DOI request status) to the output file which can be used for troubleshooting possible issues with DOI retrieval.

The default is **1** but you can change it as seen below:

``` bash
python google-scholar-parser --user-ids USERID \
                             --output-file OUTPUT.txt \
                             --verbosity 2
```

### Replace File

By default, `google-scholar-parser` does not like to overwrite existing files. However, sometimes due to either bad input, a failed or aborted attempt to run `google-scholar-parser`, a desire to reduce digital clutter, testing purposes, or whatever other reason, you may wish to overwrite an existing file anyway.

To overwrite or replace an existing file, you can use the argument `--replace file` :

```
python google-scholar-parser --user-ids USERID1 \
                             --output-file OUTPUT.txt \
                             --replace-file Yes
```

The default option is **No** .

### Levenshtein-threshold

When you run `google-scholar-parser`, the program will first use [scholarly](https://pypi.org/project/scholarly/) to collect a considerable amount of publication information for the publications of the Google Scholar users whose id(s) you included when entering the `--user-ids` argument.

Google Scholar, however, does not give you DOIs; therefore article titles need to be queried through [CrossRef Rest API](https://github.com/CrossRef/rest-api-doc) to get the DOIs. Yet, when doing this, it is possible that the DOI associated with the title returned by CrossRef Rest API is not a great match for the title you initially queried.

Hence, `google-scholar-parser` uses the Python module [Levenshtein](https://pypi.org/project/Levenshtein/) to compare the title used to query CrossRef Rest API with the title associated with the returned DOI. When doing this, a number between 0 and 1 is produced to indicate the similarity between the two titles. Higher numbers are considered to be better matches. To ensure a high degree of accuracy and minimize false positives, a default of **0.95** is used.

If you wish to change this number, you can do so with the `--levenshtein-threshold` argument:

```
python google-scholar-parser --user-ids USERID1 \
                             --output-file OUTPUT.txt \
                             --levenshtein-threshold 0.5
```

# Full list of arguments

Below is a cheat sheet for all `google-scholar-parser` arguments. Required arguments, by definition are required. Precautionary arguments are intended to help avoid angering the almighty Google. Miscellaneous arguments are intended to customize your user experience and assist in testing and troubleshooting.

| Argument type | Argument | Description |
| :------------ | :------- | :---------- |
| Required Argument | --user-ids | one or more user ids or a plain text file containing user ids, ideally one per line |
| Required Argument | --output-file | the name of your output file or the path and name of your output file |
| Precautionary Argument | --article-limit-precaution | test if google-scholar-parser is working properly by gathering info for only 1 or 5 articles per user id |
| Precautionary Argument | --random-interval-precaution | gather publication info from Google Scholar at random intervals of 30s-150s |
| Precautionary Argument | --api-key | use Scraper API to avoid getting blocked by Google |
| Miscellaneous Argument | --verbosity | customize the amount of output printed to the terminal screen |
| Miscellaneous Argument | --replace-file | overwrite existing files |
| Miscellaneous Argument | --file-type | attempt to process plain text files other than .txt files |
| Miscellaneous Argument | --levenshtein-threshold | adjust level of similarity necessary for a title associated with a doi to be considered a match |

# Troubleshooting

## Start simple

`google-scholar-parser` was extensively tested to ensure the easy collection of data from Google Scholar using Google Scholar ids. We also built in numerous, relatively simple warnings and error messages to flag simple mistakes people may make when using `google-scholar-parser`. These generally include things like entering a non-existent id or file, or entering a file that cannot be processed for other reasons (e.g. it is empty, it is not a plain text file, etc.). If you are experiencing trouble using `google-scholar-parser`, we would recommend you pay close attention to these error messages and make sure your problem is not due to one of these simple errors.

## Investigating more complex problems

If you seem to be experiencing a more complex problem, we would advise leaving `--verbosity` set on **1** or perhaps setting it to **2** and looking to see where `google-scholar-parser` breaks down; we would also advise checking the output file produced by `google-scholar-parser`.

If `google-scholar-parser` returns data, including DOIs, for most of the entered user IDs, but fails to return data for a very limited number of IDs, that may be due to issues specific to those IDs or a temporary issue reaching Google Scholar or connecting with Scraper API.

If `google-scholar-parser` seems to be having problems with only DOIs, that may be an issue with CrossRef Rest API. Please note, if you are not using Scraper API, you will see a high DOI failure rate rather quickly.

## More serious issues with scholarly and Scraper API

### Scholarly

If `google-scholar-parser` is not returning any data for any ids, that may be due to changes in how easily scholarly gathers data from Google Scholar or how easily it connects with Scraper API. If this appears to have happened you may wish to check the [scholarly Git Hub page](https://github.com/scholarly-python-package/scholarly) as scholarly has a very active user community that is quick to point out these types of issues and maintainers who engage with their users when presented with these issues.

### Scraper API

If you are using Scraper API and have reason to believe your Google Scholar queries or DOI queries are not being made through Scraper API (e.g. you have a high DOI failure rate despite using Scraper API, you get blocked by Google, etc.), you may want to check the dashboard of your Scraper API account. Here you should see a line graph with a blue success line and a red failure line. Your number of successes should roughly come out to two successes for every publication and three success for every id.

If you have a high failure rate, this would suggest you have connected to Scraper API properly, but either the user ids are bad or Scraper API is having issues scraping Google Scholar.

If you have no activity on your Scraper API dashboard, this would suggest either you have not set up your API key properly or scholarly and Scraper API have become incompatible (or `google-scholar-parser` and one of these other two tools have become incompatible).
