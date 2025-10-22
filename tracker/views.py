from django.shortcuts import render,redirect
from .models import CurrentBalance,TrackingHistory
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)
        if not user.exists():
            messages.warning(request,"User not found")
            return redirect('/login/')

        user=authenticate(username=username,password=password)
        if not user :
            messages.warning(request,"Incorrect password")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/')


    return render(request,'login.html')



def register_view(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
 

        user=User.objects.filter(username=username)
        if user.exists():
            messages.warning(request,"User already exists You can login")
            return redirect('/login/')
        
        user=User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()
        messages.success(request,"Account Created")
        return redirect('/login')


    return render(request,'register.html')


def logout_view(request):
    logout(request)
    return redirect('/login')




@login_required(login_url='login_view')
def index(request):
    current_balance, _ =CurrentBalance.objects.get_or_create(user=request.user)
    if request.method=="POST":
        description=request.POST.get('description')
        amount=request.POST.get('amount')
        current_balance, _ =CurrentBalance.objects.get_or_create(user=request.user)
        expense_type='CREDIT'
        if float(amount)<0:
            expense_type='DEBIT'

        if float(amount)==0:
            messages.warning(request, "enter valid amount")
            return redirect('/')

        tracking_history=TrackingHistory.objects.create(
            amount=amount,
            expense_type=expense_type,
            description=description,
            current_balance=current_balance
        )
        current_balance.current_balance+=float(tracking_history.amount)
        current_balance.save()

        return redirect("/")

    income=0
    expense=0

    for tracking_history in TrackingHistory.objects.filter(current_balance=request.user.id):
        if tracking_history.expense_type=='CREDIT':
            income+=tracking_history.amount
        else:
            expense+=tracking_history.amount

    context={'income':income,'expense':expense,'transactions' : TrackingHistory.objects.filter(current_balance=request.user.id),'current_bal':CurrentBalance.objects.get(user=request.user)}
    return render(request, 'index.html',context)

@login_required(login_url='login_view')
def delete_transaction(request,id):
    tracking_history1=TrackingHistory.objects.filter(id=id,current_balance__user=request.user)
    if tracking_history1.exists():
        current_balance, _ =CurrentBalance.objects.get_or_create(user=request.user)
        tracking_history1=tracking_history1[0]

        current_balance.current_balance=current_balance.current_balance-tracking_history1.amount

        current_balance.save()

    tracking_history1.delete()

    return redirect('/')