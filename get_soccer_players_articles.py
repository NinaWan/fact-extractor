#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import sys


DEBUG = True


def load_wiki_ids(filein):
    """Load soccer player articles Wiki IDs from a file.
    
    :param filein: the path of the file that stores soccer player articles Wiki IDs
    :return: the list of soccer player articles Wiki IDs
    """
    with open(filein) as i:
        # Strip all whitespace characters from the beginning and the end of each line
        # Return the list of soccer player articles Wiki IDs
        return [l.strip() for l in i.readlines()]


def extract_soccer_articles(soccer_ids, corpus_dir, output_dir):
    """Extract soccer player articles out of the Wikipedia corpus.
    
    :param soccer_ids: the list of soccer player articles Wiki IDs
    :param corpus_dir: the directory path of the Widipedia corpus
    :param output_dir: the directory path to store the soccer player articles extracted out of the Wikipedia corpus
    :return: 0
    """
    # Generate the paths, subdirectories and file names in the directory tree of corpus by walking it
    for path, subdirs, files in os.walk(corpus_dir):
        # For each file in corpus_dir, generate its path
        for name in files:
            f = os.path.join(path, name)
            # Get the content of each file in corpus_dir
            with open(f) as i:
                content = ''.join(i.readlines())
            # Search in the content using pattern - id="([^"]+)" to find strings look like id="...", 
            # ... can be replaced by any characters except " and repeat one or more times. e.g. id="112288"
            match = re.search('id="([^"]+)"', content)
            # Get Wiki IDs from the strings that match the above pattern
            # e.g. get 112288 from id="112288"
            current_id = match.group(1)
            if DEBUG:
                # Print the path of each file and the related Wiki IDs
                print "File = [%s] - Wiki ID = [%s]" % (f, current_id)
            # If the current Wiki ID is a soccer player article Wiki ID, 
            # copy the file which holds the related content from the Wikipedia corpus to the output directory
            if current_id in soccer_ids:
                shutil.copy(f, output_dir)
                if DEBUG:
                    print "MATCHED! [%s]" % content
    return 0


if __name__ == "__main__":
    # Check if any argument is missed
    if len(sys.argv) != 4:
        print "Usage: %s <SOCCER_IDS> <CORPUS_DIR> <OUTPUT_DIR>" % __file__
        sys.exit(1)
    else:
        # Load the soccer player articles Wiki IDs
        ids = load_wiki_ids(sys.argv[1])
        # Extract soccer player articles out of the Wikipedia corpus
        extract_soccer_articles(ids, sys.argv[2], sys.argv[3])
