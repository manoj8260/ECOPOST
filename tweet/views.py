from django.shortcuts import render
from tweet.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
import os
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import random
from django.core.mail import send_mail
import logging
logger = logging.getLogger(__name__)



@login_required
def home(request):
    un = request.session.get('username')
    if not un:
        return redirect('user_login')  
    try:
        UO = User.objects.get(username=un)
    except User.DoesNotExist:
        return redirect('user_login')  
    try:
        PO = Profile.objects.get(username=UO) 
    except Profile.DoesNotExist:
        PO = None  

    userprofile = Profile.objects.filter(username=UO)
    other_profiles = Profile.objects.exclude(username=UO)
    all_profiles = list(userprofile) + list(other_profiles)
    tweets = Tweet.objects.all().order_by('-created_at')
    allusers=User.objects.all()
    countsaved = count_saved(request)
    userstory = Story.objects.all()
    context = {
        'UO': UO,
        'PO': PO,
        'tweets': tweets,
        'all_profile': all_profiles,
        'number': countsaved,
        'userstory': userstory,
        allusers : 'allusers',
       }
    return render(request, 'tweet/home.html', context)

    
def register(request):
    ERFO=UserModel()
    EPFO=ProfileModel()
    d={'ERFO':ERFO,'EPFO':EPFO}
    if request.method == 'POST' and request.FILES:
        UFDO=UserModel(request.POST)
        PFDO=ProfileModel(request.POST,request.FILES)
        if UFDO.is_valid() and PFDO.is_valid():
            pw=UFDO.cleaned_data.get('password')
            MUFDO=UFDO.save(commit=False)
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO=PFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()
            email=UFDO.cleaned_data.get('email')
            message = f"Hello {UFDO.cleaned_data.get('first_name')}\n \t Your Registration against our application is successfully Done with username:{UFDO.cleaned_data.get('username')} \n\n \t\t Thanks & regards \n \t\tEcoPost Team"
            try:
             send_mail(
                'your otp',
                message,
                'kumarmanoj8260910@gmail.com',
                [email],
                fail_silently=False
            )
            except Exception as e:
                    return HttpResponse(f"Email sending failed: {e}")
            return HttpResponseRedirect(reverse('user_login'))
        return HttpResponse('invalid data')
    return render(request,'tweet/register.html',d)



def user_login(request):
    if request.method == 'POST':
        try:
            un = request.POST.get('username')
            pw = request.POST.get('password')
            if not un or not pw:
                return render(request,'error.html',{'message': "Both username and password are required."})
            AO = authenticate(username=un, password=pw)
            if AO:
                request.session['username'] = un
                login(request, AO)
                return HttpResponseRedirect(reverse('home'))
            else:
                 return render(request,'error.html',{'message': "User not found or invalid credentials."})           
        except Exception : 
            return HttpResponse("An unexpected error occurred. Please try again later.")
    return render(request, 'tweet/user_login.html')


@login_required
def user_logout(request):
     logout(request)
     return render(request,'tweet/user_login.html')
   
@login_required
def user_profile(request):
    if request.method == 'GET':
        un = request.session.get('username')
        if not un:
            return render(request,'error.html',{'message': "Username not found in session."})

        try:
            UO = User.objects.get(username=un)
        except User.DoesNotExist:
            return render(request,'error.html',{'message': "User does not exist."})
        try:
            PO = Profile.objects.get(username=UO)
        except Profile.DoesNotExist:
            return render(request,'error.html',{'message': "Profile does not exist."})
        countsaved = count_saved(request) 
        tweets = Tweet.objects.filter(username=UO) 
        posts = count_post(request)

        context = {
            'UO': UO,
            'PO': PO,
            'number': countsaved,
            'tweets': tweets,
            'posts': posts,
            }
        return render(request, 'tweet/user_profile.html', context)
    return render(request,'error.html',{'message': "Invalid method"})

  
