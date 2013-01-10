Listing Classifier
=================

    usage: main.py \[-h\] \[-v\] \[-d\]

    Shopping listing classifier tool. Run in a directory containing listings.txt
    and products.txt. Produces results.txt.

    optional arguments:
      -h, --help        show this help message and exit
      -v, --verbose     display extra information for debugging
      -d, --diagnostic  use classified_listings.txt, which contains listings with
                        correct products.

This reads products from products.txt and listings from listings.txt, and produces results.txt which maps products to the listings that refer to it. There is a deliberate bias towards negative error (that is, not classifying a listing) over positive error (classifying a listing incorrectly).

Some improvements to the algorithm are included but commented out since they take much longer to run.