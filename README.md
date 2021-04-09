# Illuminati Map - SoftDes 2021 Spring MidTerm
## Jacob Smilg and Markus Leschly
## Summary

This project features two main components. There is a data collection script, `get_data.py` which can be called from the command line to collect data, and a computational essay, `computational_essay.ipynb`. The essay walks through the meat of the project - analyzing how the how the Wikipedia pages with the most views in the category “American billionaires" are connected. To answer this question, we provided 3 visualizations, which can be seen in the computational essay, as well as on [the GitHub Pages site](https://olincollege.github.io/illuminatimap) for this project. The visualizations are as follows:

* A 3D Kamada-Kawai network chart that shows the links between pages within the category
* A scatterplot of links to a page vs. total page views over the past 60 days
* A treemap showing each page's number of views as the size of a rectangle to emphasize large range in the number page views within the dataset.

## How to use

To run this project, clone this repository to your computer, then install the required packages with

`pip install -r requirements.txt`

If you want to use the data provided, simply run the Jupyter notebook, and it will generate the plots as intended for the project.

### get_data.py

`get_data.py` contains the code for acquiring data from Wikipedia. It uses the [mediawiki module, created by barrust](https://github.com/barrust/mediawiki), which wraps the MediaWiki API. The data is collected using a [generator](https://www.mediawiki.org/wiki/API:Query#Example_6:_Generators), which allows getting different properties (pageviews, links) from a set of several pages in a list or category (American billionaires). After downloading the data, it is formatted into a dictionary with the following structure:
```
{
    'Name of page':
    {
        'linkshere': [
            'linking page title inside category',
            'linking page title outside of category',
            'another linking page title inside category',
        ],
        'pageviews': {  # contains 60 days of data
            'yyyy-mm-dd': 123,
            'yyyy-mm-dd': 987,
        },
        'pageid': 123456,
        'total_views': 12345678,
        'linkshere_within_category': [
            'linking page title inside category',
            'another linking page title inside category',
        ]
    }
}
```

To use the script, you can run it from the command line.

`python get_data.py -h`

will display the instructions for it, which are as follows:

```
usage: get_data.py [-h] [-c CATEGORY] [-r RATE_LIMIT] [-w RATE_LIMIT_WAIT] filename

positional arguments:
  filename              Path to save the obtained data (.pkl) to

optional arguments:
  -h, --help            show this help message and exit
  -c CATEGORY, --category CATEGORY
                        Width of the generated image in pixels (default: American_billionaires)
  -r RATE_LIMIT, --rate-limit RATE_LIMIT
                        Use rate limiting to limit calls to Wikipedia (default: True)
  -w RATE_LIMIT_WAIT, --rate-limit-wait RATE_LIMIT_WAIT
                        The amount of time to wait between requests in seconds (default: 1.0)
```


**DELETE THIS LATER:**
The README provides a short summary of the project.
Where applicable, the README provides instructions for obtaining the necessary packages or libraries needed to run the code.
Where applicable, the README mentions any changes necessary to the code required to successfully run it.
The README provides instructions for obtaining similar or identical data to that used in the project.
The README provides instructions for how to generate plots similar or identical to those shown in the project computational essay.