@login_required
def create_tweet(request):
    un = request.session.get('username')
    if not un:
            return render(request,'error.html',{"message": "Username not found in session."})
    try:
            UO = User.objects.get(username=un)
    except User.DoesNotExist:
            return render(request,'error.html',{"message": "User does not exist."})

    try:
            PO = Profile.objects.get(username=UO)
    except Profile.DoesNotExist:
            return render(request,'error.html',{"message": "Profile does not exist."})
    ETFO=TweetModel() 
    countsaved=count_saved(request) 
    d={'ETFO':ETFO,'PO':PO,'number':countsaved}
    if request.method =='POST' and request.FILES:
        TFDO=TweetModel(request.POST,request.FILES)
        if UO:
           MTFDO=TFDO.save(commit=False)
           MTFDO.username= UO
           MTFDO.profile=PO
           MTFDO.save()
           return  HttpResponseRedirect(reverse('home')) 
        return render(request,'error.html',{"message": "Invalid Information"})
    return render(request,'tweet/create_tweet.html',d)

@login_required
def update(request,pk):
    un = request.session.get('username')
    if not un:
        return render(request,'error.html',{"message": "Username not found in session."})
    try:
        UO = User.objects.get(username=un)
    except User.DoesNotExist:
         return render(request,'error.html',{"message": "User does not exist."})  
    try:
        PO = Profile.objects.get(username=UO)
    except Profile.DoesNotExist:
         return render(request,'error.html',{"message": "Profile does not exist."})
    try:
       TO=Tweet.objects.get(pk=pk)
    except Tweet.DoesNotExist:
        return render(request,'error.html',{"message": "Tweet does not exist."})
    countsaved=count_saved(request) 
    d={'TO':TO,'PO':PO,'number':countsaved}
    if request.method == 'POST'and request.FILES:
        if TO.photo:
            os.remove(TO.photo.path)
        TO.text=request.POST.get('text')
        TO.photo=request.FILES.get('photo')
        TO.save()
        return HttpResponseRedirect(reverse('home'))    
    return render(request,'tweet/update.html',d)

@login_required
def delete(request,pk):
    if request.method  == 'POST':
        TO=Tweet.objects.get(pk=pk)
        if TO.username.username  == request.session.get('username'):
          TO.delete()
          return HttpResponseRedirect(reverse('home'))
        return render(request,'error.html',{"message": "you dont delete other tweet"})
    else:
        tweet = Tweet.objects.get(pk = pk )
        return render(request,'tweet/tweetdeleteconfirm.html',{'tweet':tweet})
    

@login_required
def save(request,pk):
    un = request.session.get('username')
    if not un:
        return render(request,'error.html',{"message": "Username not found in session."})
    try:
        UO = User.objects.get(username=un)
    except User.DoesNotExist:
        return render(request,'error.html',{"message": "User does not exist."})
    try:
       TO=Tweet.objects.get(pk=pk)
    except Tweet.DoesNotExist:
        return render(request,'error.html',{"message": "Tweet does not exist."})
    AST=Saved.objects.filter(tweet=TO)
    if AST and AST[0].username.username  == un:
        AST.delete()
        return HttpResponseRedirect(reverse('saved'))
    else:
        if  TO.username.username != un:
          save_tweet=Saved(username=UO,tweet=TO)
          save_tweet.save()
          return HttpResponseRedirect(reverse('saved')) 
        return render(request,'error.html',{"message": "you dont save your tweet"})
        

@login_required    
def saved(request):
    un = request.session.get('username')
    if not un:
         return render(request,'error.html',{"message": "Username not found in session."})
    try:
        UO = User.objects.get(username=un)
    except User.DoesNotExist:
        return HttpResponse("User does not exist.")
    try:
       PO=Profile.objects.get(username=UO) 
    except Profile.DoesNotExist:
        return HttpResponse("Profile does not exist.")          
    ASO=Saved.objects.filter(username=UO)
    countsaved=count_saved(request)
    d={'tweets':ASO,'PO':PO,'number':countsaved}
    return render(request,'tweet/saved.html',d)

