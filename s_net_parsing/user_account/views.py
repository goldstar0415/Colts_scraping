from pymongo import MongoClient

from django.core.exceptions import MultipleObjectsReturned
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaulttags import register
from django.template import loader

from hashtags.models import HashTag
from hashtag_network.models import HashTagNetwork
from social_parsing.models import Network
from user_account.models import SimpleUsers
from user_account.forms import HashtagAddingForm, HashtagEditingForm, UserEditForm


mongo = MongoClient(settings.MONGO_URL)
db = mongo.get_default_database()


def get_mongo_connector(collection_name=settings.POSTS_COLLECTION_NAME):
    return db[collection_name]


def user_account_page(request):
    template = loader.get_template('bootstrapous/user_acc.html')
    user = request.user
    hashtags = get_user_hashtags(user.pk)
    allowed_networks = Network.objects.all().count()
    context = {'user': user,
               'allowed_networks': allowed_networks if allowed_networks else None,
               'user_networks': len(get_user_networks(user.pk)),
               'user_hashtags': len(hashtags),
               'mean_network_parsing_time': get_mean_parsing_time(),
               'ten_most_rated_hashtags': get_data_bar_chart(user.pk, hashtags),
               'date_posts': get_number_of_posts_for_tags_by_date(user.pk, hashtags),
               'total_posts_with_user_hashtags': get_total_posts_with_user_hashtags(user.pk, hashtags)
               }

    return HttpResponse(template.render(context, request))


def get_mean_parsing_time():
    parsing_time = Network.objects.all().values_list('parsing_frequency', flat=True)
    if not parsing_time:
        return None
    else:
        return int(sum(parsing_time) / len(parsing_time))


def get_user_hashtags(user_pk):
    return list(HashTag.objects.filter(user_id=user_pk).distinct().values_list('tag', flat=True))


def get_user_networks(user_pk):
    return list(HashTag.objects.filter(user_id=user_pk).distinct().values_list('networks__name', flat=True))


