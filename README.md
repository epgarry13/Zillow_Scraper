This repo scrapes zillow data by entering the desired city and zipcodes in the getNumPages.py file. Default is set to Houston and all Houston area zipcodes. Run the files in this order: getNumPages (loops through all zipcodes and records number of associated pages), getAllLinks (retrieves list of all zipcode links and secondary pages), then AsyncioScraper (scrapes each link and deposits data into csv).

Caveats:

Sometimes AsyncioScraper will get stuck and developer will have to hit ctrl-c to unstuck. This won't stop the program, but it will move on to the next link.
Zillow changes their website frequently and the functions may need to be updated to reflect new HTML/CSS structure.
