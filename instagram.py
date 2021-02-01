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


def get_instagram_audience(bot):
    user_id = bot.get_user_id_from_username("cocacolarus")
    user_posts = bot.get_total_user_medias(user_id)[4::-1]

    commentators_rating = {}
    commentators_by_post_rating = {}

    for post in user_posts:
        comments = bot.get_media_comments(post)
        commentators = set()

        for comment in comments:
            edge_of_comments_date = today - timedelta(days=RANGE_OF_USER_COMMENTS_IN_DAYS)
            created_at = datetime.utcfromtimestamp(comment['created_at']).date()
            if created_at > edge_of_comments_date:
                commentator_id = comment['user_id']
                commentators.add(commentator_id)
                increment_rating(commentator_id, commentators_rating)

        for user_id in commentators:
            increment_rating(user_id, commentators_by_post_rating)

    return commentators_rating, commentators_by_post_rating


if __name__ == '__main__':
    env = Env()
    env.read_env()

    today = date.today()
    instagram_username = env('INSTAGRAM_USERNAME')
    instagram_password = env('INSTAGRAM_PASSWORD')

    bot = login_instagram(instagram_username, instagram_password)

    commentators_rating, commentators_by_post_rating = get_instagram_audience(bot)

    print('----Комментаторы за последние 3 месяца с кол-вом комментариев----:')
    pprint(commentators_rating)
    print('----Комментаторы за последние 3 месяца с кол-вом постов, которые комментировал----:')
    pprint(commentators_by_post_rating)