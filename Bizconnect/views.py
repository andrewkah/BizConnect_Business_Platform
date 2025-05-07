# Bizconnect/views.py
from socket import gaierror
from django.forms import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, render, redirect
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from .models import CustomUser, InvestmentFunds, ServiceRequest, BusinessIdeas, Registration, ExpertRegistration, InvestmentDeal, Resource, ConsultationPackage, ScheduledMeeting
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import random
import string
from InternshipPro import settings
from django.views.decorators.http import require_POST

def generate_password(name):
    special_characters = "!@#$%^&*()"
    name_part = name[:4] 
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    special_part = ''.join(random.choices(special_characters, k=2))
    password = name_part + random_part + special_part
    return password


def send_password_email(email, password):
    subject = 'Welcome to Bizconnect'
    message = f'Hello , thank you for registering into Bizconnect. Your password is {password}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    cc = [settings.EMAIL_HOST_USER]
    email = EmailMessage(subject, message, email_from, recipient_list, cc)
    email.send()
    
def logout_view(request):
    try:
        logout(request)
        del request.session["user_id"]
    except KeyError:
        pass    
    return redirect('index')


def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('Password')
        user_exists = (
            CustomUser.objects.filter(email=email).exists() or
            (Registration.objects.filter(email=email).exists() or
            ExpertRegistration.objects.filter(email=email).exists() or
            Investor.objects.filter(email=email).exists())
        )

        if not user_exists:
            messages.add_message(request, messages.ERROR, 'No account found with this email.')
            return render(request, 'login.html')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            return redirect('homepage1')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid email or password. Please try again.')
            return render(request, 'login.html')

    return render(request, 'login.html')


def indexPage(request):
    return render(request, 'index.html')
    
def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'services.html')

def service_detail(request):
    return render(request, 'service_details.html')

def get_startednow(request):
    return render(request, 'get_started.html')

def after_register(request):
    return render(request, 'after_register.html')



##########################   Entrepreneurs   ###############################

def register_entrepreneur(request):
    return render(request, 'entrepreneur/register_entrepreneur.html')
 
@login_required(login_url='login')
def homepage1(request):
    return render(request, 'entrepreneur/homepage1.html')

@login_required(login_url='login')
def business_ideals(request):
    if request.user.is_entrepreneur():
        entrepreneur = get_object_or_404(Registration, user_id=request.session['user_id'])
        ideals = BusinessIdeas.objects.filter(entrepreneur=entrepreneur)
    else:
        ideals = BusinessIdeas.objects.all()
    return render(request, 'entrepreneur/business_ideals.html', {'proposals': ideals,})

@login_required(login_url='login')
def business_ideal_form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        industry = request.POST.get('industry')
        target_market = request.POST.get('market')
        business_model = request.POST.get('business-model')
        projections = request.POST.get('projections')
        goals = request.POST.get('goals')
        
        pitch_deck = request.FILES.get('pitch-deck')
        plan = request.FILES.get('plan')
        video = request.FILES.get('video')
        support = request.FILES.get('support')
        entrepreneur = get_object_or_404(Registration, user_id=request.session['user_id'])

        business_idea = BusinessIdeas(
            title=title,
            description=description,
            industry=industry,
            target_market=target_market,
            business_model=business_model,
            projections=projections,
            goals=goals,
            pitch_deck=pitch_deck,
            plan=plan,
            video=video,
            support=support,
            entrepreneur=entrepreneur,
        )
        
        business_idea.save()
        return redirect('business_ideals')
    
    return render(request, 'entrepreneur/business_ideal_form.html')

@login_required(login_url='login')
def service_requests(request):
    if request.user.is_entrepreneur():
        entrepreneur = get_object_or_404(Registration, user_id=request.session['user_id'])
        completed_requests = ServiceRequest.objects.filter(requester=entrepreneur, status="Completed")
        service_request = ServiceRequest.objects.filter(requester_id=entrepreneur, status='Concluded')
        if service_request.exists():
            replies = ReplyRequest.objects.filter(service_request__in=service_request)
            return render(request, 'entrepreneur/service_request.html', {'completed_requests': completed_requests, 'replies': replies})
    else:
        completed_requests = ServiceRequest.objects.filter(status='Completed')
    return render(request, 'entrepreneur/service_request.html', {
        'completed_requests': completed_requests,
    })

