from django.shortcuts import render
import json
from django.core import serializers
from .models import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.db.models import Count
import re
#from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
from sklearn.cluster import KMeans

@never_cache
# Create your views here.
###############LOGIN & REGISTRATION START
def display_login(request):
    return render(request, "login.html", {})


def show_register(request):
    return render(request, "register.html", {})

@never_cache
def logout(request):
    if 'uid' in request.session:
        del request.session['uid']
    return render(request,'login.html')


def register(request):
	
	username = request.GET.get("uname")
	phone = request.GET.get("phone")
	email_id=request.GET.get("email_id")
	password = request.GET.get("pass")
	age=request.GET.get("age")
	gender=request.GET.get("gender")

	a = Users.objects.filter(username=username)
	print("a:>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",a)
	c = a.count()
	print(c)
	if(c == 1):
	    return HttpResponse("[INFO]: Username is already Taken, Choose another one")
	else:
		if re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$',email_id):
		    b = Users(username=username, phone=phone, email_id=email_id,password=password,age=age,gender=gender)
		    b.save()
		    return HttpResponse("Successfully Registered")
		else:
			return HttpResponse("Try valid email id")


def check_login(request):
	username = request.GET.get("uname")
	password = request.GET.get("password")

	print(username)
	print(password)

	if username == 'admin' and password == 'admin':
		request.session["uid"] = "admin"
		return HttpResponse("Admin Login Successful")
	else:
	    d = Users.objects.filter(username=username, password=password)
	    c = d.count()
	    if c == 1:
	        d2 = Users.objects.get(username=username, password=password)
	        request.session["uid"] = d2.u_id
	        return HttpResponse("Login Successful")
	    else:
	        return HttpResponse("Invalid")

###############LOGIN & REGISTRATION END

@never_cache
###############ADMIN START
def show_home_admin(request):
	if 'uid' in request.session:
		print(request.session['uid'])
		return render(request,'home_admin.html') 
	else:
		return render(request,'login.html')

@never_cache
def view_users_admin(request):
	if 'uid' in request.session:
		users_list=Users.objects.all()

		return render(request,"view_users_admin.html",{'usr':users_list,})
	else:
		return render(request,'login.html') 

def delete(request):
	get_user_id=request.POST.get("u_id")
	f = Users.objects.get(u_id=get_user_id)
	f.delete()
	return HttpResponse("<script>alert('Deleted Successfully');window.location.href='/view_users_admin/'</script>")

@never_cache
def display_add_mobile_admin(request):
	if 'uid' in request.session:
		return render(request,"add_mobile_admin.html",{})
	else:
		return render(request,'login.html')

def add_mobile(request):
	mobile_name=request.POST.get("mname")
	ram=request.POST.get("ram")
	rom=request.POST.get("rom")
	camera=request.POST.get("camera")
	size=request.POST.get("size")
	battery=request.POST.get("battery")
	rating=request.POST.get("rating")
	price=request.POST.get("price")
	picture=request.FILES["picture"]

	print(mobile_name)
	print(ram)
	print(rom)
	print(camera)
	print(size)
	print(battery)
	print(rating)
	print(price)
	print(picture)


	fs1=FileSystemStorage("mob_app/static/mobile_images")
	fs1.save(picture.name,picture)

	obj1=Mobiles(mobile_name=mobile_name,ram=ram,rom=rom,camera=camera,size=size,battery=battery,rating=rating,price=price,picture=picture)
	obj1.save()

	return HttpResponse("<script>alert('Successfully Added');window.location.href='/show_view_mobile_admin/'</script>")     

@never_cache
def show_view_mobile_admin(request):
	if 'uid' in request.session:
		mobiles_list=Mobiles.objects.all()
		#print(mobiles_list)

		return render(request,"view_mobile_admin.html",{"mob":mobiles_list,})
	else:
		return render(request,'login.html')

def mobile_delete(request):
	get_mobile_id=request.POST.get("m_id")
	f = Mobiles.objects.get(m_id=get_mobile_id)
	f.delete()
	return HttpResponse("<script>alert('Deleted Successfully');window.location.href='/show_view_mobile_admin/'</script>")

#############ADMIN END

################USER START
@never_cache
def show_home_user(request):
	if 'uid' in request.session:
		print(request.session['uid'])
		return render(request,'home_user.html') 
	else:
		return render(request,'login.html') 

@never_cache
def display_find_my_mobile_user(request):
	if 'uid' in request.session:
		return render(request,'find_my_mobile_user.html') 
	else:
		return render(request,'login.html')

# @never_cache
def display_similiar_phones_user(request):
	if 'uid' in request.session:
		return render(request,'display_similiar_phones_user.html') 
	else:
		return render(request,'login.html')

