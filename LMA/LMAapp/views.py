from django.shortcuts import render,redirect,HttpResponse
from .models import User_details,Book_details,Res_fin_details,Add_Bag,purchase
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import AddBagForm
from datetime import timedelta,date
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404



def index(request):
    return render(request,'index.html')
#@login_required
def home(request): 

    username= request.user.username
    booklist=Book_details.objects.filter(Status='available') 
    return render(request, 'home.html', {'username': username, 'lma': booklist})
  
def signup(request):
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                # Assuming your UserCreationForm maps to the User_details model
                form.save()
                return redirect('login')  # Redirect to the login page on successful registration
        else:
            form = UserCreationForm()

        return render(request, 'signup.html', {'form': form})

    except Exception as e:
        print(f"An error occurred during registration: {e}")
        return render(request, 'signup.html', {'form': form, 'msg': 'Invalid'})

def loginview(request):
     uname=request.POST['username']
     pwd=request.POST['password']
     user=authenticate(request,username=uname,password=pwd)
     if user is not None:
          login(request,user)
          return redirect('home')
     else:
          return render(request,'login.html',{'msg':'Invalid login'})
     
def logoutview(request):
     logout(request)
     return redirect('index')  


@login_required   
def mybag(request):
    if request.user.is_authenticated:
        current_username = request.user
        
        # Retrieve books from Add_Bag where return date is before the current date
        booklist = Add_Bag.objects.filter(UserName=current_username)
        book_title = request.POST.get('book_title')
        
        return render(request, 'mybag.html', {'lma': booklist})
    else:
        # Handle the case when the user is not authenticated
        return redirect('login')  
    
@login_required  
def add_to_bag(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            book_data = request.POST.get('Book_Title')

            # Check if there is a comma in the book_data string
            if ',' in book_data:
                book_title, quantity = book_data.split(',')
            else:
                messages.warning(request, 'Invalid book data format.')
                return redirect('home')

            if Add_Bag.objects.filter(UserName=username, Book_Title=book_title).exists():
                messages.warning(request, 'Book already in your bag.')
            else:
                if int(quantity) > 0:
                    current_date = timezone.now().date()
                    return_date = current_date + timezone.timedelta(days=10)

                    #book = get_object_or_404(Book_details, Book_Title=book_title)
                    books = Book_details.objects.filter(Book_Title=book_title)
                    if books.exists():
                     book = books.first()
                     Add_Bag.objects.create(UserName=username, Book_Title=book_title, AddDate=current_date, Datereturn=return_date)
                     purchase.objects.create(UserName=username, Book_Title=book_title, AddDate=current_date, Datereturn=return_date,status='not return')
                     messages.success(request, 'Book added to your bag successfully.')
                     book.Quantity -= 1
                     book.save()
                else:
                    messages.warning(request, 'Invalid quantity.')

            return redirect('home')
        else:
            return redirect('login')
    else:
        return HttpResponse('Method not allowed') 

@login_required
def return_book(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            book_title = request.POST.get('Book_Title')
            # Check if the book is in the user's bag
            if Add_Bag.objects.filter(UserName=username, Book_Title=book_title).exists():
                # Get the book record from Add_Bag
                book = get_object_or_404(Add_Bag, UserName=username, Book_Title=book_title)
                purchase.objects.update(status='return')
                # Delete the book record from Add_Bag
                book.delete()
                messages.success(request, 'Book returned successfully.')
                # Get the corresponding book details
                book_details_list = Book_details.objects.filter(Book_Title=book_title)
                # Iterate over each book_details and increase the quantity by 1
                for book_details in book_details_list:
                    book_details.Quantity += 1
                    book_details.save()
    return redirect('mybag')
 
@login_required
def resfin(request):
     if request.user.is_authenticated:
        current_date = timezone.now().date()
        # Retrieve books from Add_Bag that are due for return for the current user
        due_books = Add_Bag.objects.filter(UserName=request.user.username, Datereturn__lt=current_date)
        for book in due_books:
            # Calculate the number of days overdue
            days_overdue = (current_date - book.Datereturn.date()).days
            # Calculate the fine (Rs 2 per day overdue)
            fine = max(0, days_overdue) * 2
            # Create a record in Res_fin_details
            Res_fin_details.objects.create(
                UserName=book.UserName,
                Book_Title=book.Book_Title,
                Date_issue=book.AddDate,
                Date_return=book.Datereturn,
                fine=fine,
                status='Not Return' if days_overdue > 0 else 'Returned'
            )
            # Delete the book record from Add_Bag
            book.delete()
        # Retrieve records from Res_fin_details for the current user
        resfin_records = Res_fin_details.objects.filter(UserName=request.user.username)
        return render(request, 'resfin.html', {'lma': resfin_records})
     else:
        # If the user is not authenticated, you may redirect them to a login page or perform other actions
        return redirect('login')



   