@login_required(login_url='login')
def service_request_form(request):
    return render(request, 'entrepreneur/expert_request_form.html')

@login_required(login_url='login')
def consultation_schedule(request):
    if request.user.is_entrepreneur():
        entrepreneur = get_object_or_404(Registration, user_id=request.session['user_id'])
        approved_meetings = ScheduledMeeting.objects.filter(status='Approved', entrepreneur = entrepreneur)
        denied_meetings = ScheduledMeeting.objects.filter(status='Denied', entrepreneur=entrepreneur)
        context = {'approved_meetings': approved_meetings, 'denied_meetings': denied_meetings}
        return render(request, 'entrepreneur/consultation_schedule.html', context) 
    
    return render(request, 'entrepreneur/consultation_schedule.html')

@login_required(login_url='login')
def investment_deals(request):
    if request.user.is_entrepreneur():
        entrepreneur = get_object_or_404(Registration, user_id=request.session['user_id'])
        investment_deals = InvestmentDeal.objects.filter(entrepreneur=entrepreneur)
    else:
        investment_deals = InvestmentDeal.objects.all()
        # Handling search query
        query = request.GET.get('q')
        if query:
            investment_deals = investment_deals.filter(
                title__icontains=query) | investment_deals.filter(
                industry__icontains=query)  # Adjust as per your fields

    return render(request, 'entrepreneur/investment_deals.html', {'deals': investment_deals,})

@login_required(login_url='login')
def investment_deal_form(request):
    return render(request, 'entrepreneur/investment_deal_form.html')

