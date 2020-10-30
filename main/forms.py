from django.forms import ModelForm
from .models import Favourite

class FavouriteForm(ModelForm):
    class Meta:
        model = Favourite
        fields = ['source', 'target']