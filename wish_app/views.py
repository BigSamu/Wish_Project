from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def userDetails(request):

    #Check if an user is logged in:
    if 'name' in request.session:
        
        currentUser = User.objects.get(id=request.session['id'])
        
        context = {
            'all_wishes': Wish.objects.all(),
            'wishes_uploaded_by_current_user': currentUser.wishes_uploaded.all() 
        }
        return render(request,'user_details.html', context)
    
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def makeWish(request):
    
    #Check if an user is logged in:
    if 'name' in request.session:

        if request.method == 'POST':
            
            #Check if the user want to submit or Cancel the operation:
            if 'cancel_operation' in request.POST:
                return redirect('/wishes')
            
            # If the user want to submit the operation, then:
            elif 'submit_operation' in request.POST:
                
                # Check if there are erros on the data submission:
                errors = Wish.objects.validatorWish(request.POST)
                if len(errors)>0:
                    for key, value in errors.items():
                        messages.error(request, value)
                    return redirect('/wishes/new')

                # If not errors are found, then create the wish:
                currentUser = User.objects.get(id=request.session['id'])
                newWish = Wish.objects.create(
                    item = request.POST['item'],
                    description = request.POST['description'],
                    uploaded_by = currentUser,
                )
                return redirect('/wishes')
        
        return render(request,'new_wish.html')
    
    return redirect('/')

def checkStats(request):

    #Check if an user is logged in:
    if 'name' in request.session:

        currentUser = User.objects.get(id=request.session['id'])
        wishesGrantedbyCurrentUser = currentUser.wishes_uploaded.filter(granted=True)
        wishesPendingbyCurrentUser = currentUser.wishes_uploaded.filter(granted=False)

        context = {
            'all_wishes': Wish.objects.all(),
            'wishes_granted_by_current_user': wishesGrantedbyCurrentUser,
            'wishes_pending_by_current_user': wishesPendingbyCurrentUser,
        }
        return render(request,'user_stats.html', context)

    return redirect('/')

def removeWish(request,wish_id):

    #Check if an user is logged in:
    if 'name' in request.session:
        
        currentUser = User.objects.get(id=request.session['id'])
        
        # Handle wishes that doesn't exist if user looks them by the URL (when inserting an ID)
        try:
            wishSelected = currentUser.wishes_uploaded.get(id=wish_id)
            wishSelected.delete()
            return redirect('/wishes')
        except Wish.DoesNotExist:
            # Add Message Error - LASTING!
            return redirect('/wishes')
    
    return redirect('/wishes')

def editWish(request,wish_id):
    
    #Check if an user is logged in:
    if 'name' in request.session:
        
        currentUser = User.objects.get(id=request.session['id'])
        # Handle wishes that doesn't exist if user looks them by the URL (when inserting an ID)
        try:
            wishSelected = currentUser.wishes_uploaded.get(id=wish_id)
        except Wish.DoesNotExist:
            # Add Message Error - LASTING!
            return redirect('/wishes')

        if request.method == 'POST':

            # Check if the user want to submit or Cancel the operation:
            if 'cancel_operation' in request.POST:
                return redirect('/wishes')
            
            # If the user want to submit the operation, then:
            elif 'submit_operation' in request.POST:
                
                # Check if there are erros on the data submission
                errors = Wish.objects.validatorWish(request.POST)
                if len(errors)>0:
                    for key, value in errors.items():
                        messages.error(request, value)
                    return redirect(f'/wishes/edit_wish/{str(wish_id)}')

                # If not errors are found, then create the wish
                wishSelected.item = request.POST['item']
                wishSelected.description = request.POST['description']
                wishSelected.save()
                return redirect('/wishes')

        context = {
                'wish_selected': wishSelected,
            }

        return render(request,'edit_wish.html', context)
    
    return redirect('/')


def grantWish(request,wish_id):

    #Check if an user is logged in:
    if 'name' in request.session:

        currentUser = User.objects.get(id=request.session['id'])
        
        # Handle wishes that doesn't exist or does not belong to him if user looks them by the URL (when inserting an ID)
        try:
            wishSelected = currentUser.wishes_uploaded.get(id=wish_id)
            wishSelected.granted = True
            wishSelected.save()
            return redirect('/wishes')
        except Wish.DoesNotExist:
            # Add Message Error - LASTING!
            return redirect('/wishes')

    return redirect('/wishes')

def likeWish(request,wish_id):

    #Check if an user is logged in:
    if 'name' in request.session:

        currentUser = User.objects.get(id=request.session['id'])
        wishesFromOtherUsers = Wish.objects.exclude(uploaded_by=currentUser)
        
        # Handle wishes that doesn't exist or does not belong to him if user looks them by the URL (when inserting an ID)
        try:
            wishSelected = wishesFromOtherUsers.get(id=wish_id)
            currentUser.liked_wishes.add(wishSelected)
            return redirect('/wishes')
        except Wish.DoesNotExist:
            # Add Message Error - LASTING!
            return redirect('/wishes')
    
    return redirect('/wishes')