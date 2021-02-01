from environs import Env
from datetime import datetime, date, timedelta
from pprint import pprint

from utils import handle_request


FILTER_PERIOD_IN_DAYS = 30


def get_posts_list(facebook_group_id, facebook_access_token):
    url = f'https://graph.facebook.com/v9.0/{facebook_group_id}/feed'

    payload = {
        'access_token': facebook_access_token,
        'fields': 'id'
    }

    response = handle_request(url, payload)

    post_ids = []

    for post in response['data']:
        post_ids.append(post['id'])

    return post_ids


def get_comments_from_posts(posts, days):
    commentators = set()
    edge_of_comments_date = today - timedelta(days=days)

    for post_id in posts:
        url = f'https://graph.facebook.com/v9.0/{post_id}/comments'

        payload = {
            'access_token': facebook_access_token,
            'fields': 'created_time,from'
        }
        response = handle_request(url, payload)

        for comment in response['data']:
            created_at = datetime.strptime(comment['created_time'], "%Y-%m-%dT%H:%M:%S+0000").date()
            if created_at > edge_of_comments_date:
                commentators.add(comment['from']['id'])

    return commentators


def get_reactions_from_post(posts):
    reactors = {}

    for post_id in posts:
        url = f'https://graph.facebook.com/v9.0/{post_id}/reactions'

        payload = {
            'access_token': facebook_access_token,
        }
        response = handle_request(url, payload)

        for reaction in response['data']:
            reactor_id = reaction['id']

            if reactor_id in reactors:
                reactors[reaction['id']][reaction['type']] += 1
                continue
            else:
                reactors[reaction['id']] = {
                    "LIKE": 0,
                    "LOVE": 0,
                    "WOW": 0,
                    "HAHA": 0,
                    "SAD": 0,
                    "ANGRY": 0,
                    "THANKFUL": 0
                }

            reactors[reaction['id']][reaction['type']] = 1

    return reactors


if __name__ == '__main__':
    env = Env()
    env.read_env()
    facebook_group_id = env('FACEBOOK_GROUP_ID')
    facebook_access_token = env('FACEBOOK_ACCESS_TOKEN')
    today = date.today()

    post_ids = get_posts_list(facebook_group_id, facebook_access_token)

    commentators = get_comments_from_posts(post_ids, FILTER_PERIOD_IN_DAYS)
    reactors = get_reactions_from_post(post_ids)

    print('----Комментаторы за последний месяц:----')
    pprint(commentators)
    print('----Реакции пользователей:----')
    pprint(reactors)




