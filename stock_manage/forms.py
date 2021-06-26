from django import forms
from .models import Stock, StockHistory, Category

class StockCreateForm(forms.ModelForm): 
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity', 'received_quantity', 'received_by', 
                    'issue_quantity', 'issue_by','issue_to', 'phone_number', 'created_by',
                    'reorder_level', 'export_to_CSV']

    def clean_category(self): 
        category = self.cleaned_data.get('category')
        if not category: 
            raise forms.ValidationError('This field is required')
        
        '''for instance in Stock.objects.all():
            if instance.category == category:
                raise forms.ValidationError(str(category) + ' is already created')'''
        return category

    def clean_item_name(self): 
        item_name = self.cleaned_data.get('item_name')
        if not item_name: 
            raise forms.ValidationError('This field is required')
        return item_name

class StockSearchForm(forms.ModelForm): 
    export_to_CSV = forms.BooleanField(required=False)
    class Meta: 
        model = Stock
        fields = ['category', 'item_name', 'export_to_CSV',]

class StockUpdateForm(forms.ModelForm): 
    class Meta: 
        model = Stock
        fields = ['category', 'item_name', 'quantity', 'received_quantity', 'received_by', 
                    'issue_quantity', 'issue_by','issue_to', 'phone_number', 'created_by',
                    'reorder_level', 'export_to_CSV']


class IssueForm(forms.ModelForm): 
    class Meta: 
        model = Stock
        fields = ['issue_quantity', 'issue_to']

class ReceiveForm(forms.ModelForm): 
    class Meta: 
        model = Stock
        fields = ['received_quantity', 'received_by']

class ReorderLevelForm(forms.ModelForm): 
    class Meta: 
        model = Stock
        fields = ['reorder_level']

class StockHistorySearchForm(forms.ModelForm): 
    export_to_CSV = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
  
    start_date.widget.attrs.update({'id': 'datetimeinput'})
    class Meta: 
        model = StockHistory 
        fields = ['category', 'item_name', 'start_date', 'end_date']
    def __init__(self, *args, **kwargs): 
        super(StockHistorySearchForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['class'] = 'datepicker'
        self.fields['end_date'].widget.attrs['class'] = 'datepicker'

class CategoryCreateForm(forms.ModelForm): 
    class Meta: 
        model = Category
        fields = ['name']


       
