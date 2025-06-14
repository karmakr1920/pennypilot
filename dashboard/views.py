from django.shortcuts import render, get_object_or_404, redirect
from .models import Expense, Category,User,MonthlyBudget,PasswordResetToken
from django.db.models import Sum,Count
from django.contrib import messages
import calendar
from django.utils.timezone import now, timedelta
from datetime import datetime
from django.utils.dateparse import parse_date
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import re
import uuid
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
import re

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect if already logged in
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        consent = request.POST.get('consent')

        # Store form data to repopulate on warning
        form_data = {
            'username': username or '',
            'email': email or '',
            'password1': password1 or '',
            'password2': password2 or '',
            'consent': consent == 'on'  # Checkbox state
        }

        # Basic validation
        if not all([username, email, password1, password2]):
            messages.warning(request, "All fields are required.")
            return render(request, 'dashboard/register.html', {'form_data': form_data})

        if password1 != password2:
            messages.warning(request, "Passwords do not match.")
            return render(request, 'dashboard/register.html', {'form_data': form_data})

        if not consent:
            messages.warning(request, "You must agree to the Terms & Conditions.")
            return render(request, 'dashboard/register.html', {'form_data': form_data})

        # Validate email format
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messages.warning(request, "Invalid email format.")
            return render(request, 'dashboard/register.html', {'form_data': form_data})

        # Check uniqueness
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already taken.")
            return render(request, 'dashboard/register.html', {'form_data': form_data})

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already registered.")
            return render(request, 'dashboard/register.html', {'form_data': form_data})

        try:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password1)
            # Automatically log in the user
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('dashboard')  # Replace 'dashboard' with your desired redirect URL
        except Exception as e:
            messages.warning(request, f"Registration failed: {str(e)}")
            return render(request, 'dashboard/register.html', {'form_data': form_data})

    # GET request: render empty form
    return render(request, 'dashboard/register.html', {'form_data': {}})

