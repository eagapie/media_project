This file will contain some of the commands that were ran on the data, and hat are not included in the available scripts. It will also explain some fo the data structure. 



Mongo DB

Indexes to Build on the DB

db.mediacloud_story.ensureIndex({ "media_id":1 })
db.mediacloud_story.ensureIndex({ "story_id":1 })
db.mediacloud_story.ensureIndex( { "companies.name" :1 })
db.mediacloud_mediastories.ensureIndex({ "story_id":1})



How to load the data:

to insert text of stories into database,  from django shell:

python manage.py shell
from mediacloud.models import Media, Story
s = Story()
s.etl("/data/mediacloud/stories_06_07_sec.csv")
s.insertText("/data/mediacloud/extracted_html_20110601_20110701.txt")
s.insertText("/data/mediacloud/extracted_html_20110701_20110801.txt")

to load the basic media data:
mongoimport -d media -c mediacloud_media --type csv --file file_location.media.csv --headerline

to load categories for media:

to add media_id to stories:

to add the companies appearing in the stories:



Data files available:
/data/mediacloud
    # list of companies used in the search
    companies.csv    
    # text of stories for june and july
    extracted_html_20110601_20110701.txt
    extracted_html_20110701_20110801.txt
    # list of all media
    media.csv
    # list of all media with details, with and without header
    media_sets.csv
    media_sets_sec.csv
    # 2mil stories list from jun/jul with details
    stories_06_07_sec.csv
    # 4 mil stories list from jun/jul without details (with/out header)
    stories_id_media_id_2011_06_01_to_2011_09_01.csv
    stories_id_media_id_2011_06_01_to_2011_09_01_sec.csv
/data/wikileaks
    AllCablesOnePerLine.txt  
    MatchedCablesNov28.csv






