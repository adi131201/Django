from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth 
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowerCount
from itertools import chain
import random

# Create your views here.

@login_required(login_url='signin')
def index(request):
    userObject = User.objects.get(username=request.user.username)
    userProfile = Profile.objects.get(user=userObject)
    
    userFollowingList = []
    feed = []

    userFollowing = FollowerCount.objects.filter(follower=request.user.username)

    for users in userFollowing:
        userFollowingList.append(users.user)
    
    for usernames in userFollowingList:
        feedLists = Post.objects.filter(user=usernames)
        feed.append(feedLists)

    feedList = list(chain(*feed))

    #user suggestions
    allUsers = User.objects.all()
    userFollowingAll = []

    for user in userFollowing:
        userList = User.objects.get(username= user.user)
        userFollowingAll.append(userList)

    newSuggestionsList = [x for x in list(allUsers) if (x not in list(userFollowingAll))]

    currUser = User.objects.filter(username=request.user.username)
    finalSuggestionList = [x for x in list(newSuggestionsList) if (x not in list(currUser))]
    random.shuffle(finalSuggestionList)

    usernameProfile = []
    usernameProfileList=[]

    for users in finalSuggestionList:
        usernameProfile.append(users.id)
    
    for ids in usernameProfile:
        profileLists = Profile.objects.filter(id_user=ids)
        usernameProfileList.append(profileLists)
    
    suggestionsUsernameProfileList = list(chain(*usernameProfileList))

    return render(request,'index.html', {'userProfile': userProfile, "posts": feedList, 'suggestionsUsernameProfileList': suggestionsUsernameProfileList[:4]})

@login_required(login_url='signin')
def profile(request, pk):
    userObject = User.objects.get(username=pk)
    userProfile = Profile.objects.get(user=userObject)
    userPosts = Post.objects.filter(user=pk)
    userPostLength = len(userPosts)

    follower = request.user.username
    user = pk

    if FollowerCount.objects.filter(follower=follower, user=user).first():
        buttonText = 'Unfollow'
    else:
        buttonText = 'Follow'
    userFollowers = len(FollowerCount.objects.filter(user=pk))
    userFollowing = len(FollowerCount.objects.filter(follower=pk))

    context = {
        'userObject': userObject,
        'userProfile': userProfile,
        'userPosts': userPosts,
        'userPostLength': userPostLength,
        'buttonText': buttonText,
        'userFollowers': userFollowers,
        'userFollowing': userFollowing,
    }

    return render(request, 'profile.html', context)

def follow(request):
    if request.method == "POST":
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowerCount.objects.filter(follower=follower, user=user).first():
            deleteFollower = FollowerCount.objects.get(follower=follower, user=user)
            deleteFollower.delete()
            return redirect('/profile/'+user)
        
        else:
            newFollower = FollowerCount.objects.create(follower=follower, user=user)
            newFollower.save()
            return redirect('/profile/'+user)

    else:
        return redirect('/')

@login_required(login_url='signin')
def search(request):
    userObject = User.objects.get(username=request.user.username)
    userProfile = Profile.objects.get(user=userObject)
    
    usernameProfileList = []

    if request.method=='POST':
        username = request.POST['username']
        usernameObject = User.objects.filter(username__icontains=username)

        usernameProfile = []

        for users in usernameObject:
            usernameProfile.append(users.id)
        
        for ids in usernameProfile:
            profileLists = Profile.objects.filter(id_user=ids)
            usernameProfileList.append(profileLists)
        
        usernameProfileList = list(chain(*usernameProfileList))

    return render(request, 'search.html', {'userProfile': userProfile, 'usernameProfileList': usernameProfileList})

@login_required(login_url='signin')
def likePost(request):
    username = request.user.username
    postId = request.GET.get('post_id')

    post = Post.objects.get(id=postId)

    likeFilter = LikePost.objects.filter(postId=postId, username=username).first()
    if likeFilter==None:
        newLike = LikePost.objects.create(postId=postId, username=username)
        newLike.save()
        post.no_of_like = post.no_of_like+1
        post.save()
        return redirect('/')
    else:
        likeFilter.delete()
        post.no_of_like = post.no_of_like-1
        post.save()
        return redirect('/')

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #login user and redirect to the settings page.
                userlogin = auth.authenticate(username=username, password=password)
                auth.login(request, userlogin)

                #create a Profile object for the new user.
                userModel = User.objects.get(username=username)
                newProfile = Profile.objects.create(user=userModel, id_user=userModel.id)
                newProfile.save()
                return redirect('settings')
            
        else:
            messages.info(request, 'Password does not match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    return render(request,'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('imageUpload')
        caption = request.POST['caption']
        newPost = Post.objects.create(user = user, image=image, caption=caption)
        newPost.save()

        return redirect('/')
    
    else:
        return redirect('/')
    return HttpResponse('<h1>Upload View</h1>')

@login_required(login_url='signin')
def settings(request):
    userProfile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = userProfile.profileImg
            bio = request.POST['bio']
            location = request.POST['location']

            userProfile.profileImg = image
            userProfile.bio = bio
            userProfile.location = location
            userProfile.save()
        
        if request.FILES.get('image')!=None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            
            userProfile.profileImg = image
            userProfile.bio = bio
            userProfile.location = location
            userProfile.save()

        return redirect('settings')

    return render(request, 'setting.html', {'userProfile': userProfile})