def find_mobile(request):

	ram=request.GET.get("ram")
	rom=request.GET.get("rom")
	camera=request.GET.get("camera")
	size=request.GET.get("size")
	battery=request.GET.get("battery")
	rating=request.GET.get("rating")
	price=request.GET.get("price")

	keys=['ram','rom','camera','size','battery','rating','price']
	values=[ram,rom,camera,size,battery,rating,price]

	dictionary = dict(zip(keys, values))
	print("dictionary : ",dictionary)

	userdf=pd.DataFrame(dictionary,index=[0])
	print("Userdf : ",userdf)

	items = Mobiles.objects.all().values()
	df = pd.DataFrame(items)
	#print("Fullmobile list :",df)

	df=userdf.append(df,ignore_index=True)
	print("final df : ",df)

	#create a new column , which have all values
	def combineFeatures(row):
		return str(row['ram'])+" "+str(row['rom'])+" "+str(row['camera'])+" "+str(row['size'])+" "+str(row['battery'])+" "+str(row['rating'])+" "+str(row['price'])
	# this will create a seperate colm of combined features
	df["combinedFeatures"]=df.apply(combineFeatures,axis=1)
	print(df)

	# create an object of countVectorizer
	cv=CountVectorizer()
	countMatrix=cv.fit_transform(df['combinedFeatures'])
	# print (countMatrix).toarray()
	similar=cosine_similarity(countMatrix)
	similarPhones=list(enumerate(similar[0]))
	print("similar phones :",similarPhones)
	print(len(similarPhones))
	#Now sort the entries acc to similarity scores
	sortedSimilarPhones=sorted(similarPhones,key=lambda x:x[1], reverse=True)
	print("sortedSimilarPhones :",sortedSimilarPhones)

	final_dict={}
	final_list=[]
	k=0
	for phone in sortedSimilarPhones[1:]:
		if (df[df.index==phone[0]]['mobile_name'].values[0]=='NaN'):
		    pass
		else:
			temp_list=[]
			  # final_dict[k]={
		    # 'm_id':str(df[df.index==phone[0]]['m_id'].values[0]),
		    # 'mobile_name':str(df[df.index==phone[0]]['mobile_name'].values[0]),
		    # 'ram':str(df[df.index==phone[0]]['ram'].values[0]),
		    # 'rom':str(df[df.index==phone[0]]['rom'].values[0]),
		    # 'camera':str(df[df.index==phone[0]]['camera'].values[0]),
		    # 'size':str(df[df.index==phone[0]]['size'].values[0]),
		    # 'battery':str(df[df.index==phone[0]]['battery'].values[0]),
		    # 'rating':str(df[df.index==phone[0]]['rating'].values[0]), 
		    # 'price':str(df[df.index==phone[0]]['price'].values[0]),
		    # 'picture':df[df.index==phone[0]]['picture'].values[0],    
		    # }
		  
			v1=str(df[df.index==phone[0]]['m_id'].values[0])
			v2=str(df[df.index==phone[0]]['mobile_name'].values[0])
			v3=str(df[df.index==phone[0]]['ram'].values[0])
			v4=str(df[df.index==phone[0]]['rom'].values[0])
			v5=str(df[df.index==phone[0]]['camera'].values[0])
			v6=str(df[df.index==phone[0]]['size'].values[0])
			v7=str(df[df.index==phone[0]]['battery'].values[0])
			v8=str(df[df.index==phone[0]]['rating'].values[0])
			v9=str(df[df.index==phone[0]]['price'].values[0])
			v10=df[df.index==phone[0]]['picture'].values[0]
			temp_list.append(v1)
			temp_list.append(v2)
			temp_list.append(v3)
			temp_list.append(v4)
			temp_list.append(v5)
			temp_list.append(v6)
			temp_list.append(v7)
			temp_list.append(v8)
			temp_list.append(v9)
			temp_list.append(v10)
			final_list.append(temp_list)

			k=k+1
			if(k==6):
				break
	print("**********************************")
	print("FINAL LIST : ",final_list)

	#return render(request,"display_similiar_phones_user.html",{"s_phone":final_dict,})
	return JsonResponse(final_list,safe=False)

def purchase_mobile(request):
	m_id=float(request.POST.get("m_id"))
	e = Mobiles.objects.get(m_id=int(m_id))
	mobile_name=e.mobile_name
	print("Purchased Mobile Name :",mobile_name)

	user_id=request.session["uid"]
	print("User id :",user_id)
	rating=''
	review=''
	obj1=Purchase(u_id=user_id,mobile_name=mobile_name,rating=rating,review=review)
	obj1.save()

	return HttpResponse("<script>alert('Product Purchased Successfully');window.location.href='/show_home_user/'</script>")


@never_cache
def show_give_rating_user(request):
	if 'uid' in request.session:
		user_id=request.session['uid']
		purchase_users_list=Purchase.objects.values_list('u_id', flat=True)
		#print('purchase_users_list :',purchase_users_list)
		if user_id in purchase_users_list:
			return render(request,'give_rating_user.html')
		else:
			return HttpResponse("<script>alert('You Should Purchase any Product before give Rating');window.location.href='/show_home_user/'</script>")
	else:
		return render(request,'login.html')

