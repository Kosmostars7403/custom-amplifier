from datetime import datetime, date, timedelta
from pprint import pprint
from collections import Counter

from instabot import Bot
from environs import Env


RANGE_OF_USER_COMMENTS_IN_DAYS = 90
RATING_SIZE_IN_LINES = 5  # количество строчек топа комментаторов


def check_comment_age(comment, edge_date):
    return datetime.utcfromtimestamp(comment['created_at']).date() > edge_date


def login_instagram(username, password):
    instabot = Bot()
    instabot.login(username=username, password=password)
    return instabot


def get_instagram_audience(bot, target_account_name):
    user_id = bot.get_user_id_from_username(target_account_name)
    user_posts = bot.get_total_user_medias(user_id)[4::-1]

    edge_of_comments_date = today - timedelta(days=RANGE_OF_USER_COMMENTS_IN_DAYS)

    comments_amount_rating = Counter()
    commented_posts_amount_rating = Counter()

    for post in user_posts:
        comments = bot.get_media_comments(post)

        commentator_ids = [
            comment['user_id'] for comment in comments if check_comment_age(comment, edge_of_comments_date)
        ]

        comments_amount_rating.update(commentator_ids)

        commented_posts_amount_rating.update(set(commentator_ids))

    return comments_amount_rating.most_common(RATING_SIZE_IN_LINES), commented_posts_amount_rating.most_common(RATING_SIZE_IN_LINES)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    today = date.today()
    instagram_username = env('INSTAGRAM_USERNAME')
    instagram_password = env('INSTAGRAM_PASSWORD')
    target_account_name = env('INSTAGRAM_ACCOUNT_NAME')

    bot = login_instagram(instagram_username, instagram_password)

    comments_amount_rating, commented_posts_amount_rating = get_instagram_audience(bot, target_account_name)

    print('----Комментаторы за последние 3 месяца с кол-вом комментариев----:')
    pprint(comments_amount_rating)
    print('----Комментаторы за последние 3 месяца с кол-вом постов, которые комментировали----:')
    pprint(commented_posts_amount_rating)