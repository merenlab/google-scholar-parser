A set of Python utilities to parse Google Scholar data

You can run it the following way:

```
python google-scholar-parser --user-ids [INPUT_FILE_PATH|LIST_OF_IDS] \
                             --output-file OUTPUT_FILE_PATH
```

where,

```
  OUTPUT_FILE_PATH
    a TAB-delmited file, contents and structure of which looks
    like this: https://github.com/merenlab/web/blob/master/pubs.txt

  INPUT_FILE_PATH
    a single-column file where each line describes a unique Google
    Scholar user ID.

  LIST_OF_IDS
    an array of text to be split by the character comma (',')
```