@login_required
def like(request,pk):
    un = request.session.get('username')
    if not un:
        return render(request,'error.html',{"message": "Username not found in session."})
    try:
        UO = User.objects.get(username=un)
    except User.DoesNotExist:
        return HttpResponse("User does not exist.")
    try:
       TO=Tweet.objects.get(pk=pk)
    except Tweet.DoesNotExist:
        return HttpResponse("Tweet does not exist.")
    LO=Liked.objects.filter(username=UO,tweet=TO)
    if LO:
        TO.like -=1
        TO.save()
        LO.delete()
    else:
         TO.like +=1
         TO.save()
         LO=Liked(username=UO,tweet=TO)
         LO.save()
    return HttpResponseRedirect(reverse('home'))

@login_required
def savecomment(request, pk):
    if request.method == 'POST':
        print(f"Received pk: {pk}")  # Debugging
        try:
            TO = Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            return HttpResponse("Tweet not found.", status=404)
        comment_text = request.POST.get('cmt')
        un = request.session.get('username')
        if not un:
            return HttpResponse("User not logged in.", status=403)
        try:
            UO = User.objects.get(username=un)
        except User.DoesNotExist:
            return HttpResponse("User not found.", status=404)      
        TO.save_comment+=1
        CO = Comment(username=UO, tweet=TO, comment_text=comment_text)
        TO.save()
        CO.save()
        return HttpResponseRedirect(reverse('commentes',args=[TO.pk]))

@login_required
def commentes(request,pk):
    try:
        TO = Tweet.objects.get(pk=pk)
    except Tweet.DoesNotExist:
        return HttpResponse("Tweet not found.", status=404)
    un = request.session.get('username')
    if not un:
        return render(request,'error.html',{"message": "Username not found in session."})
    try:
        UO = User.objects.get(username=un)
    except User.DoesNotExist:
        return HttpResponse("User does not exist.")
    try:
        PO=Profile.objects.get(username=UO)
    except Profile.DoesNotExist:
        return HttpResponse("Profile does not exist.")
   
    countsaved=count_saved(request) 
    comments = Comment.objects.filter(tweet=TO).order_by('-comment_time')  
    return render(request, 'tweet/comments.html', {'comments': comments,'PO':PO,'number':countsaved,'UO':UO})

