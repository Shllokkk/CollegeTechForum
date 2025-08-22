from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from datetime import datetime
from Home.models import Querry, Signup, Answers, Rating
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import F, Avg, OuterRef, Subquery, FloatField, Value, Q
from django.db.models.functions import Coalesce
from django.db import IntegrityError
import json
from django.views.decorators.csrf import csrf_exempt

# ---------------- Public Views ---------------- #

def index(request):
    return render(request, 'Login.html')

def LogIn(request):
    return render(request, 'Login.html')

def SignUp(request):
    return render(request, 'SignUp.html')

@csrf_exempt
def SignUpButton(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            password = request.POST.get('password')
            email = request.POST.get('email')
            Year = request.POST.get('Year')
            Branch = request.POST.get('Branch')

            new_user = User.objects.create_user(username=name, password=password)
            new_user.save()

            signup = Signup(name=name, password=password, email=email, Year=Year, Branch=Branch, date=datetime.today()) 
            signup.save()

            return JsonResponse({'success': True, 'message': 'Signup successful'})
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Username already exists. Please choose a different username.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred: ' + str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def LogInButton(request):
    if request.method == "POST":
        username = request.POST.get('input')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['fname'] = user.username
            return JsonResponse({'success': True, 'message': 'Login successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid Credentials'}, status=400)
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

def Search(request):
    search_query = request.GET.get('Search', '')
    EList = Querry.objects.filter(Q(desc__icontains=search_query))
    
    fname = request.session.get('fname', None)
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'

    context = {
        'EList': EList,
        'search_query': search_query,
        'no_results': not EList.exists(),
        'initials': initials
    }
    return render(request, 'Search.html', context)


# ---------------- Protected Views (never_cache + login_required) ---------------- #

@never_cache
@login_required
def Home(request):
    EList = Querry.objects.order_by('-view_count')  
    fname = request.session.get('fname', None)  
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'

    avg_rating_subquery = (
        Rating.objects
        .filter(answer=OuterRef('pk'))
        .values('answer')
        .annotate(avg_rating=Avg('rating_value'))
    )

    leaderboard = (
        Answers.objects
        .annotate(avg_rating=Subquery(avg_rating_subquery.values('avg_rating')))
        .values('user__username', 'user__id')
    .annotate(cumulative_avg=Coalesce(Avg('avg_rating'), 0.0))  
        .order_by('-cumulative_avg')[:5]
    )

    return render(request, 'Home.html', {'EList': EList, 'fname': fname, 'initials': initials, 'leaderboard': leaderboard})

@never_cache
@login_required
def ContactUs(request):
    EList = Querry.objects.order_by('-view_count')  
    fname = request.session.get('fname', None)  

    if fname:
        initials = ''.join([name[0].upper() for name in fname.split()[:2]])  
    else:
        initials = 'NA'
    return render(request, 'ContactUs.html', {'initials': initials})


@never_cache
@login_required
def AskingQuerry(request):
    if request.method == "POST":
        user = request.user
        name = user.username
        email = user.email or "anonymous@example.com"
        desc = request.POST.get('desc')
        Cat = request.POST.get('Cat')
        querry = Querry(name=name, user=user, email=email, desc=desc, Cat=Cat, date=datetime.today())
        querry.save()
        messages.success(request, "Query Posted Successfully!")

    fname = request.session.get('fname', None)  
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    return render(request, 'AskQuery.html', {'initials': initials})


@never_cache
@login_required
def Answer(request, query_id):
    query = Querry.objects.get(pk=query_id)
    fname = request.session.get('fname', None)
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    context = {'query': query, 'initials': initials}
    return render(request, 'Answer.html', context)


@never_cache
@login_required
def Answered(request, query_id):
    if request.method == "POST":
        query = Querry.objects.get(pk=query_id)
        user = request.user

        # Prevent answering own query
        if query.user == user:
            return JsonResponse({"success": False, "message": "❌ You cannot answer your own query!"})

        response = request.POST.get('response')
        answers = Answers(query=query, response=response, user=user)
        answers.save()

        return JsonResponse({"success": True, "message": "✅ Answered Successfully!"})

    return JsonResponse({"success": False, "message": "Invalid request"})


@never_cache
@login_required
def AllAnswers(request, query_id):
    query = Querry.objects.get(pk=query_id)

    if f'query_viewed_{query_id}' not in request.session:
        query.view_count = F('view_count') + 1
        query.save()
        request.session[f'query_viewed_{query_id}'] = True

    answers = Answers.objects.filter(query=query).annotate(
        avg_rating=Coalesce(Avg('ratings__rating_value'), Value(0, output_field=FloatField()))
    ).order_by('-avg_rating')

    fname = request.session.get('fname', None)
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'

    context = {'query': query, 'answers': answers, 'initials': initials}
    return render(request, 'AllAnswer.html', context)


@never_cache
@login_required
def AllQueries(request):
    user = request.user
    EList = Querry.objects.filter(user=user)
    fname = request.session.get('fname', None)
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    return render(request, 'AllQueries.html', {'initials': initials, 'EList': EList})


@never_cache
@login_required
def unanswered_queries(request):
    fname = request.session.get('fname', None)  
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    unanswered_list = Querry.objects.filter(answers__isnull=True)
    return render(request, 'unanswered_queries.html', {'unanswered_list': unanswered_list, 'initials': initials})


@never_cache
@login_required
def Attendance(request):
    EList = Querry.objects.filter(Cat='Attendance')
    fname = request.session.get('fname', None)
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    return render(request, 'Attendance.html', {'EList': EList, 'initials': initials})


@never_cache
@login_required
def Miniproject(request):
    EList = Querry.objects.filter(Cat='Miniproject')
    fname = request.session.get('fname', None)
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    return render(request, 'Miniproject.html', {'EList': EList, 'initials': initials})


@never_cache
@login_required
def Examination(request):
    EList = Querry.objects.filter(Cat='Examination')
    fname = request.session.get('fname', None)
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    return render(request, 'Examination.html', {'EList': EList, 'initials': initials})


@never_cache
@login_required
def Practical_Viva(request):
    EList = Querry.objects.filter(Cat='Practicals/Viva')
    fname = request.session.get('fname', None)
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    return render(request, 'Practicals_Viva.html', {'EList': EList, 'initials': initials})


@never_cache
@login_required
def Events(request):
    EList = Querry.objects.filter(Cat='Events')
    fname = request.session.get('fname', None)
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    return render(request, 'Events.html', {'EList': EList, 'initials': initials})


@never_cache
@login_required
def Administration(request):
    EList = Querry.objects.filter(Cat='Administration')
    fname = request.session.get('fname', None)
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    return render(request, 'Administration.html', {'EList': EList, 'initials': initials})


@never_cache
@login_required
def Others(request):
    EList = Querry.objects.filter(Cat='Others')
    fname = request.session.get('fname', None)
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    return render(request, 'Others.html', {'EList': EList, 'initials': initials})


@never_cache
@login_required
def user_queries(request, username):
    user = get_object_or_404(User, username=username)
    answered_queries = Querry.objects.filter(answers__user=user).distinct()
    fname = request.session.get('fname', None)
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    return render(request, 'User1.html', {'EList': answered_queries, 'user': user, 'initials': initials})

@never_cache
@login_required
def AboutUs(request):
    fname = request.session.get('fname', None)  
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    return render(request, 'AboutUs.html', {'initials': initials})


# ---------------- Misc Views ---------------- #

@login_required
def SubmitRating(request):
    if request.method == "POST":
        data = json.loads(request.body)
        rating_value = data.get('ratingValue')
        answer_id = data.get('answerId')

        try:
            answer_obj = Answers.objects.get(pk=answer_id)
            user = request.user
            rating, created = Rating.objects.get_or_create(answer=answer_obj, rated_by=user)
            rating.rating_value = rating_value
            rating.save()
            return JsonResponse({"success": True})
        except Answers.DoesNotExist:
            return JsonResponse({"success": False, "error": "Answer does not exist."})
        except Exception as e:
            return JsonResponse({"success": False, "error": "An error occurred."})

    return JsonResponse({"success": False, "error": "Invalid request."})


def AboutUs(request):
    fname = request.session.get('fname', None)  
    initials = ''.join([name[0].upper() for name in fname.split()[:2]]) if fname else 'NA'
    return render(request, 'AboutUs.html', {'initials': initials})


def LogOut(request):
    logout(request)
    if 'fname' in request.session:
        del request.session['fname']
    request.session.flush()
    return redirect('LogIn')