@login_required(login_url='login')
def create_investment_deal(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        industry = request.POST.get('industry')
        funding_goal = request.POST.get('funding-goal')
        valuation = request.POST.get('valuation')
        terms = request.POST.get('terms')

      
        entrepreneur = get_object_or_404(Registration, user_id=request.session.get('user_id'))

            # Create the investment deal with the fetched entrepreneur
        investment_deal = InvestmentDeal(
                title=title,
                industry=industry,
                funding_goal=funding_goal,
                valuation=valuation,
                terms=terms,
                entrepreneur_id=entrepreneur.id  
            )
        investment_deal.save()
        return redirect('homepage1')

    return redirect('investment_deals')


@login_required(login_url='login')
def create_consultation_package(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        package_type = request.POST.get('industry')
        package_price = request.POST.get('package-price')

        expert = get_object_or_404(ExpertRegistration, user_id=request.session['user_id']) 

        package = ConsultationPackage.objects.create(
            title=title,
            description=description,
            package_type=package_type,
            package_price=package_price,
            expert=expert
        )
        package.save()

        return redirect('homepage1')  # Redirect to expert homepage or another URL
    
    return render(request, 'consultation_package_form')

@login_required(login_url='login')
def consultation_schedule_form(request, request_id):
    completed_request = get_object_or_404(ServiceRequest, pk=request_id, status='Completed')
    expert = get_object_or_404(ExpertRegistration, id=completed_request.assigned_expert.id)
    consultation_packages = ConsultationPackage.objects.filter(expert=expert)
    context = {
        'consultation_packages': consultation_packages,
        'completed_request': completed_request
    }
    return render(request, 'entrepreneur/consultation_schedule_form.html', context )

@login_required(login_url='login')
def schedule_meeting4theent(request, request_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        expert_name = request.POST.get('expert')
        consultation_date = request.POST.get('consultation_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        link = request.POST.get('link')
        package_id = request.POST.get('consultation_package')
        entrepreneur = get_object_or_404(Registration, user_id=request.session.get('user_id'))
        completed_request = get_object_or_404(ServiceRequest, pk=request_id,)

        consultation_package = ConsultationPackage.objects.get(pk=package_id)

        # Save your meeting scheduling logic here, 
        schedule_meeting = ScheduledMeeting.objects.create(
            title=title,
            expert_name=expert_name,
            consultation_date=consultation_date,
            start_time=start_time,
            end_time=end_time,
            link=link,
            consultation_package=consultation_package,
            entrepreneur= entrepreneur,
            service_request=completed_request, 
        )
        schedule_meeting.save()
        completed_request.status = 'Scheduled'
        completed_request.save()
       
        return redirect('homepage1')  
    consultation_packages = ConsultationPackage.objects.all()
    context = {
        'consultation_packages': consultation_packages
    }
    return redirect('consultation_schedule_form', context)




###############################  Investors  #################################

def register_investor(request):
    return render(request, 'investor/register_investor.html')

from .models import Investor

def submit_investor_form(request):
    if request.method == 'POST':
        form_type = request.POST.get('type')

        # Common fields
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        country = request.POST.get('country')
        capital = request.POST.get('capital')
        information = request.POST.get('information')
        investment = request.POST.getlist('investment')
        # Preferences
        preferences = ', '.join(investment)
        # Check if the email is already used
        if CustomUser.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email already in use. Please use a different email.')
            return redirect('register_investors')
        
          # Generate password
        password = generate_password(email)
        try:
            send_password_email(email, password)
        except gaierror:
            return render(request, 'error.html', {'error': 'Failed to send the password via Email. Please make sure your email is correct or have internet connection!'})
            
        user = CustomUser.objects.create_user(email=email, password=password, user_type='investor')
        
        if form_type == 'individual':
            # Individual-specific fields
            surname = request.POST.get('surname')
            firstname = request.POST.get('firstname')
            gender = request.POST.get('gender')
            
            investor = Investor.objects.create(
                user=user,
                type='individual',
                email=email,
                contact=contact,
                country=country,
                capital=capital,
                information=information,
                surname=surname,
                firstname=firstname,
                gender=gender,
                password=make_password(password),
                investment_preferences=preferences,
            )

        elif form_type == 'organization':
            # Organization-specific fields
            company = request.POST.get('company')

            investor = Investor.objects.create(
                user=user,
                type='organization',
                email=email,
                contact=contact,
                country=country,
                capital=capital,
                information=information,
                company=company,
                password=make_password(password),
                investment_preferences=preferences,
            )  
           
        investor.save()    

        return redirect('after_register') 
    return redirect('register_investors') 

@login_required(login_url='login')
def investment_fundings(request):
    if request.user.is_entrepreneur():
        entrepreneur = get_object_or_404(Registration, user_id=request.session['user_id'])
        investment_deals = InvestmentDeal.objects.filter(entrepreneur_id=entrepreneur)
        
        if investment_deals.exists():
            funds = InvestmentFunds.objects.filter(investment_deal__in=investment_deals)
            return render(request, 'investor/investment_fundings.html', {'funds': funds})
        else:
            # No investment deals found
            return render(request, 'investor/investment_fundings.html', {'funds': []})
    elif request.user.is_investor():
        investor = get_object_or_404(Investor, user_id = request.session['user_id'])
        funds = InvestmentFunds.objects.filter(investor=investor)
        return render(request, 'investor/investment_fundings.html', {'funds': funds})


@login_required(login_url='login')
def investment_funding_form(request, deal_id):
    deal = get_object_or_404(InvestmentDeal, id=deal_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        industry = request.POST.get('industry')
        type = request.POST.get('type')
        investment_amount = request.POST.get('investment_amount')
        contact_method = request.POST.get('contact_method')
        notes = request.POST.get('notes')
        supporting_documents = request.FILES.get('supporting_documents')
        investor = get_object_or_404(Investor, user_id=request.session['user_id'])
        
        investment_fund = InvestmentFunds.objects.create(
            title=title,
            industry=industry,
            type=type,
            investment_amount=investment_amount,
            contact_method=contact_method,
            notes=notes,
            supporting_documents=supporting_documents,
            investment_deal=deal,
            investor=investor,
        )
        investment_fund.save()
        deal.status = 'Funded'
        deal.save()
        return redirect('investment_fundings')
    return render(request, 'investor/investment_funding_form.html', {'deal': deal})


@login_required(login_url='login')
def investor_deals(request):
    return render(request, 'investor/investor_deals.html')

@login_required(login_url='login')
def businessidea_detail(request, idea_id):
    entity_type = request.GET.get('type')
    
    if not idea_id or not entity_type:
        return render(request, 'error.html', {'error': 'Missing ID or type parameter.'})
    
    if entity_type == 'idea':
        try:
            idea = get_object_or_404(BusinessIdeas, id=idea_id)
            return render(request, 'investor/businessidea_detail.html', {'idea': idea,})
        except Exception as e:
            return render(request, 'error.html', {'error': f'An unexpected error occurred: {str(e)}'})
    elif entity_type == 'deal':
        try:
            deal = get_object_or_404(InvestmentDeal, id=idea_id)
            return render(request, 'investor/businessidea_detail.html', {'deal': deal,})
        except Exception as e:
            return render(request, 'error.html', {'error': f'An unexpected error occurred: {str(e)}'})
    elif entity_type == 'fund':
        try:
            fund = get_object_or_404(InvestmentFunds, id=idea_id)
            return render(request, 'investor/businessidea_detail.html', {'fund': fund,})
        except Exception as e:
            return render(request, 'error.html', {'error': f'An unexpected error occurred: {str(e)}'})
    else:
        # Handle invalid entity type
        return render(request, 'error.html', {'error': 'Invalid entity type.'})
    
    
    
    
################################   Experts   ################################

def register_expert(request):
    if request.method == 'POST':
        surname = request.POST.get('surname')
        firstname = request.POST.get('firstname')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        district = request.POST.get('district')
        country = request.POST.get('country')
        industries = request.POST.getlist('industry')
        services = request.POST.getlist('service')
        knowledge = ', '.join(industries)
        experience = ', '.join(services)
        achievements = request.POST.get('achievements')
        references = request.POST.get('references')
        
        # Check if the email is already used
        if CustomUser.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email already in use. Please use a different email.')
            return render(request, 'expert/register_expert.html')
        # Generate password
        password = generate_password(firstname) 
        try:
             # Send the password via email
            send_password_email(email, password)
        except gaierror:
            return render(request, 'error.html', {'error': 'Failed to send the password via Email. Please make sure your email is correct or have internet connection!'})
            
        user = CustomUser.objects.create_user(email=email, password=password, user_type='expert')
               
        # Save the data to the ExpertRegistration model
        
        expert = ExpertRegistration(
            user=user,
            surname=surname,
            firstname=firstname,
            gender=gender,
            email=email,
            contact=contact,
            district=district,
            country=country,
            experience=experience,
            knowledge=knowledge,
            achievements=achievements,
            references=references,
            password=make_password(password)
        )
        
        expert.save()
        
        return redirect('after_register')
    
    return render(request, 'expert/register_expert.html')


@login_required(login_url='login')
def resources(request):
    expert = get_object_or_404(ExpertRegistration, user_id=request.session['user_id'])
    resources = Resource.objects.filter(expert=expert)
    return render(request, 'expert/resources.html', {'resources': resources})

@login_required(login_url='login')
def resource_form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        type = request.POST.get('type')
        supporting_documents = request.POST.get('documents')
        expert = get_object_or_404(ExpertRegistration, user_id=request.session['user_id'])
        
        resource = Resource.objects.create(
            expert = expert,
            title = title,
            description = description,
            type = type,
            supporting_documents = supporting_documents,
        )
        resource.save()
        return redirect('resources')
    return render(request, 'expert/resource_form.html')

@login_required(login_url='login')
def assistance_request(request):
    expert = get_object_or_404(ExpertRegistration, user_id=request.session['user_id'])
    requests = ServiceRequest.objects.filter(assigned_expert=expert, status='Scheduled')
    return render(request, 'expert/assistance_request.html', {'requests': requests})

@login_required(login_url='login')
def consultation_packages(request):
    expert = get_object_or_404(ExpertRegistration, user_id=request.session['user_id'])
    packages = ConsultationPackage.objects.filter(expert=expert)
    return render(request, 'expert/consultation_packages.html', {"packages": packages})

@login_required(login_url='login')
def consultation_package_form(request):
    return render(request, 'expert/consultation_package_form.html')

@login_required(login_url='login')
def feedback(request):
    return render(request, 'expert/feedback.html')

@login_required(login_url='login')
def feedback(request):
    return render(request, 'expert/feedback.html')

def login2(request):
    return render(request, 'login.html')


def registration_form(request):
    if request.method == 'POST':
        surname = request.POST.get('surname')
        firstname = request.POST.get('firstname')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        district = request.POST.get('district')
        country = request.POST.get('country')
        company = request.POST.get('company')
        role_in_company = request.POST.get('role_in_company')
        
        # Check if the email is already used
        if CustomUser.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email already in use. Please use a different email.')
            return render(request, 'entrepreneur/register_entrepreneur.html')
        
        # Generate password
        password = generate_password(firstname)
        try:
             # Send the password via email
            send_password_email(email, password)
        except gaierror:
            return render(request, 'error.html', {'error': 'Failed to send the password via Email. Please make sure your email is correct or have internet connection!'})
        
        user = CustomUser.objects.create_user(email=email, password=password, user_type='entrepreneur')
        
        # Save the data to the Entrepreneur model
        entrepreneur = Registration.objects.create(
            user=user,
            surname=surname,
            firstname=firstname,
            gender=gender,
            email=email,
            contact=contact,
            district=district,
            country=country,
            company=company,
            role_in_company=role_in_company,
            password=make_password(password)
        )
        
        entrepreneur.save()
        
        return redirect('after_register')
    
    return redirect('register_entrepreneurs')


@login_required(login_url='login')
def submit_service_request(request):
    if request.method == 'POST':
        business_idea = request.POST.get('title')
        industry = request.POST.get('industry')
        description = request.POST.get('description')
        target_market = request.POST.get('market')
        consultation_time = request.POST.get('consultation_time')
        consultation_date = request.POST.get('consultation_date')
        urgency_level = request.POST.get('urgency_level')
        comments = request.POST.get('comments')
        attachment = request.FILES.get('attachment')
        entrepreneur = get_object_or_404(Registration, user_id=request.session['user_id'])

        if attachment:
            fs = FileSystemStorage(location='attachments/')
            attachment_file = fs.save(attachment.name, attachment)
            attachment_url = fs.url(attachment_file)
        else:
            attachment_url = None

        ServiceRequest.objects.create(
            business_idea=business_idea,
            industry=industry,
            description=description,
            target_market=target_market,
            consultation_time=consultation_time,
            consultation_date=consultation_date,
            urgency_level=urgency_level,
            attachment=attachment_url,
            comments=comments,
            requester=entrepreneur
        )

        return redirect('homepage1')  # Redirect to a success page or another page after submission

    return render(request, 'service_request_form.html')
#posting business ideas
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import BusinessIdeas



################################   Admin views   ###################################

@login_required(login_url='loginAdmin')
def logout2(request):
    logout(request)
    return render(request, 'login2.html')

def loginAdmin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password= password )
        if user is not None and user.user_type == "admin":
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'login2.html', {'error': 'Invalid credentials'})
    return render(request, 'login2.html')

login_required(login_url='loginAdmin')
def admin2(request):
    return render(request, 'index2.html')

@login_required(login_url='loginAdmin')
def allTables(request):
    requests = ServiceRequest.objects.all()
    scheduled_meetings = ScheduledMeeting.objects.all()
    reply_requests = ReplyRequest.objects.all()
    forward = ReplyRequest.objects.filter(status='sent')
    context = {
        'requests': requests,
        'scheduled_meetings': scheduled_meetings,
        'reply_requests': reply_requests,
        'forward': forward
    }
    return render(request, 'admin/tables/simple.html', context)



@login_required(login_url='loginAdmin')
def approve_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    if request.method == 'POST':
        expert_id = request.POST.get('expert')
        if expert_id:
            expert = get_object_or_404(ExpertRegistration, id=expert_id)
            service_request.assigned_expert = expert
        service_request.status = 'Completed'
        service_request.save()
        return redirect('allTables')
    experts = ExpertRegistration.objects.filter(user_type='expert')
    return render(request, 'admin/tables/approve_request.html', {'request': service_request, 'experts': experts})

@login_required(login_url='loginAdmin')
def charts(request):
    return render(request, 'admin/charts/chartjs.html')

@login_required(login_url='loginAdmin')
def general_forms(request):
    return render(request, 'admin/forms/general.html')

@login_required(login_url='loginAdmin')
def advanced_forms(request):
    return render(request, 'admin/forms/advanced.html')

@login_required(login_url='loginAdmin')
def validation_forms(request):
    return render(request, 'admin/forms/validation.html')

@login_required(login_url='loginAdmin')
def mailbox(request):
    return render(request, 'admin/mailbox/mailbox.html')

@login_required(login_url='loginAdmin')
def compose_mail(request):
    return render(request, 'admin/mailbox/compose.html')

@login_required(login_url='loginAdmin')
def read_mail(request):
    return render(request, 'admin/mailbox/read-mail.html')

@login_required(login_url='loginAdmin')
def admin_calendar(request):
    return render(request, 'admin/pages/calendar.html')

@login_required(login_url='loginAdmin')
def admin_gallery(request):
    return render(request, 'admin/pages/gallery.html')

@login_required(login_url='loginAdmin')
def admin_users_entr(request):
    entrepreneurs = Registration.objects.all()
    return render(request, 'admin/users/entrepreneurs.html', {'entrs': entrepreneurs})

@login_required(login_url='loginAdmin')
def admin_users_expert(request):
    experts = ExpertRegistration.objects.all()
    return render(request, 'admin/users/experts.html', {'experts': experts})

@login_required(login_url='loginAdmin')
def admin_users_investor(request):
    investors = Investor.objects.all()
    return render(request, 'admin/users/investors.html', {'investors': investors})

@login_required(login_url='loginAdmin')
def admin_proposals(request):
    return render(request, 'admin/pages/proposals.html')

@login_required(login_url='loginAdmin')
def admin_requests(request):
    return render(request, 'admin/pages/assistance_requests.html')

@login_required(login_url='loginAdmin')
def admin_meetings(request):
    return render(request, 'admin/pages/meetings.html')

@login_required(login_url='loginAdmin')
def admin_investment_deals(request):
    return render(request, 'admin/pages/investment_deals.html')

@login_required(login_url='loginAdmin')
def admin_investment_funds(request):
    return render(request, 'admin/pages/investment_funds.html')

@login_required(login_url='loginAdmin')
def admin_packages(request):
    return render(request, 'admin/pages/packages.html')

@login_required(login_url='loginAdmin')
def admin_reply_mail(request):
    return render(request, 'admin/pages/reply_mail.html')

@login_required(login_url='loginAdmin')
def table_data(request):
    entrepreneurs = Registration.objects.all()
    experts = ExpertRegistration.objects.all()
    investors = Investor.objects.all()
    ideas = BusinessIdeas.objects.all()
    requests = ServiceRequest.objects.all()
    deals = InvestmentDeal.objects.all()
    funds = InvestmentFunds.objects.all()
    scheduled_meetings = ScheduledMeeting.objects.all()
    context = {
        'entrepreneurs': entrepreneurs,
        'experts': experts,
        'investors': investors,
        'ideas': ideas,
        'requests': requests,
        'deals': deals,
        'funds': funds,
        'meetings': scheduled_meetings,
    }
    return render(request, 'admin/tables/data.html', context)

@login_required(login_url='loginAdmin')
@require_POST
def update_meeting_status(request, meeting_id, status):
    meeting = get_object_or_404(ScheduledMeeting, id=meeting_id)
    
    if status == 'Denied':
        denial_reason = request.POST.get('denial_reason', '')
        meeting.status = 'Denied'
        meeting.denial_reason = denial_reason
    elif status == 'Approved':
        meeting.status = 'Approved'
    elif status == 'Pending':
        meeting.status = 'Pending'
    
    meeting.save()
    return redirect('allTables')


@login_required(login_url='loginAdmin')
def forward_request(request_id):
    request_instance = get_object_or_404(ReplyRequest, id=request_id)
    service_request = get_object_or_404(ServiceRequest, id=request_instance.service_request.id)
    service_request.status = 'Concluded'
    service_request.save()
    request_instance.status = 'SENT'
    request_instance.save()


##############################   end of admin views   ############################


@login_required(login_url='login')
def replay_requests_made(request):
    service_request = get_object_or_404(ServiceRequest, id=request.GET.get('request_id'))
    approved_meeting = get_object_or_404(ScheduledMeeting, service_request=service_request)
    expert = get_object_or_404(ExpertRegistration, user_id=request.session['user_id'])
    resources = Resource.objects.filter(expert=expert)
    context = {
        'resources': resources,
        'meeting': approved_meeting,
        'request': service_request,
    }
    return render(request, 'expert/reply.html', context)


from .models import ReplyRequest

@login_required(login_url='login')
def replay_requests_madetothemeeting(request):
    if request.method == 'POST':
        meeting_id = request.POST.get('meeting_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        comments = request.POST.get('text_area')

        # Assuming ScheduledMeeting and other necessary imports are present
        meeting = ScheduledMeeting.objects.get(pk=meeting_id)
        request_id = get_object_or_404(ServiceRequest, id=request.GET.get('request'))

        reply_request = ReplyRequest.objects.create(
            meeting=meeting,
            title=title,
            description=description,
            comments=comments,
            service_request=request_id,
            status='NOT_SENT'  # Set default status
        )
        reply_request.save()

 
        return redirect('homepage1')  
    return render(request, 'expert/reply.html')
