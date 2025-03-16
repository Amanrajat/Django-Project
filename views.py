from django.shortcuts import render
from .models import Tweet , comment
from .forms import TweetForm , CommentForm
from .forms import UserRegistrationForm
from django.shortcuts import get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse


# Create your views here.

def index(request):
    return render(request , 'index.html')



def  tweet_list(request):
    tweets= Tweet.objects.all().order_by('-created_at')
    return render(request , 'tweet_list.html' , {'tweets':tweets})


@login_required
def tweet_create(request):
    if request.method == "POST":
     form = TweetForm(request.POST , request.FILES)
     if form.is_valid():
        tweet = form.save(commit = False)
        tweet.user = request.user
        tweet.save()
        return redirect('tweet_list') 
    else:
      form = TweetForm()
    return render(request , 'tweet_form.html' , {'form': form})

@login_required
def tweet_edit(request , tweet_id):
   tweet = get_object_or_404(Tweet ,pk=tweet_id , user = request.user)
   if request.method == "POST":
      form = TweetForm(request.POST , request.FILES , instance=tweet)
      if form.is_valid():
         tweet = form.save(commit=False)
         tweet.user = request.user
         tweet.save()
         return redirect('tweet_list')
   else:
      form = TweetForm(instance=tweet)
   return render(request , 'tweet_form.html' , {'form': form})   

@login_required
def tweet_delete(request , tweet_id):
    tweet = get_object_or_404(Tweet , pk=tweet_id , user=request.user)
    if request.method == "POST":
       tweet.delete()
       return redirect('tweet_list')
    return render(request , 'tweet_confirm_delete.html' , {'tweet': tweet}) 


# register view

def register(request):
    
   if request.method == "POST":
     form =UserRegistrationForm(request.POST)
     if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(request , user)
        return redirect('tweet_list')
   else:
      form=UserRegistrationForm()
  
   return render(request , 'registration/register.html', {'form': form}) 

# search_tweets
@login_required(login_url='login')
def search_tweets(request):
   query = request.GET.get('q','') 
   tweets = Tweet.objects.all()  # Fetch all tweets
   if query:
      tweets = Tweet.objects.filter(text__icontains=query) | Tweet.objects.filter(user__username__icontains=query)
    
   else:
      tweets = Tweet.objects.all()   

   return render(request, 'search_tweets.html', {'tweets': tweets, 'query': query}) 





# tweet Detail

 
def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    comments = tweet.comments.all()
    comment_form = CommentForm()
    return render(request, "tweet_detail.html", {"tweet": tweet, "comments": comments, "comment_form": comment_form})

# comment
 
@login_required
def comment_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.tweet = tweet
            comment.user = request.user
            comment.save()
            return redirect( "tweet_list")
        return redirect( "tweet_detail", tweet_id=tweet_id)



# like 

@login_required
def like_tweet(request, tweet_id):
   if request.method == "GET":
      tweet = get_object_or_404(Tweet, id=tweet_id)
      if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
        liked = False
      else:
        tweet.likes.add(request.user)
        liked = True

      return JsonResponse({"liked": liked, "like_count": tweet.likes.count()})
   
   return JsonResponse({"error": "Invalid request"}, status=400)
   
