'''
@author eagapie
this code includes the models that correspond to the mongodb data structure
various functions in Story that have to do with importing data should be removed and placed in a different file
'''
#from mongoengine import *
import re
import datetime
from   django.db                     import models
from   djangotoolbox                 import fields
from   django_mongodb_engine.contrib import MongoDBManager
from   djangotoolbox.fields          import ListField, EmbeddedModelField

#  models here

class MediaStories(models.Model):
    media_id = models.IntegerField(null=True)
    story_id = models.CharField(max_length=255)

    def etl(self, file_name):
        for line in open(file_name):
            line        = line.split(',')
            ms          = MediaStories()
            ms.media_id = line[1].strip()
            ms.story_id = line[0].strip()
            ms.save()

class MediaCategory(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.category

class Companies(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return "%s" % self.name

    def etl(self, file_name):
        for i_line in open(file_name):
            company = Companies()
            company.name = i_line.strip()
            company.save()    

class Media(models.Model):
    #media_id = models.IntegerField(primary_key=True)
    media_id = models.IntegerField(unique=True)
    url      = models.CharField(max_length=255)
    name     = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True)
    objects  = MongoDBManager()
     
    def __str__(self):
        return "%d" % self.media_id

    # this will read the media_sets file and add the media category to the media object
    def insertCategory(self, file_name):
        for line in open(file_name):
            line = line.split(',')

            print line[2]
            self = Media.objects.get(media_id = int(line[2].strip()))
            self.category = line[1]
            self.save()


class Story(models.Model):
    story_id     = models.IntegerField(unique=True)
    media        = models.ForeignKey(Media, null=True)
    url          = models.CharField(max_length=255, null=True)
    guid         = models.CharField(max_length=255, null=True)
    title        = models.CharField(max_length=255, null=True)
    publish_date = models.DateField(null=True)
    collect_date = models.DateField(null=True)
    story_text   = models.TextField(null=True)
    companies    = ListField(EmbeddedModelField('Companies'), null=True)
    objects      = MongoDBManager()
    
    def __str__(self):
        return "%d" % self.story_id

    # loads more information on he stories that are already in the database, adds media ids, date
    # makes use of the media foreign key that already exists in the media table
    # each line contains the relevant info for 
    def etl(self, file_name):
        f_out = open('log.out','w+')
        i = 0
        for i_line in open(file_name):            
            i += 1
            try:
                line = i_line.split(',')

                # reads the media components
                self        = Story.objects.get(story_id = line[0].strip())
                self.media  = Media.objects.get(media_id=line[1].strip())
                self.url    = line[2]
                iself.guid  = line[3]
                self.title  = line[4]
                try:
                    temp = line[5].split(' ')
                    temp = temp[0].split('-')
                    self.publish_date = datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))
                    temp = line[6].split(' ')
                    temp = temp[0].split('-')
                    self.collect_date = datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))
                except ValueError:
                    self.publish_date = None
                    self.publish_date = None
                    f_out.write("date value error:")
                    f_out.write( i_line )
                self.save()
                if i % 100000 == 0:
                    print i
                    i = 0
            except Exception: #Story.DoesNotExist:
                f_out.write( "other exception:" )
                f_out.write( i_line )

    # insert text gets executed first on mediacloud data. It inserts the stories with story ids and other functions will be ran on this data
    # the html file read containts the downloads from mediacloud with story id and story text
    # each story is delimited by "BEGIN STORY:........." and "BEGIN DOWNLOAD TEXT:........." and "END DOWNLOAD TEXT:.........""
    def insertText(self, html_file_add):

       file = open( html_file_add )
       while 1:
           line = file.readline()

           mt = re.search(r"BEGIN STORY:.........", line)
           if mt is not None:
               try:
                    s = Story()
                    s.story_id = int(mt.group()[13:].strip())
               except Story.DoesNotExist:
                   s = None

               if s is not None: 
                   line_down = file.readline()
                   mt_down = re.search(r"BEGIN DOWNLOAD TEXT:.........", line_down)
                   if mt_down is not None:
 
                       htmlStr = ""
                       # read until find another regex
                       while 1:
                           line_html = file.readline()
                           mt_end = re.search(r"END DOWNLOAD TEXT:.........", line_html)
                           if mt_end is not None:
                               break
                           else:
                               htmlStr = htmlStr + line_html
                   s.story_text = htmlStr
                   s.save()
                   print s.story_id

    # this goes through all the stories html and if it encounters the company names in the Companies table/collection it adds that field
    # to run this go to shell and run s = Story(); s.insertCompanyField()
    def insertCompanyField(self):
        stories   = Story.objects.all()
        companies = Companies.objects.all()
        for item_story in stories:
            company_list = []
            for item in companies:
                if item.name.lower() in item_story.story_text.lower():
                    company_obj   = Companies.objects.get(name=item.name.strip())
                    if not company_list:
                        company_list = [company_obj]
                    else:
                        company_list = company_list.append(company_obj)
            # save the company names per story
            item_story.companies = company_list
            item_story.save()


    # this function fills in missing media ids from the additional data that was provided
    # when new ids are discovered we run this function to complete items in the database
    # it checks each story id for a media id and fills it in if it is abailable
    def insertMissingMediaId(sefl):
        stories = Story.objects.raw_query({'media_id' : None}) #get(media__isnull = True)
        print len(stories)
        for story in stories:
            if story.media is not None:
                continue
            else:
                try:
                    media_st    = MediaStories.objects.get(story_id = story.story_id)
                    media       = Media.objects.get(media_id = media_st.media_id)
                    story.media = media
                    story.save()
                    print story.story_id
                except Exception:
                    print "exception for ", story.story_id


  