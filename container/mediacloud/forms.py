'''
@author eagapie
contains forms used in the mediacloud app
'''
from django import forms
from mediacloud.models import MediaCategory, Companies

class SearchForm(forms.Form):
                
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

    def __str__(self):
        return "%d" % self.category

    category = forms.ChoiceField(choices=[ (o.id, o.category) for o in MediaCategory.objects.all()])
    company  = forms.ChoiceField(choices=[ (o.id, o.name) for o in Companies.objects.all()])
#ToDo use this is want ot narrow the queries over the stories
#    includeCompany = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No','No')], widget=forms.RadioSelect())