@method_decorator(login_required, name='dispatch')
class DeleteComment(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        tweet=comment.tweet
        if hasattr(tweet, 'save_comment'):
            tweet.save_comment = max(0, tweet.save_comment - 1)  
            tweet.save()       
        return redirect(reverse('home'))

# count number of tweet
def count_saved(request):
    count=0
    un = request.session.get('username')
    if not un:
        return HttpResponse("Username not found in session.")
    try:
        UO = User.objects.get(username=un)
    except User.DoesNotExist:
        return HttpResponse("User does not exist.")
    saved_tweet=Saved.objects.filter(username=UO)
    for saved in saved_tweet:
        count+=1     
    return count

@login_required
def story(request):
    if request.method == 'GET':
        form = StoryForm()
        un=request.user.username
        if not un:
             return render(request,'error.html',{"message": "Username not found in session."})

        try:
            UO = User.objects.get(username=un)
        except User.DoesNotExist:
            return HttpResponse("User not found.", status=404)
        try:
            PO=Profile.objects.get(username=UO)
        except Profile.DoesNotExist:
            return HttpResponse("profile not found.", status=404)   
        countsaved=count_saved(request)    
        print(countsaved)
        return render(request, 'tweet/story.html', {'form': form,'PO':PO,'number':countsaved})
    elif request.method == 'POST':
        form = StoryForm(request.POST,request.FILES)
        PO=Profile.objects.get(username=request.user)
        if form.is_valid():
            form.instance.username = request.user
            form.instance.profile=PO
            form.save()
            return HttpResponseRedirect(reverse('home'))
        return HttpResponse('invalid data')
    
@method_decorator(login_required, name='dispatch')
class Showstory(View):
    def get(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            user = profile.username  
            allstory = Story.objects.filter(username=user) 
            try:
             un=request.session.get('username')
            except Exception:
                return redirect('user_login')
            
            UO=User.objects.get(username=un)

            PO=Profile.objects.get(username=UO)
            countsaved=count_saved(request) 

            context = {'allstory': allstory,'PO':PO,'number':countsaved,'UO':UO}
            
            return render(request, 'tweet/showstory.html', context)
        except User.DoesNotExist:
            return HttpResponse('User not Found', status=404)
        except Profile.DoesNotExist:
            return HttpResponse('Profile not Found', status=404)
        except Story.DoesNotExist:
            return HttpResponse('Story not Found', status=404)
        
@method_decorator(login_required, name='dispatch')
class  Explores(View):
    def get(self,request):
        un=request.user.username
        if not un:
            return render(request,'error.html',{"message": "Username not found in session."})
        try:
            UO = User.objects.get(username=un)
        except User.DoesNotExist:
            return HttpResponse("User not found.", status=404)
        try:
            PO=Profile.objects.get(username=UO)
        except Profile.DoesNotExist:
            return HttpResponse("profile not found.", status=404)  
        countsaved=count_saved(request) 
        all_media = Explore.objects.all()
        return render(request,'tweet/explore.html',{'PO':PO,'number':countsaved,'media_list': all_media})


class forgot_password(View): 
    def get(self,request):
        return render(request,'tweet/forgot_password.html')
    def post(self,request):
        un=request.POST.get('un')
        if not un:
            return render(request,'error.html',{"message": "Username not found in session."})
        try:
            UO=User.objects.get(username=un)
        except User.DoesNotExist: 
            return render(request,'error.html',{'message': 'User not found'})
        otp=random.randint(1000,9999)
        request.session['username']=un
        request.session['otp']=otp
        if UO:
            try:
                email=UO.email
                mesaage=f'your otp  is : {otp}'
                send_mail(
                'your otp',
                mesaage,
                'kumarmanoj8260910@gmail.com',
                [email],
                fail_silently=False
               )
            except Exception as e:
                    return HttpResponse(f"Email sending failed: {e}")
            print(otp)
            return HttpResponseRedirect(reverse('otp'))
        return render(request,'error.html',{"message": "'User not found."})
    
class otp(View):
    def get(self,request):
        return render(request,'tweet/otp.html')
    def post(self,request):
        uotp=request.POST.get('uotp')
        sotp=request.session.get('otp')
        print(uotp)
        if uotp == str(sotp) :
            return HttpResponseRedirect(reverse('new_password'))
        return render(request,'alert.html',{"message": "Invalid otp"})
    
class new_password(View):
    def get(self,request):
        un=request.session.get('username')
        if not un :
            return HttpResponse("user not logged in.", status=403)     
        try:
            UO=User.objects.get(username=un)
        except User.DoesNotExist:
            return render(request,'error.html',{"message": "'User not found."}) 
        d={'UO':UO}
        return render(request,'tweet/new_password.html',d) 
    def post(self,request):
        npw=request.POST.get('npw')   
        cpw=request.POST.get('cpw')   
        if npw == cpw :
            un=request.session.get('username')
            if not un :
               return HttpResponse("user not logged in.", status=403)     
            try:
              UO=User.objects.get(username=un)
            except User.DoesNotExist:
               return render(request,'error.html',{"message": "'User not found."}) 
            UO.set_password(cpw)
            UO.save()
            return HttpResponseRedirect(reverse('user_login'))                 
        return HttpResponse('password doesnot match')


class ChangePassword(View):
    def get(self, request):
        un = request.session.get('username')
        if not un:
            return HttpResponseRedirect(reverse('user_login'))  
        try:
            UO = get_object_or_404(User, username=un)
            PO = get_object_or_404(Profile, username=UO)  
            countsaved = count_saved(request)
            context = {'UO': UO, 'PO': PO, 'number': countsaved}
            return render(request, 'tweet/change_password.html', context)
        except Exception as e:
            return HttpResponse(f"Error: {e}")
          

    def post(self, request):
        un = request.session.get('username')
        if not un:
            return HttpResponseRedirect(reverse('user_login'))  
        try:
            UO = get_object_or_404(User, username=un)
            otp = random.randint(1000, 9999)
            request.session['otp'] = otp

            if UO.email:
                message = f'Your OTP is: {otp}'
                try:
                    send_mail(
                        'Your OTP',
                        message,
                        'kumarmanoj8260910@gmail.com',  
                        [UO.email],
                        fail_silently=False
                    )
                    print(f"OTP sent: {otp}")
                except Exception as e:
                    return HttpResponse(f"Email sending failed: {e}")

            return HttpResponseRedirect(reverse('otp'))
        except Exception as e:
            return HttpResponse(f"Error: {e}")
            
    
@method_decorator(login_required, name='dispatch')
class Editprofile(View):
    def get(self, request):
        if not request.user.is_authenticated:
              return redirect('user_login')  
        try:
            user = request.user
            profile = Profile.objects.get(username=user)
            countsaved=count_saved(request) 
            context = {'UO': user, 'PO': profile,'number':countsaved}
            return render(request, 'tweet/edit_profile.html', context)
        except Profile.DoesNotExist:
            return HttpResponse("Profile does not exist", status=404)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse("User not logged in", status=400)        
        try:
            user = request.user
            profile = Profile.objects.get(username=user)
            
            if 'photo' in request.FILES and profile.profile_pic:
                if os.path.isfile(profile.profile_pic.path):
                    os.remove(profile.profile_pic.path)
            profile.profile_pic = request.FILES.get('photo', profile.profile_pic)
            profile.bio = request.POST.get('bio', profile.bio)
            profile.website = request.POST.get('website', profile.website)
            profile.phno = request.POST.get('phno', profile.phno)
            profile.save()
            return HttpResponseRedirect(reverse('home'))
        except Profile.DoesNotExist:
            return HttpResponse("Profile does not exist", status=404)

def count_post(request):
    numberofpost=0
    un=request.session.get('username')
    UO = get_object_or_404(User, username=un)
    tweetposts=Tweet.objects.filter(username=UO)
    for post in tweetposts:
        numberofpost+=1
    return numberofpost   
 
@method_decorator(login_required, name='dispatch')
class DeleteStory(View):
    def profile(self,request):
        un = request.session.get('username')
        if not un:
            return HttpResponseRedirect(reverse('login')) 
        UO = get_object_or_404(User, username=un)
        PO=get_object_or_404(Profile,username=UO)
        return PO
    def get(self,request,pk):
        try:
            story=Story.objects.get(pk=pk)
        except Story.DoesNotExist:
            return HttpResponse('story object doesnot exits ! ') 
        return render(request,'tweet/confirmdeletestory.html',{'story':story })
    def post(self,request,pk):
        try:
          Story.objects.get(pk=pk).delete() 
        except Story.DoesNotExist:
            return HttpResponse('story object deleleted')
        return HttpResponseRedirect(reverse('showstory',args=[self.profile(request).pk]))   


@login_required
def follow_user(request, user_id):
    un = request.session.get('username')
    if not un: 
        return redirect('user_login')
    try:
        UO=User.objects.get(username=un)
    except User.DoesNotExist:
        return redirect('user_login') 
    following = get_object_or_404(User, id=user_id)
    print(following.id)
    print(UO.id)
    if UO == following:
        return HttpResponse("You cannot follow yourself.", status=400)

    follow, created = Follow.objects.get_or_create(follower=UO, following=following)

    if created:
        return HttpResponseRedirect(reverse('find_user',args= [following.username]))
        return redirect('home')

    else:
        return HttpResponse("Already following this user.", status=400)

@login_required
def unfollow_user(request, user_id):
    un = request.session.get('username')
    if not un: 
        return redirect('user_login')
    try:
        UO=User.objects.get(username=un)
    except User.DoesNotExist:
        return redirect('user_login')
    following = get_object_or_404(User, id=user_id)
    follow = Follow.objects.filter(follower=UO, following=following)

    if follow.exists():
        follow.delete()
        return HttpResponseRedirect(reverse('find_user',args= [following.username])) 
    else:
        return HttpResponse("You are not following this user.", status=400)

@login_required
def search_user(request):
    if request.method == 'GET':
        user_username = request.GET.get('user_username')
        try:
          valid_userobj = User.objects.get(username = user_username)
          search_profileobj = Profile.objects.get(username = valid_userobj)
          un=request.session.get('username')
          if not un: 
              return redirect('user_login')
          try:
              UO=User.objects.get(username=un)
          except User.DoesNotExist:
              return redirect('user_login') 
          try:    
             PO=Profile.objects.get(username = UO)
          except  Profile.DoesNotExist:
              PO =None 
          countsaved = count_saved(request)
          posts= count_post(request)
          is_following = Follow.objects.filter(follower=UO, following=valid_userobj).exists()
          d={'search_profileobj':search_profileobj,
             'number':countsaved,
             'PO':PO,
             'posts':posts,
             'UO':UO,
             'is_following':is_following,
             'valid_userobj':valid_userobj
             }
          return render(request,'tweet/search_user_profile.html',d)
        except User.DoesNotExist:
            return render(request,'alert.html',{'message': 'Search object does not found'})
@login_required        
def find_user(request,name):
        user_username = name
        try:
          valid_userobj = User.objects.get(username = user_username)
          search_profileobj = Profile.objects.get(username = valid_userobj)
          un=request.session.get('username')
          if not un: 
              return redirect('user_login')
          try:
              UO=User.objects.get(username=un)
          except User.DoesNotExist:
              return redirect('user_login') 
          try:    
             PO=Profile.objects.get(username = UO)
          except  Profile.DoesNotExist:
              PO =None 
          countsaved = count_saved(request)
          posts= count_searchobj_post(request,user_username)
          is_following = Follow.objects.filter(follower=UO, following= valid_userobj).exists()
          d={'search_profileobj':search_profileobj,
             'number':countsaved,
             'PO':PO,
             'posts':posts,
             'is_following':is_following,
             'valid_userobj':valid_userobj,
             'UO':UO,
             }
          return render(request,'tweet/search_user_profile.html',d)
        except User.DoesNotExist:
            return render(request,'alert.html',{'message': 'Search object does not found'})
@login_required
def count_searchobj_post(request,username):
    numberofpost=0   
    un=username
    UO = get_object_or_404(User, username=un)
    tweetposts=Tweet.objects.filter(username=UO)
    for post in tweetposts:
        numberofpost+=1
    return numberofpost 

def followers_list(request, username):
    un = request.session.get('username')
    if not un:
        return redirect('user_login')  
    try:
        UO = User.objects.get(username=un)
    except User.DoesNotExist:
        return redirect('user_login')  
    try:
        PO = Profile.objects.get(username=UO) 
    except Profile.DoesNotExist:
        PO = None  
    user = get_object_or_404(User, username=username)
    followers = user.followers.all()  
    return render(request, 'tweet/followers_list.html', {'user': user, 'followers': followers,'PO':PO})

def following_list(request, username):
    un = request.session.get('username')
    if not un:
        return redirect('user_login')  
    try:
        UO = User.objects.get(username=un)
    except User.DoesNotExist:
        return redirect('user_login')  
    try:
        PO = Profile.objects.get(username=UO) 
    except Profile.DoesNotExist:
        PO = None  
    user = get_object_or_404(User, username=username)
    following = user.following.all() 
    return render(request, 'tweet/following_list.html', {'user': user, 'following': following,'PO':PO})


