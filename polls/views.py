# Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from .forms import CommentForm
from .models import Comment

from .models import Choice, Question


def indexView(request):
    question = Question.objects.all
    comment = Comment.objects.all
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comm = form.save(commit=False)
            comm.user = request.user
            comm.post = comment
            comm.save()
    else:
        form = CommentForm()
    return render(request, "polls/index.html", {"questions": question, "form":
        form, 'comments': comment})





def comment(request, question_id):
    comment = Comment.objects.filter(question_id=question_id)
    form = CommentForm()
    comm = form.save(commit=False)
    comm.user = request.user
    comm.save()
    return render(request, "polls/index.html", {"question": question, "form": form, 'comment': comment})


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
