import math
from datetime import date, timedelta, datetime
from pprint import pprint
from environs import Env

from utils import handle_request


FILTER_PERIOD_IN_DAYS = 14


def calculate_pages_amount(items_amount):
    return math.ceil(items_amount / 100)


def get_group_id(groupname):
    url = 'https://api.vk.com/method/groups.getById'

    payload = {
        'group_id' : groupname,
        'access_token': vk_service_key,
        'v': '5.126'
    }

    response = handle_request(url, payload)

    return -response['response'][0]['id']


def paginate_vk_entities(url, payload, pages_amount):
    paginate_items = []

    for page_number in range(1, pages_amount):

        payload['offset'] = 100 * page_number
        response = handle_request(url, payload)

        paginate_items += response['response']['items']

    return paginate_items


def get_vk_posts(pages_amount=0):
    url = 'https://api.vk.com/method/wall.get'

    payload = {
        'domain': 'cocacola',
        'filter': 'owner',
        'offset': 0,
        'count': 100,
        'access_token': vk_service_key,
        'v': '5.126'
    }

    response = handle_request(url, payload)
    posts = response['response']['items']

    if pages_amount == 0:
        pages_amount = calculate_pages_amount(response['response']['count'])

    posts += paginate_vk_entities(url, payload, pages_amount)

    return posts


def get_post_comments(post_id, pages_amount=0):
    url = 'https://api.vk.com/method/wall.getComments'

    payload = {
        'owner_id': target_group_id,
        'post_id': post_id,
        'offset': 0,
        'count': 100,
        'sort': 'desc',
        'access_token': vk_service_key,
        'v': '5.126'
    }

    response = handle_request(url, payload)
    comments = response['response']['items']

    if pages_amount == 0:
        pages_amount = calculate_pages_amount(response['response']['count'])

    comments += paginate_vk_entities(url, payload, pages_amount)

    return comments


def filter_comments_by_period(comments, days):
    edge_of_comments_date = today - timedelta(days=days)

    filtered_comments = []

    for comment in comments:
        created_at = datetime.utcfromtimestamp(comment['date']).date()
        if created_at > edge_of_comments_date:
            filtered_comments.append(comment)

    return filtered_comments


def get_commentators(comments):
    commentators = set()

    for comment in comments:
        if 'from_id' in comment:
            commentators.add(comment['from_id'])

    return commentators


def get_likers(post_id):
    url = 'https://api.vk.com/method/likes.getList'

    payload = {
        'type': 'post',
        'owner_id': target_group_id,
        'item_id': post_id,
        'filter': 'likes',
        'count': 100,
        'access_token': vk_service_key,
        'v': '5.126'
    }

    response = handle_request(url, payload)
    return response['response']['items']


if __name__ == '__main__':
    env = Env()
    env.read_env()

    vk_service_key = env('VK_SERVICE_KEY')
    group_name = env('VK_GROUP_NAME')
    target_group_id = get_group_id(group_name)
    today = date.today()

    posts = get_vk_posts()

    recent_commentators = set()
    likers = set()

    for post in posts:
        filtered_comments = filter_comments_by_period(get_post_comments(post['id']), FILTER_PERIOD_IN_DAYS)
        recent_commentators = recent_commentators | get_commentators(filtered_comments)
        likers = likers | set(get_likers(post['id']))

    core_audience = recent_commentators.intersection(likers)

    print('----Целевая активная аудитория:----')
    pprint(core_audience)