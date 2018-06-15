# 4chan_image_scraper
Scrapes images from 4chan and downloads them to your harddrive.

## Requirements
You would need to have a couple of modules installed in order to run this scraper.

```
pip install scrapy
pip install pymongo
```

The current code is based on MongoDB. You should install it before you run the spider. Although you can fork the code
and throw out the MongoDB part but it prevents you from downloading the same images again and again. There are sure
more effective ways to prevent this but I wanted to get used to MongoDB :-P

* [Download MongoDB Community Edition](https://www.mongodb.com/download-center?#community)
* [Download MongoDB Compass Community Edition](https://www.mongodb.com/download-center?jmp=docs&_ga=2.106487491.1393936996.1528917700-864404028.1518123586#compass)

## Installation
Just download the whole project via git clone:

`git clone https://github.com/ihgalis/4chan_image_scraper.git`

## Setup
Attention here because you need to specify the destination folder where you want your files to be saved. MongoDB only
hosts your meta data and since JSON only supports data up to 16 MB I decided not to place the picture into the MongoDB
(hint: GridFS solves this)

Open the file **settings.py** and change the **IMAGES_STORE** variable to a destination that suites you best:

### Examples
```
IMAGES_STORE = 'C:\\fourchan_img'
IMAGES_STORE = '/tmp/fourchan_img/'
```

## Let the spider crawl
Switch to the folder where you have downloaded the files and execute with scrapy. And execute the following:

```
cd your_install_directory
scrapy runspider spiders\fourchan_image_spider
```