@login_required(login_url='/login/')
def update_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        # Store form data to repopulate on warning
        form_data = {
            'username': username or '',
            'email': email or '',
            'first_name': first_name or '',
            'last_name': last_name or '',
        }

        # Basic validation
        if not all([username, email]):
            messages.warning(request, "Username and email are required.")
            return render(request, 'dashboard/update-user.html', {'form_data': form_data})

        # Validate email format
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messages.warning(request, "Invalid email format.")
            return render(request, 'dashboard/update-user.html', {'form_data': form_data})

        # Check uniqueness, excluding current user
        if User.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.warning(request, "Username already taken.")
            return render(request, 'dashboard/update-user.html', {'form_data': form_data})

        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.warning(request, "Email already registered.")
            return render(request, 'dashboard/update-user.html', {'form_data': form_data})

        # Password validation
        if current_password or new_password:
            if not current_password:
                messages.warning(request, "Current password is required to update password.")
                return render(request, 'dashboard/update-user.html', {'form_data': form_data})
            if not new_password:
                messages.warning(request, "New password is required to update password.")
                return render(request, 'dashboard/update-user.html', {'form_data': form_data})
            if not request.user.check_password(current_password):
                messages.warning(request, "Current password is incorrect.")
                return render(request, 'dashboard/update-user.html', {'form_data': form_data})
            if len(new_password) < 8:
                messages.warning(request, "New password must be at least 8 characters long.")
                return render(request, 'dashboard/update-user.html', {'form_data': form_data})

        try:
            # Update user
            user = request.user
            user.username = username
            user.email = email
            user.first_name = first_name or ''
            user.last_name = last_name or ''
            if new_password and current_password:
                user.set_password(new_password)
            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')  # Replace 'dashboard' with your desired redirect URL
        except Exception as e:
            messages.warning(request, f"Update failed: {str(e)}")
            return render(request, 'dashboard/update-user.html', {'form_data': form_data})

    # GET request: render form with current user data
    form_data = {
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    return render(request, 'dashboard/update-user.html', {'form_data': form_data})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect if already logged in

    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        # Store form data for input retention
        form_data = {
            'username_or_email': username_or_email or '',
            'password': password or '',
            'remember_me': remember_me == 'on'
        }

        # Basic validation
        if not all([username_or_email, password]):
            messages.warning(request, "All fields are required.")
            return render(request, 'dashboard/login.html', {'form_data': form_data})

        # Try authenticating with username or email
        user = None
        if '@' in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        else:
            user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            # Handle "Remember me"
            if not remember_me:
                request.session.set_expiry(0)  # Session expires on browser close
            else:
                request.session.set_expiry(1209600)  # 2 weeks
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.warning(request, "Invalid username/email or password.")
            return render(request, 'dashboard/login.html', {'form_data': form_data})

    return render(request, 'dashboard/login.html', {'form_data': {}})

def index(request):
    today = datetime.today()
    current_year = today.year

    year_name = str(current_year)
    context = {
        'year_name': year_name
    }
    return render(request, 'dashboard/index.html',context)

def terms(request):
    today = datetime.today()
    current_year = today.year

    year_name = str(current_year)
    context = {
        'year_name': year_name
    }
    return render(request, 'dashboard/terms.html',context)


@login_required(login_url='/login/')
def expense_list(request):
    user = request.user
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    # Get month name like "June"
    month_name = calendar.month_name[current_month]

    expenses = Expense.objects.filter(user=user,
                                      paid_date__year=current_year,
                                      paid_date__month=current_month).order_by('-paid_date')
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Fetch user's monthly budget for current month/year
    try:
        monthly_budget_obj = MonthlyBudget.objects.get(user=user, year=current_year, month=current_month)
        monthly_budget = monthly_budget_obj.amount
    except MonthlyBudget.DoesNotExist:
        monthly_budget = 0  # Or default value, maybe 0 or None

    remaining_budget = monthly_budget - total_expenses

    # Paginate: 6 expenses per page
    paginator = Paginator(expenses,15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        # 'expenses': expenses,
        'total_expenses': round(total_expenses, 2),
        'monthly_budget': round(monthly_budget, 2),
        'remaining_budget': round(remaining_budget, 2),
        'month_name' : month_name,
        'expenses': page_obj,  # Pass paginated expenses
        'page_obj': page_obj,  # For pagination controls
    }

    return render(request, 'dashboard/expense_list.html', context)

@login_required(login_url='/login/')
def user_dashboard(request):
    user = request.user
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    # Get month name like "June"
    month_name = calendar.month_name[current_month]
    year_name = str(current_year)

    # Filter expenses for the current month
    expenses = Expense.objects.filter(
        user=user,
        paid_date__year=current_year,
        paid_date__month=current_month
    ).order_by('-paid_date')

    # Calculate total expenses
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Fetch category-wise expenses for pie chart
    by_category = (
        expenses
        .values('category__category')  # Adjust field name if your Category model uses 'name' instead of 'category'
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    # Fetch user's monthly budget for current month/year
    try:
        monthly_budget_obj = MonthlyBudget.objects.get(user=user, year=current_year, month=current_month)
        monthly_budget = monthly_budget_obj.amount
    except MonthlyBudget.DoesNotExist:
        monthly_budget = 0  # Or default value, maybe 0 or None

    remaining_budget = monthly_budget - total_expenses

    # Paginate: 6 expenses per page
    paginator = Paginator(expenses,6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'total_expenses': round(total_expenses, 2),
        'monthly_budget': round(monthly_budget, 2),
        'remaining_budget': round(remaining_budget, 2),
        'month_name': month_name,
        'year_name': year_name,
        'expenses': page_obj,
        'page_obj': page_obj,
        'by_category': list(by_category),  # Convert to list for template
        'has_category_data': bool(by_category),  # Explicitly convert to boolean
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='/login/')
def add_expense(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category_id_or_flag = request.POST.get('category')
        new_category_name = request.POST.get('new_category')
        paid_date = request.POST.get('paid_date')
        notes = request.POST.get('notes')

        # Determine category
        if category_id_or_flag == '__new__' and new_category_name:
            category_obj, _ = Category.objects.get_or_create(
                category=new_category_name.strip(),
                user=request.user
            )
        else:
            category_obj = get_object_or_404(Category, id=category_id_or_flag, user=request.user)

        # Create expense
        Expense.objects.create(
            user=request.user,
            title=title.strip(),
            amount=amount,
            category=category_obj,
            paid_date=paid_date,
            notes=notes.strip()
        )

        messages.success(request, "Expense added successfully!")
        return redirect('dashboard')

    # GET request: Show form with user's categories
    categories = Category.objects.filter(user=request.user).order_by('category')
    return render(request, 'dashboard/add_expense.html', {
        'categories': categories
    })


@login_required(login_url='/login/')
def update_expense(request, exp_id):
    expense = get_object_or_404(Expense, pk=exp_id, user=request.user)
    user_categories = Category.objects.filter(user=request.user).order_by('category')

    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category_name = request.POST.get('category')
        new_category_name = request.POST.get('new_category')
        paid_date = request.POST.get('paid_date')
        notes = request.POST.get('notes')

        if category_name == '__new__' and new_category_name:
            category_obj, created = Category.objects.get_or_create(
                category=new_category_name.strip(),
                user=request.user
            )
            # if created:
            #     messages.success(request, f"New category '{new_category_name}' created.")
        else:
            category_obj = Category.objects.filter(
                category=category_name, user=request.user
            ).first()
            if not category_obj:
                category_obj = Category.objects.create(
                    category=category_name.strip(),
                    user=request.user
                )

        expense.title = title
        expense.amount = amount
        expense.category = category_obj
        expense.paid_date = paid_date
        expense.notes = notes
        expense.save()

        messages.success(request, "Expense updated successfully!")
        return redirect('expense_list')

    return render(request, 'dashboard/update_expense.html', {
        'expense': expense,
        'categories': user_categories,
    })


@login_required(login_url='/login/')
def delete_expense(request, exp_id):
    expense = get_object_or_404(Expense, pk=exp_id, user=request.user)
    expense.delete()
    messages.success(request, "Expense deleted successfully!")
    return redirect('dashboard')

@login_required(login_url='/login/')
def set_monthly_budget(request):
    user = request.user
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    # Get month name like "June"
    month_name = calendar.month_name[current_month]

    budget, created = MonthlyBudget.objects.get_or_create(
        user=user,
        year=current_year,
        month=current_month,
        defaults={'amount': 0}
    )

    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = float(amount)
            if amount < 0:
                raise Valuewarning("Budget cannot be negative")
        except Valuewarning:
            messages.warning(request, "Please enter a valid positive number for budget.")
            return redirect('set_monthly_budget')

        budget.amount = amount
        budget.save()
        messages.success(request, f"Monthly budget set to ₹{amount} for {month_name} {current_year}.")
        return redirect('dashboard')

    context = {
        'budget': budget,
        'month': current_month,
        'month_name': month_name,
        'year': current_year,
    }
    return render(request, 'dashboard/set_budget.html', context)


@login_required(login_url='/login/')
def report_view(request):
    user = request.user
    today = now().date()
    current_year = today.year
    year_name = str(current_year)

    filter_type = request.GET.get('filter_type', 'weekly')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Set default filter ranges
    if filter_type == 'monthly':
        start = today - timedelta(days=30)
        end = today
    elif filter_type == 'yearly':
        start = today.replace(month=1, day=1)
        end = today
    elif filter_type == 'custom':
        start = parse_date(start_date) if start_date else today - timedelta(days=7)
        end = parse_date(end_date) if end_date else today
        if not start or not end:
            start = today - timedelta(days=7)
            end = today
    else:  # Default: weekly
        start = today - timedelta(days=7)
        end = today

    # Filter user's expenses in the selected date range
    filtered_expenses = Expense.objects.filter(user=user, paid_date__range=(start, end))

    weekly_total = filtered_expenses.filter(paid_date__gte=today - timedelta(days=7)).aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_total = filtered_expenses.filter(paid_date__gte=today - timedelta(days=30)).aggregate(Sum('amount'))['amount__sum'] or 0

    by_category = (
        filtered_expenses
        .values('category__category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    daily_series = (
        filtered_expenses
        .values('paid_date')
        .annotate(total=Sum('amount'))
        .order_by('paid_date')
    )

    recurring = (
        filtered_expenses
        .values('category__category')
        .annotate(count=Count('id'))
        .filter(count__gte=2)
        .order_by('-count')
    )

    return render(request, 'dashboard/expense_report.html', {
        'weekly_total': weekly_total,
        'monthly_total': monthly_total,
        'by_category': by_category,
        'daily_series': list(daily_series),
        'recurring': recurring,
        'filter_type': filter_type,
        'start_date': start_date,
        'end_date': end_date,
        'year_name': year_name,
        'has_data': filtered_expenses.exists(),
    })

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('home')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate a unique token
            token = uuid.uuid4()
            user.password_reset_token = token
            user.save()
            # Redirect to reset_password view with the token
            return redirect('reset_password', token=token)
        except User.DoesNotExist:
            messages.warning(request, 'Email not found.')
            return render(request, 'dashboard/forgot_password.html')
    return render(request, 'dashboard/forgot_password.html')

def reset_password(request, token=None):
    form_data = {}

    if request.method == 'POST':
        if not token:
            # Handle username_or_email submission to generate token
            username_or_email = request.POST.get('username_or_email')
            if not username_or_email:
                messages.warning(request, "Username or email is required.")
                return render(request, 'dashboard/forgot_password.html', {'form_data': {'username_or_email': username_or_email}})

            try:
                # Look up user by username or email
                user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
                # Delete any existing tokens for this user
                PasswordResetToken.objects.filter(user=user).delete()
                # Generate a new token
                reset_token = PasswordResetToken.objects.create(user=user)
                # Redirect to reset_password with token
                return redirect('reset_password', token=reset_token.token)
            except User.DoesNotExist:
                messages.warning(request, "User with this username or email does not exist.")
                return render(request, 'dashboard/forgot_password.html', {'form_data': {'username_or_email': username_or_email}})

        else:
            # Handle password reset with token
            try:
                reset_token = PasswordResetToken.objects.get(token=token)
                if reset_token.is_expired():
                    messages.warning(request, "Reset token has expired.")
                    reset_token.delete()
                    return redirect('forgot_password')
                user = reset_token.user
            except PasswordResetToken.DoesNotExist:
                messages.warning(request, "Invalid or expired reset token.")
                return redirect('forgot_password')

            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            form_data = {
                'new_password': new_password,
                'confirm_password': confirm_password
            }

            # Basic validation
            if not new_password or not confirm_password:
                messages.warning(request, "All fields are required.")
                return render(request, 'dashboard/forgot_password.html', {'form_data': form_data, 'token': token})

            if new_password != confirm_password:
                messages.warning(request, "Passwords do not match.")
                return render(request, 'dashboard/forgot_password.html', {'form_data': form_data, 'token': token})

            # Additional password validation
            if len(new_password) < 8:
                messages.warning(request, "Password must be at least 8 characters long.")
                return render(request, 'dashboard/forgot_password.html', {'form_data': form_data, 'token': token})

            # Update password
            user.set_password(new_password)
            user.save()
            # Delete the token after use
            PasswordResetToken.objects.filter(token=token).delete()
            messages.success(request, "Password reset successfully. Please log in.")
            return redirect('login')

    return render(request, 'dashboard/forgot_password.html', {'form_data': form_data, 'token': token})