from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, reverse, get_object_or_404
from .forms import BookReviewForm, UserUpdateForm, ProfilisUpdateForm, UserBookCreateForm, UserBookUpdateForm
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from .models import Book, Author, BookInstance, Genre




def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_free = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    favorite_books = Book.objects.annotate(num_copies=Count('bookinstance')).order_by('-num_copies')[:4]
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_free': num_instances_free,
        'num_authors': num_authors,
        'favorite_books': favorite_books,
    }
    return render(request, 'index.html', context=context)

def authors(request):
    paginator =  Paginator(Author.objects.all(),5)
    page_number = request.GET.get('page')
    authors = paginator.get_page(page_number)
    context = {
        'authors': authors
    }

    return render(request, 'authors.html', context=context)

def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)

    return render(request, 'author.html', {'author': single_author})

def book_list(request):
    paginator = Paginator(Book.objects.all(), 5)

    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    context = {'books': books, 'duomenys': 'papildomas turinys'}

    return render(request, 'book_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            if request.user.is_authenticated:
                review.reviewer = request.user
            review.save()
            return redirect('book-detail', pk=book.id)
    else:
        form = BookReviewForm()
    return render(request, 'book_detail.html', {'book': book, 'form': form})



def search(request):
    query = request.GET.get('query')
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query)
                                         | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query))
    return render(request, 'search.html', {'books': search_results, 'query': query})

@login_required
def LoanedBooksByUser(request):
    books = BookInstance.objects.filter(reader=request.user).filter(status__exact='s').order_by('due_back')
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'books': page_obj,
    }
    return render(request, 'user_books.html', context=context)


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')

@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)




class BookByUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = BookInstance
    template_name = 'user_book.html'


class BookByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = BookInstance
    # fields = ['book', 'due_back']
    success_url = "/library/mybooks/"
    template_name = 'user_book_form.html'
    form_class = UserBookCreateForm

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)



class BookByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BookInstance
    #fields = ['due_back',]
    success_url = "/library/mybooks/"
    template_name = 'user_book_form_update.html'
    form_class = UserBookUpdateForm

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.reader


class BookByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = BookInstance
    success_url = "/library/mybooks/"
    template_name = 'user_book_delete.html'

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.reader