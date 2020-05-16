from pathlib import Path
import re
import requests
import logging
import markdown
import sys
from lxml import etree

logging.basicConfig(filename='debug.log', filemode='w')
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

directory_in_str = "."
pathlist = Path(directory_in_str).glob('**/*.md')
headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3'}

for path in pathlist:
    path_in_str = str(path)

    with open(path, 'r', encoding='utf-8') as fh:
        file_contents = fh.read()

        doc = etree.HTML(markdown.markdown(file_contents))

        urls = []
        for link in doc.xpath('//a'):
            #print(link.get('href'))
            urls.append(link.get('href'))

        logger.debug(f"URLs for {path_in_str}: {urls}")

        for url in urls:
            try:
                res = requests.head(url, headers=headers)
                if (res.status_code == 301):
                    logger.debug(f"Received code {res.status_code} for {url} in file {path_in_str}.")
                elif (res.status_code != requests.codes.ok):
                    logger.info(f"Received code {res.status_code} for {url} in file {path_in_str}.")

            except requests.exceptions.MissingSchema:
                logger.debug(f"Invalid url: {url}")
                continue

            except OSError as e:
                logger.info(f"Error occured while requesting headers from {url} in file {path_in_str}: {e}.")
                continue




