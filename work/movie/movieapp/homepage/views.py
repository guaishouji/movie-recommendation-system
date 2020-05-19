from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Movie, Users, Genres, Rating, Recommend
from .myforms import UserForm, RegisterForm
import hashlib, math, decimal
import pandas as pd
# Create your views here.


def homepages(request):
    most_pop_list = Movie.objects.order_by('-pop')[:1000]
    context = filter_movie(most_pop_list)
    return render(request, 'homepage/homepages.html', context)


def filter_movie(pop_list):
    drama_list = []
    comedy_list = []
    thriller_list = []
    romance_list = []
    adventure_list = []
    crime_list = []
    fantasy_list = []
    for movie in pop_list:
        # movie_genres = Genres.objects.filter(movie_id=movie.movie_id)
        movie_dic = dict()
        movie_dic['movie_id'] = movie.movie_id
        movie_dic['movie_title'] = movie.movie_title
        movie_dic['movie_imdbId'] = movie.movie_imdbId
        movie_dic['movie_img'] = movie.movie_img
        movie_dic['rating'] = movie.movie_rating
        movie_genres = Genres.objects.filter(movie_id=movie.movie_id)
        for genre in movie_genres:
            if genre.movie_genres == 'Drama' and len(drama_list) < 12:
                drama_list.append(movie_dic)
                break
            elif genre.movie_genres == 'Comedy' and len(comedy_list) < 12:
                comedy_list.append(movie_dic)
                break
            elif genre.movie_genres == 'Thriller' and len(thriller_list) < 12:
                thriller_list.append(movie_dic)
                break
            elif genre.movie_genres == 'Romance' and len(romance_list) < 12:
                romance_list.append(movie_dic)
                break
            elif genre.movie_genres == 'Adventure' and len(adventure_list) < 12:
                adventure_list.append(movie_dic)
                break
            elif genre.movie_genres == 'Crime' and len(crime_list) < 12:
                crime_list.append(movie_dic)
                break
            elif genre.movie_genres == 'Fantasy' and len(fantasy_list) < 12:
                fantasy_list.append(movie_dic)
                break
            else:
                continue
        if len(drama_list) >= 12 and len(comedy_list) >= 12 and len(thriller_list) >= 12 and len(romance_list) >= 12 and len(adventure_list) >= 12 and len(comedy_list) >= 12 and len(fantasy_list) >= 12:
            context = {'drama_list': drama_list, 'comedy_list': comedy_list, 'thriller_list': thriller_list,
                       'romance_list': romance_list, 'adventure_list': adventure_list, 'crime_list': crime_list,
                       'fantasy_list': fantasy_list, 'count': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]}
            break
    return context


