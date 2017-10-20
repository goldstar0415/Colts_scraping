from hashtags.models import HashTag


def get_dict_with_objects_for_network(func, user_pk, user_networks):
    dictionary = dict()
    for network in user_networks:
        dictionary[network.name] = func(user_pk, network)
    return dictionary


def fetch_hashtags(user_pk, network_name):
    return HashTag.objects.filter(user__pk=user_pk, network__name=network_name)