def display_mobile_list(request):
	d = Mobiles.objects.all()
	dic = {}
	if d:
	    value = serializers.serialize("json", d)
	    dic["key"] = json.loads(value)
	    return JsonResponse(dic, safe=False)
	else:
	    return HttpResponse("No Mobiles available")

def add_rating(request):
	mobile_name=request.GET.get("mobile_name")
	rating=request.GET.get("rating")
	review=request.GET.get("review")

	# print("mobile_name :",mobile_name)
	# print(rating)
	# print(review)

	user_id=request.session['uid']
	# print("user_id :",user_id)

	obj1 = Purchase.objects.filter(u_id=user_id,mobile_name=mobile_name) 
	c = obj1.count()
	print("C : ",c)
	if(c == 0):
	    return HttpResponse("[INFO]: You didnt Purchase this Mobile Yet")
	else:
		obj2 = Purchase.objects.get(u_id=user_id,mobile_name=mobile_name)
		print("obj2 : ",obj2)
		obj2.rating = rating
		obj2.review=review
		obj2.save()

		return HttpResponse("Rating added Successfully")

@never_cache
def view_recommendations_user(request):
	if 'uid' in request.session:
		return render(request,'view_recommendations_user.html')
		
	else:
		return render(request,'login.html')

def get_recommendations(request):

	my_user_df=pd.DataFrame(list(Users.objects.all().values()))
	#print(my_user_df)
	my_user_df['gender']=my_user_df['gender'].replace("Male",1)
	my_user_df['gender']=my_user_df['gender'].replace("Female",0)

	x=my_user_df[["age","gender"]]

	#performing kmeans clustering
	km1=KMeans(n_clusters=4)
	#Fitting the input data
	km1.fit(x)
	#predicting the labels of the input data
	y=km1.predict(x)
	#adding the labels to a column named label
	my_user_df["label"] = y
	#The new dataframe with the clustering done
	#print(my_user_df)

	my_u_id=request.session['uid']

	current_user_label=my_user_df.loc[my_user_df['u_id']==my_u_id,'label'].item()

	new_df=my_user_df[my_user_df['label']==current_user_label]

	get_u_id_from_new_df= new_df['u_id'].tolist()

	get_u_id_from_new_df.remove(my_u_id)

	mobile_names=[]
	for i in get_u_id_from_new_df:
		try:
			obj10= Purchase.objects.get(u_id=i,rating='High')
			mobile_name=obj10.mobile_name
			mobile_names.append(mobile_name)
		except:
			continue

	if((mobile_names==[]) or ((len(mobile_names))<3)) :
		return HttpResponse("There is no Recommendations For You")
	else:
		random.shuffle(mobile_names)

		final_list=[]
		c=0
		for k in mobile_names:
			temp_list=[]
			mobile_name=k
			obj1=Mobiles.objects.get(mobile_name=mobile_name)
			m_id=obj1.m_id
			ram=obj1.ram
			rom=obj1.rom
			camera=obj1.camera
			size=obj1.size
			battery=obj1.battery
			rating=obj1.rating
			price=obj1.price
			picture=obj1.picture

			temp_list.append(m_id)
			temp_list.append(mobile_name)
			temp_list.append(ram)
			temp_list.append(rom)
			temp_list.append(camera)
			temp_list.append(size)
			temp_list.append(battery)
			temp_list.append(rating)
			temp_list.append(price)
			temp_list.append(picture)

			final_list.append(temp_list)
			c+=1
			if(c==3):
				break


		return JsonResponse(final_list,safe=False)















































































###################################old start
	# df1 = pd.DataFrame(list(Purchase.objects.filter(review='Good Product',rating='High').values()))
	# if df1.empty:
	# 	return HttpResponse("There is no Recommendations For You")
	# else:
	# 	list_of_mobiles = df1['mobile_name'].tolist()
	# 	random.shuffle(list_of_mobiles)

	# 	final_list=[]
	# 	c=0
	# 	for k in list_of_mobiles:
	# 		temp_list=[]
	# 		mobile_name=k
	# 		obj1=Mobiles.objects.get(mobile_name=mobile_name)
	# 		m_id=obj1.m_id
	# 		ram=obj1.ram
	# 		rom=obj1.rom
	# 		camera=obj1.camera
	# 		size=obj1.size
	# 		battery=obj1.battery
	# 		rating=obj1.rating
	# 		price=obj1.price
	# 		picture=obj1.picture

	# 		temp_list.append(m_id)
	# 		temp_list.append(mobile_name)
	# 		temp_list.append(ram)
	# 		temp_list.append(rom)
	# 		temp_list.append(camera)
	# 		temp_list.append(size)
	# 		temp_list.append(battery)
	# 		temp_list.append(rating)
	# 		temp_list.append(price)
	# 		temp_list.append(picture)

	# 		final_list.append(temp_list)
	# 		c+=1
	# 		if(c==3):
	# 			break


	# 	return JsonResponse(final_list,safe=False)
################################old end

#################USER END