def get_data_bar_chart(user_pk, hashtags):
    posts_collection = get_mongo_connector(settings.POSTS_COLLECTION_NAME)

    most_rated_hashtags = posts_collection.aggregate([
        {"$match": {"hashtags": {"$in": hashtags}}},
        {"$project": {"hashtags": 1}},
        {"$unwind": {"path": '$hashtags'}},
        {"$group": {"_id": '$hashtags', "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    return list(most_rated_hashtags) if most_rated_hashtags else list()


def get_total_posts_with_user_hashtags(user_pk, hashtags):
    posts_collection = get_mongo_connector(settings.POSTS_COLLECTION_NAME)

    posts_num = posts_collection.aggregate([
        {'$match': {'hashtags': {'$in': hashtags}}},
        {'$group': {'_id': 'null', 'count': {'$sum': 1}}}])

    return list(posts_num)


def get_number_of_posts_for_tags_by_date(user_pk, hashtags):
    posts_collection = get_mongo_connector(settings.POSTS_COLLECTION_NAME)

    date_posts = posts_collection.aggregate([
                                  {"$match": {"hashtags": {"$in": hashtags}}},
                                  {"$group": {
                                      "_id": {"$add":
                                              [{"$dayOfYear": "$date_published"},
                                               {"$multiply": [400, {"$year": "$date_published"}]}]},
                                      "published": {"$sum": 1},
                                      "first": {"$min": "$date_published"}}},
                                  {"$sort": {"_id": -1}},
                                  {"$limit": 30},
                                  {"$project": {"date": "$first", "published": 1, "_id": 0}}])

    if not date_posts:
        date_posts = list()
    else:
        date_posts = sorted(list(date_posts), key=lambda x: x.get('date'))

    return date_posts


def edit_user_fields(request):
    user, _ = SimpleUsers.objects.get_or_create(user_id=request.user.id)

    if request.method == "POST":
        form = UserEditForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.avatar = form.cleaned_data['avatar']
            user.bio = form.cleaned_data['bio']
            user.country_name = form.cleaned_data['country_name']
            user.company = form.cleaned_data['company']
            user.birth_date = form.cleaned_data['birth_date']
            user.save()
            return redirect('user_account', )
        form = UserEditForm(data=request.POST, files=request.FILES, instance=user)
        return render(request, 'bootstrapous/user_edit_page.html', {'form': form})
    else:
        form = UserEditForm(instance=user)
        return render(request, 'bootstrapous/user_edit_page.html', {'form': form})


def hashtags(request, *args, **kwargs):
    template = loader.get_template('bootstrapous/hashtags.html')
    user_hashtags = HashTag.objects.filter(user_id=request.user).values_list('tag', 'guid').distinct('tag')
    hashtags_networks_dict = dict()
    for hashtag, guid in user_hashtags:
        hashtags_networks_dict[guid] = (hashtag, list(Network.objects.filter(hashtags__user_id=request.user,
                                                                             hashtags__tag=hashtag).values_list('name', flat=True)))

    context = {'user_hashtags': hashtags_networks_dict, }
    return HttpResponse(template.render(context, request))


def add_hashtag(request, *args, **kwargs):
    if request.method == "POST":
        form = HashtagAddingForm(request.POST)

        if form.is_valid():
            hashtag_networks = Network.objects.filter(hashtags__user_id=request.user,
                                                      hashtags__tag=form.cleaned_data['tag']).values_list('guid', flat=True)
            if not hashtag_networks:
                hashtag_networks = list()
            else:
                hashtag_networks = [str(network) for network in hashtag_networks]
            if form.cleaned_data['user'] == request.user:
                hashtag = form.save(commit=False)
                hashtag.networks.clear()
                hashtag.user = request.user
                hashtag.save()
                for network_value in form.cleaned_data['networks']:
                    if network_value not in hashtag_networks:
                        m2m_table = HashTagNetwork(hashtag=hashtag,
                                                   network=Network.objects.get(guid=network_value))
                        m2m_table.save()
                    else:
                        continue
            else:
                form = HashtagAddingForm(initial={'networks': [network.guid for network in Network.objects.all()],
                                                  'user': request.user, })
                return render(request, 'bootstrapous/add_hashtag.html',
                              {'form': form}, )
        return redirect('hashtags', )
    else:
        form = HashtagAddingForm(initial={'networks': [network.guid for network in Network.objects.all()],
                                          'user': request.user, })
        return render(request, 'bootstrapous/add_hashtag.html',
                      {'form': form}, )


def edit_hashtag(request, pk):
    hashtag = get_object_or_404(HashTag, pk=pk)

    if request.method == "POST":
        form = HashtagEditingForm(request.POST, instance=hashtag)

        if request.POST.get('networks') is None:
            try:
                hashtag = HashTag.objects.get(user=request.user, tag=request.POST.get('tag'))
                hashtag.delete()
            except (MultipleObjectsReturned):
                return redirect('hashtags', )
        else:
            if form.is_valid():
                hashtag = form.save(commit=False)
                hashtag.networks.clear()
                hashtag.user = request.user
                hashtag.save()
                for network_value in form.cleaned_data['networks']:
                    m2m_table = HashTagNetwork(hashtag=hashtag,
                                               network=Network.objects.get(guid=network_value))
                    m2m_table.save()
                return redirect('hashtags', )
            form = HashtagEditingForm(request.POST, instance=hashtag, )
            return render(request, 'bootstrapous/edit_hashtags.html',
                          {'form': form, }, )
        return redirect('hashtags', )
    else:
        hashtag_networks = Network.objects.filter(hashtags__user_id=request.user,
                                                  hashtags=hashtag)
        form = HashtagEditingForm(instance=hashtag, initial={'networks': [network.guid for network in hashtag_networks],
                                                             'user': request.user, })
        return render(request, 'bootstrapous/edit_hashtags.html',
                      {'form': form, }, )


def delete_hashtag(request, pk):
    hashtag = get_object_or_404(HashTag, pk=pk)
    hashtag.delete()
    return redirect('hashtags', )


def posts(request):
    template = loader.get_template('bootstrapous/posts.html')
    user_networks = Network.objects.all()
    hashtags = HashTag.objects.filter(user_id=request.user.pk).distinct().values_list('tag', flat=True)

    posts_collection = get_mongo_connector(settings.POSTS_COLLECTION_NAME)

    posts = posts_collection.find({'hashtags': {'$in': list(hashtags)}}).sort([('date_published', -1)]).limit(10)
    context = {'posts': list(posts),
               'user_networks': user_networks}
    return HttpResponse(template.render(context, request))


def posts_raw(request):
    template = loader.get_template('bootstrapous/posts_items.html')
    if request.GET.get('networks'):
        user_networks = Network.objects.filter(guid__in=request.GET.get('networks').split(','))
    else:
        user_networks = Network.objects

    hashtags = list(HashTag.objects.filter(user_id=request.user.pk).filter(networks__guid__in=list(Network.objects.values_list('guid', flat=True))).distinct().values_list('tag', flat=True))

    posts_collection = get_mongo_connector(settings.POSTS_COLLECTION_NAME)

    try:
        limit = int(request.GET.get('limit', 10))
    except TypeError:
        limit = 10

    try:
        offset = int(request.GET.get('offset', 0))
    except TypeError:
        offset = 0

    posts = posts_collection.aggregate([
        {'$match': {'network': {'$in': list(user_networks.values_list('name', flat=True))}}},
        {'$lookup':
            {
                'from': settings.AUTHORS_COLLECTION_NAME,
                'localField': "author_id",
                'foreignField': "_id",
                'as': "author"
            }
        },
        {'$sort': {'date_published': -1}},
        {'$skip': offset},
        {'$limit': limit}
    ])

    context = {'posts': list(posts),
               'user_networks': user_networks.all(),
               'hashtags': hashtags}
    return HttpResponse(template.render(context, request))


def posts_likes(request):
    template = loader.get_template('bootstrapous/posts_likes.html')
    user = request.user
    hashtags = get_user_hashtags(user.pk)

    posts_collection = get_mongo_connector(settings.POSTS_COLLECTION_NAME)

    if not hashtags:
        posts_likes = list()
    else:
        posts_likes = posts_collection.aggregate([
            {'$match': {'hashtags': {'$in': hashtags}}},
            {'$lookup':
                {
                    'from': settings.AUTHORS_COLLECTION_NAME,
                    'localField': "author_id",
                    'foreignField': "_id",
                    'as': "author"
                }
            },
            {'$sort': {'likes': -1}},
            {'$limit': settings.TOP_POSTS_LIKES_LIMIT}
        ])

    context = {'posts_likes': posts_likes, }

    return HttpResponse(template.render(context, request))


def posts_shares(request):
    template = loader.get_template('bootstrapous/posts_shares.html')
    user = request.user
    hashtags = get_user_hashtags(user.pk)

    posts_collection = get_mongo_connector(settings.POSTS_COLLECTION_NAME)

    if not hashtags:
        posts_shares = list()
    else:
        posts_shares = posts_collection.aggregate([
            {'$match': {'hashtags': {'$in': hashtags}}},
            {'$lookup':
                {
                    'from': settings.AUTHORS_COLLECTION_NAME,
                    'localField': "author_id",
                    'foreignField': "_id",
                    'as': "author"
                }
            },
            {'$sort': {'shares': -1}},
            {'$limit': settings.TOP_POSTS_SHARES_LIMIT}
        ])

    context = {'posts_shares': posts_shares, }

    return HttpResponse(template.render(context, request))


def posts_recent(request):
    template = loader.get_template('bootstrapous/posts_recent.html')
    user = request.user
    hashtags = get_user_hashtags(user.pk)

    posts_collection = get_mongo_connector(settings.POSTS_COLLECTION_NAME)

    if not hashtags:
        posts_recent = list()
    else:
        posts_recent = posts_collection.aggregate([
            {'$match': {'hashtags': {'$in': hashtags}}},
            {'$lookup':
                {
                    'from': settings.AUTHORS_COLLECTION_NAME,
                    'localField': "author_id",
                    'foreignField': "_id",
                    'as': "author"
                }
            },
            {'$sort': {'date_published': -1}},
            {'$limit': settings.TOP_MOST_RECENT_POSTS_LIMIT}
        ])

    context = {'posts_recent': posts_recent, }

    return HttpResponse(template.render(context, request))


def top_post_likes(request):
    template = loader.get_template('bootstrapous/top-post-likes-count.html')
    user = request.user
    hashtags = get_user_hashtags(user.pk)

    posts_collection = get_mongo_connector(settings.POSTS_COLLECTION_NAME)

    if not hashtags:
        top_post_likes_count = list()
    else:
        top_post_likes_count = posts_collection.find({}, {'likes': 1}).sort([('likes', -1), ]).limit(1)

    context = {'top_post_likes_count': top_post_likes_count, }
    return HttpResponse(template.render(context, request))


def top_post_shares(request):
    template = loader.get_template('bootstrapous/top-post-shares-count.html')
    user = request.user
    hashtags = get_user_hashtags(user.pk)

    posts_collection = get_mongo_connector(settings.POSTS_COLLECTION_NAME)

    if not hashtags:
        top_post_shares_count = list()
    else:
        top_post_shares_count = posts_collection.find({}, {'shares': 1}).sort([('shares', -1), ]).limit(1)

    context = {'top_post_shares_count': top_post_shares_count, }
    return HttpResponse(template.render(context, request))


def help(request):
    template = loader.get_template('instructions.html')
    context = {'phrase': "Please, do not break anything.", }
    return HttpResponse(template.render(context, request))


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_string(list_element):
    return str(list_element.get('_id'))


@register.filter
def get_number(list_element):
    return list_element.get('count')


@register.filter
def get_date(dict_obj):
    date = dict_obj.get('date')
    return str(date.strftime('%d/%m') if date else None)


@register.filter
def get_number_published(dict_obj):
    published = dict_obj.get('published')
    return published if published else 0