def rating(request):
    if request.session.get('is_login', None):
        if request.method == "GET":
            user_id = int(request.GET.get('user_id'))
            movie_imdbId = str(request.GET.get('movie_imdbId'))
            movie = Movie.objects.get(movie_imdbId=movie_imdbId)
            movie_id = movie.movie_id
            movie_rating = float(request.GET.get('rating'))
            try:  # get_or_create
                re_rating=Rating.objects.get(user_id=user_id, movie_id=movie_id)
                Rating.objects.filter(user_id=user_id, movie_id=movie_id).update(movie_rating=movie_rating)
                print("更改评分")
            except:
                new_rating = Rating.objects.create(user_id=user_id, movie_id=movie_id, movie_imdbId=movie_imdbId, movie_rating=movie_rating)
                new_rating.save()
                print("创建评分")
            watched = Rating.objects.filter(user_id=user_id).order_by("-id")[:10]
            watched_list = list()
            for movie in watched:
                d = dict()
                d['movie_imdbId'] = movie.movie_imdbId
                movie_img = Movie.objects.get(movie_id=movie.movie_id).movie_img
                d['movie_img'] = movie_img
                movie_title = Movie.objects.get(movie_id=movie.movie_id).movie_title
                d['movie_title'] = movie_title
                watched_list.append(d)
            if len(watched_list) < 10:
                recommend_list = []
            else:
                recommend_list = Recommend.objects.filter(user_id=user_id).order_by("-id")[:5]
            try:
                Recommend.objects.filter(user_id=user_id, movie_id=movie_id).delete()
                return render(request, 'homepage/index.html', locals())
            except:
                return render(request, 'homepage/index.html', locals())
    return render(request, 'homepage/', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect('/homepage/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = Users.objects.get(username=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.user_id
                    request.session['user_name'] = user.username
                    return redirect('/homepage/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'homepage/login.html', locals())
    login_form = UserForm()
    return render(request, 'homepage/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/homepage/')
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = '请检查填写的内容！'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            # gender = register_form.cleaned_data['gender']
            if password1 != password2:
                message = "两次输入的密码不同！"
                return render(request, 'homepage/register.html', locals())
            else:
                same_name_user = Users.objects.filter(username=username)
                if same_name_user:
                    message = '用户已经存在，请重新输入用户名!'
                    return render(request, 'homepage/register.html', locals())
                same_email_user = Users.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'homepage/register.html', locals())
                new_user = Users.objects.create()
                new_user.username = username
                new_user.password = hash_code(password1)
                new_user.email = email
                # new_user.gender = gender
                new_user.save()
                return redirect('/homepage/login/')
    register_form = RegisterForm()
    return render(request, 'homepage/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/homepage/')
    request.session.flush()
    return redirect('/homepage/')


def hash_code(s, salt='movies'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def index(request, user_id):
    if request.session.get('is_login', None):
        pk = request.session.get('user_id', None)
        if pk == user_id:
            try:
                rating_list = Rating.objects.filter(user_id=user_id)
                if len(rating_list) < 10:
                    print("进入")
                    watched = Rating.objects.filter(user_id=user_id).order_by("-id")[:10]
                    watched_list = list()
                    for movie in watched:
                        d = dict()
                        d['movie_imdbId'] = movie.movie_imdbId
                        movie_img = Movie.objects.get(movie_id=movie.movie_id).movie_img
                        d['movie_img'] = movie_img
                        movie_title = Movie.objects.get(movie_id=movie.movie_id).movie_title
                        d['movie_title'] = movie_title
                        watched_list.append(d)
                    return render(request, 'homepage/index.html', locals())
                rank = update_matrix(user_id)
                for movie_id, like in rank.items():
                    if len(Recommend.objects.filter(user_id=user_id)) < 15:
                        try:
                            Recommend.objects.get(user_id=user_id, movie_id=movie_id)
                            continue
                        except:
                            movie_imdbId = Movie.objects.get(movie_id=movie_id).movie_imdbId
                            movie_title = Movie.objects.get(movie_id=movie_id).movie_title
                            movie_img = Movie.objects.get(movie_id=movie_id).movie_img
                            recommend_movie = Recommend.objects.create(user_id=user_id, movie_id=movie_id, movie_imdbId=movie_imdbId, movie_title=movie_title, movie_img=movie_img)
                            recommend_movie.save()
                    else:
                        break
                recommend_list = Recommend.objects.filter(user_id=user_id).order_by("-id")[:5]
                watched = Rating.objects.filter(user_id=user_id).order_by("-id")[:10]
                watched_list = list()
                for movie in watched:
                    d = dict()
                    d['movie_imdbId'] = movie.movie_imdbId
                    movie_img = Movie.objects.get(movie_id=movie.movie_id).movie_img
                    d['movie_img'] = movie_img
                    movie_title = Movie.objects.get(movie_id=movie.movie_id).movie_title
                    d['movie_title'] = movie_title
                    watched_list.append(d)
                return render(request, 'homepage/index.html', locals())
            except:
                return redirect('/homepage/')
        else:
            return redirect('/homepage/')  # 没登录返回原界面
    else:
        pass
        return redirect('/homepage/')


def update_matrix(user_id):
    similar_matrix = pd.read_table(r'C:\Users\asus\Desktop\work\movie\movieapp\homepage\data\similar_matrix.csv',
                                    sep =',', header=0, engine='python')  # {user:{v_user,like}}
    rating_table = get_rating_all()
    similar_matrix.rename(columns={'Unnamed: 0': 'index'}, inplace=True)
    similar_matrix.set_index(["index"], inplace=True)
    if user_id in similar_matrix.index:
        print("直接推荐")
        similar_matrix = similar_matrix.to_dict(orient="dict")
        similar_matrix1 = dict()
        for user, item in similar_matrix.items():
            similar_matrix1[user] = {}
            for v_user, like in item.items():
                if str(like) != 'nan':
                    similar_matrix1[user][v_user] = like
        rank = get_recommendation(user_id, rating_table, similar_matrix1, 40, 5)  # rank:{item:like}
        print("获得推荐")
        return rank
    else:
        print("更新用户相似矩阵")
        similar_matrix = user_similarity(rating_table)
        rank = get_recommendation(user_id, rating_table, similar_matrix, 40, 5)  # rank:{item:like}
    return rank


def get_rating_all():       # 获得集合
    rating_all = Rating.objects.all()      # [['user_id':user_id,'movie_id':movie_id],'movie_rating':movie_rating]]
    rating_table = dict()
    for item in rating_all:
        if item.user_id not in rating_table:
            rating_table[item.user_id] = {}
        rating_table[item.user_id][item.movie_id] = float(item.movie_rating)
    return rating_table


def user_similarity(rating_table):     # {user:{items,rating}}
    movie_users = dict()
    for user, movies in rating_table.items():  # {item:[user]}
        for movie in movies:
            if movie not in movie_users:
                movie_users[movie] = set()
            movie_users[movie].add(user)
    cov = dict()
    num = dict()
    for movies, users in movie_users.items(): # {item:[user]}
        for user in users:
            if user not in num:
                num[user] = 0
            num[user] += 1
            for v_user in users:
                if user == v_user:
                    continue
                elif user not in cov:
                    cov[user] = {}
                if v_user not in cov[user]:
                    cov[user][v_user] = 0
                cov[user][v_user] += 1/math.log(1+len(users))
    similar_matrix = dict()
    for user, related_users in cov.items():
        for v_user, cuv in related_users.items():
            if user not in similar_matrix:
                similar_matrix[user] = {}
            elif v_user not in similar_matrix[user]:
                similar_matrix[user][v_user] = 0
            similar_matrix[user][v_user] = cuv / math.sqrt(num[user] * num[v_user])
    pd.DataFrame(similar_matrix).to_csv(r'C:\Users\asus\Desktop\work\movie\movieapp\homepage\data\similar_matrix.csv')
    return similar_matrix


def get_recommendation(user, rating_table, similar_matrix, k, n):
    rank = dict()    # 对推荐物品兴趣度评分user:{item:[like,times]}
    connect_movies = rating_table[user]  # {user:{items,raing}}
    for v_user, wuv in sorted(similar_matrix[str(user)].items(), key=lambda item: (item[1], item[0]), reverse=True)[0:k]:  # (user,like) K=40
        for movie, rvi in rating_table[v_user].items():   # {user:{item:rating}}
            if movie in connect_movies:
                continue
            elif movie not in rank:
                rank[movie] = [0, 0]
            rank[movie][0] += wuv*float(rvi)
            rank[movie][1] = Movie.objects.get(movie_id=movie).pop
    rank = sorted(rank.items(), key=lambda item: (item[1][0], item[1][1]), reverse=True)[:n]    #A=5
    rank_sort = {}
    for item1, item2 in rank:
        rank_sort[item1] = item2[0]
    return rank_sort   # rank1{item:like}
