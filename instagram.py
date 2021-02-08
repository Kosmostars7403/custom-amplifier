from datetime import datetime, date, timedelta
from pprint import pprint

from instabot import Bot
from environs import Env


RANGE_OF_USER_COMMENTS_IN_DAYS = 90


def increment_rating(user, rating_type):
    if user in rating_type:
        rating_type[user] += 1
    else:
        rating_type[user] = 1


def login_instagram(username, password):
    instabot = Bot()
    instabot.login(username=username, password=password)
    return instabot


def filter_active_commentators_from_comment(comment, commentators_rating):
    created_at = datetime.utcfromtimestamp(comment['created_at']).date()
    if created_at > edge_of_comments_date:
        increment_rating(comment['user_id'], commentators_rating)
    return comment['user_id']


def get_instagram_audience(bot, target_account_name):
    user_id = bot.get_user_id_from_username(target_account_name)
    user_posts = bot.get_total_user_medias(user_id)[4::-1]

    commentators_rating = {}
    commentators_by_post_rating = {}

    for post in user_posts:
        comments = bot.get_media_comments(post)
        commentators = {filter_active_commentators_from_comment(comment, commentators_rating) for comment in comments}
        [increment_rating(user_id, commentators_by_post_rating) for user_id in commentators]

    return commentators_rating, commentators_by_post_rating


if __name__ == '__main__':
    env = Env()
    env.read_env()

    today = date.today()
    instagram_username = env('INSTAGRAM_USERNAME')
    instagram_password = env('INSTAGRAM_PASSWORD')
    target_account_name = env('INSTAGRAM_ACCOUNT_NAME')

    bot = login_instagram(instagram_username, instagram_password)

    edge_of_comments_date = today - timedelta(days=RANGE_OF_USER_COMMENTS_IN_DAYS)

    commentators_rating, commentators_by_post_rating = get_instagram_audience(bot, target_account_name)

    print('----Комментаторы за последние 3 месяца с кол-вом комментариев----:')
    pprint(commentators_rating)
    print('----Комментаторы за последние 3 месяца с кол-вом постов, которые комментировали----:')
    pprint(commentators_by_post_rating)