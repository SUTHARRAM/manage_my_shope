from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import csv


from .models import Stock, StockHistory, UserProfile

from .forms import (StockCreateForm, StockSearchForm, StockUpdateForm, 
                    IssueForm, ReceiveForm, ReorderLevelForm, StockHistorySearchForm, 
                    CategoryCreateForm)

def home(request): 
    title = 'Welcome : This is our life of imaginations and feel amazed each time'
    context = {
        'title': title, 
    }

    #return render(request, 'home.html', context)
    return redirect('/list_items')

@login_required
def list_item(request): 
    title = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
       # print(queryset)
    context = {
        "title": title, 
        "queryset": queryset,
    }

    if request.method == 'POST': 
        category =  form['category'].value()
        item = form['item_name'].value()
        """category__name__icontains=form['category'].value()"""
        if(item != None):
            queryset = Stock.objects.filter(item_name__icontains=form['item_name'].value())

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response
        
        context = {
            "title": title, 
            "form": form, 
            "queryset": queryset
        }
        

    #print(context)

    return render(request, "list_item.html", context)

@login_required
def add_items(request): 
    form = StockCreateForm(request.POST or None)

    if form.is_valid(): 
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_items')
    context = {
        "form": form, 
        "title": "Add Item", 
    }

    return render(request, "add_items.html", context)

@login_required
def update_items(request, pk): 
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)

    if request.method == 'POST': 
        form = StockUpdateForm(request.POST, instance=queryset)

        if form.is_valid():
            form.save()
            return redirect('/list_items')
        
    context = {
        'form': form
    }

    return render(request, 'add_items.html', context)
@login_required
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        'title': queryset.item_name,
        'queryset': queryset,
    }
    return render(request, 'stock_detail.html', context)

@login_required
def issue_items(request, pk): 
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid(): 
        instance = form.save(commit=False)
        instance.received_quantity = 0
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, " Issued SCUCCESSFULLY. "+str(instance.quantity)+" "+str(instance.item_name)+"s now left in Store")
        instance.save()

        issue_history = StockHistory(
            id = instance.id, 
            last_updated = instance.last_updated, 
            category_id = instance.category_id, 
            item_name = instance.item_name, 
            quantity = instance.quantity, 
            issue_to = instance.issue_to, 
            issue_by = instance.issue_by, 
            issue_quantity = instance.issue_quantity,
        )
        issue_history.save()
        return redirect('/stock_detail/'+str(instance.id))
    
    context = {
        'title': 'Issue '+str(queryset.item_name), 
        'queryset': queryset,
        'form': form, 
        'username': 'Issue By : '+str(request.user), 
    }
    return render(request, 'add_items.html', context)

@login_required
def receive_items(request, pk): 
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid(): 
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.received_quantity
        instance.save()
        messages.success(request, "Received Successfully. "+str(instance.quantity)+
                            " " + str(instance.item_name)+"s now in Store.")

        receive_history = StockHistory(
            id = instance.id, 
            last_updated = instance.last_updated, 
            category_id = instance.category_id, 
            item_name = instance.item_name, 
            quantity = instance.quantity, 
            received_quantity = instance.received_quantity, 
            received_by = instance.received_by, 
        )
        receive_history.save()
        return redirect('/stock_detail/'+str(instance.id))
    context = {
        'title': 'Received '+ str(queryset.item_name), 
        'instance': queryset, 
        'form': form, 
        'username': 'Received By : '+str(request.user),
    }
    return render(request, 'add_items.html', context)

@login_required
def reorder_level(request, pk): 
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, " Reorder level for "+str(instance.item_name)+ " is updated to "+ str(instance.reorder_level))
        return redirect("/list_items")
    
    context = {
            "instance": queryset, 
            "form": form,
        }
    return render(request, "add_items.html", context)


@login_required
def list_history(request): 
    title = 'LIST OF ITEMS'
    queryset = StockHistory.objects.all()
    context = {
        "title": title, 
        "queryset": queryset, 
    }
    form = StockHistorySearchForm(request.POST or None)
    if request.method == 'POST': 
        category = form['category'].value()
        item_name = form['item_name'].value()
        start_date = form['start_date'].value()
        end_date = form['end_date'].value()
        if(item_name != None and category != None and start_date != None and end_date != None):
            queryset = StockHistory.objects.filter(item_name__icontains=item_name, 
                                                    last_updated__range=[
                                                        start_date, 
                                                        end_date
                                                    ])
        if category != '': 
            queryset = queryset.filter(category_id=category)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(
                ['CATEGORY', 
                 'ITEM NAME', 
                 'QUANTITY', 
                 'ISSUE QUANTITY', 
                 'RECEIVE QUANTITY', 
                 'RECEIVE BY', 
                 'ISSUE BY', 
                 'LAST UPDATE']
            )
            instance = queryset
            for stock in instance: 
                writer.writerow(
                    [stock.category, 
                    stock.item_name, 
                    stock.quantity, 
                    stock.issue_quantity, 
                    stock.received_quantity, 
                    stock.received_by, 
                    stock.issue_by, 
                    stock.last_updated]
                )
            return response
        context = {
        "title": title, 
        "form": form, 
        "queryset": queryset
        }
    return render(request, "list_history.html", context)

def add_category(request): 
    form = CategoryCreateForm(request.POST or None)
    if form.is_valid(): 
        form.save()
        messages.success(request, 'Successfully Created')
        return redirect('/list_items')
    context = {
        "title" : 'Add Category',
        "form": form
    }

    return render(request, 'add_items.html', context)

def temp_view(request): 
    queryset = UserProfile.objects.all(); 
    context = {
        'title': 'List of all registered users', 
        'queryset': queryset
    }
    return render(request, 'temp.html', context)


