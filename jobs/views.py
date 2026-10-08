from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.db.models import Q

from .models import Profile
from .models import Job
from .models import Application

from .forms import RegisterForm
from .forms import JobForm
from .forms import ApplicationForm
from .forms import ProfileForm


def home(request):

    jobs = Job.objects.all()[:6]

    return render(
        request,
        'home.html',
        {
            'jobs': jobs
        }
    )


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Account created successfully.'
            )

            return redirect('dashboard')

    else:

        form = RegisterForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


def job_list(request):

    query = request.GET.get(
        'q',
        ''
    )

    location = request.GET.get(
        'location',
        ''
    )

    category = request.GET.get(
        'category',
        ''
    )

    jobs = Job.objects.all()

    if query:

        jobs = jobs.filter(

            Q(title__icontains=query) |

            Q(company__icontains=query) |

            Q(description__icontains=query)

        )

    if location:

        jobs = jobs.filter(
            location__icontains=location
        )

    if category:

        jobs = jobs.filter(
            category__icontains=category
        )

    return render(
        request,
        'job_list.html',
        {
            'jobs': jobs,
            'query': query,
            'location': location,
            'category': category
        }
    )


def job_detail(request, pk):

    job = get_object_or_404(
        Job,
        pk=pk
    )

    already_applied = False

    if request.user.is_authenticated:

        already_applied = Application.objects.filter(
            job=job,
            applicant=request.user
        ).exists()

    return render(
        request,
        'job_detail.html',
        {
            'job': job,
            'already_applied': already_applied
        }
    )


@login_required
def apply_job(request, pk):

    job = get_object_or_404(
        Job,
        pk=pk
    )

    profile = request.user.profile

    if profile.role != 'seeker':

        messages.error(
            request,
            'Only job seekers can apply.'
        )

        return redirect(
            'job_detail',
            pk=pk
        )

    if Application.objects.filter(
        job=job,
        applicant=request.user
    ).exists():

        messages.warning(
            request,
            'You already applied for this job.'
        )

        return redirect(
            'job_detail',
            pk=pk
        )

    if request.method == 'POST':

        form = ApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            application = form.save(
                commit=False
            )

            application.job = job

            application.applicant = request.user

            application.save()

            messages.success(
                request,
                'Application submitted successfully.'
            )

            return redirect(
                'dashboard'
            )

    else:

        form = ApplicationForm()

    return render(
        request,
        'apply_job.html',
        {
            'form': form,
            'job': job
        }
    )


@login_required
def dashboard(request):

    profile = request.user.profile

    if profile.role == 'recruiter':

        jobs = Job.objects.filter(
            posted_by=request.user
        )

        applications = Application.objects.filter(
            job__posted_by=request.user
        )

        return render(
            request,
            'recruiter_dashboard.html',
            {
                'jobs': jobs,
                'applications': applications
            }
        )

    applications = Application.objects.filter(
        applicant=request.user
    )

    return render(
        request,
        'seeker_dashboard.html',
        {
            'applications': applications
        }
    )


@login_required
def add_job(request):

    if request.user.profile.role != 'recruiter':

        messages.error(
            request,
            'Recruiter access required.'
        )

        return redirect('dashboard')

    if request.method == 'POST':

        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(
                commit=False
            )

            job.posted_by = request.user

            job.save()

            messages.success(
                request,
                'Job posted successfully.'
            )

            return redirect(
                'dashboard'
            )

    else:

        form = JobForm()

    return render(
        request,
        'job_form.html',
        {
            'form': form,
            'title': 'Post a Job'
        }
    )


@login_required
def edit_job(request, pk):

    job = get_object_or_404(
        Job,
        pk=pk,
        posted_by=request.user
    )

    if request.method == 'POST':

        form = JobForm(
            request.POST,
            instance=job
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Job updated successfully.'
            )

            return redirect(
                'dashboard'
            )

    else:

        form = JobForm(
            instance=job
        )

    return render(
        request,
        'job_form.html',
        {
            'form': form,
            'title': 'Edit Job'
        }
    )


@login_required
def delete_job(request, pk):

    job = get_object_or_404(
        Job,
        pk=pk,
        posted_by=request.user
    )

    if request.method == 'POST':

        job.delete()

        messages.success(
            request,
            'Job deleted successfully.'
        )

    return redirect(
        'dashboard'
    )


@login_required
def update_application_status(
    request,
    pk,
    status
):

    application = get_object_or_404(
        Application,
        pk=pk,
        job__posted_by=request.user
    )

    if status not in [
        'Pending',
        'Shortlisted',
        'Rejected'
    ]:

        messages.error(
            request,
            'Invalid status.'
        )

        return redirect(
            'dashboard'
        )

    application.status = status

    application.save()

    messages.success(
        request,
        'Application status updated.'
    )

    return redirect(
        'dashboard'
    )


@login_required
def profile(request):

    profile = request.user.profile

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Profile updated.'
            )

            return redirect(
                'profile'
            )

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'profile.html',
        {
            'form': form
        }
    )
