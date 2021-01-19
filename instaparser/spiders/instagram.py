import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import InstaparserItem

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']

    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'kttt9333'
    inst_password = ''
    parse_user = ['selena_sun_', 'katya.t_m']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    subscriber_hash = '5aefa9893005572d237da5068082d8d5'
    subscribe_hash = '3dec7e2c57367ef3da3d987d89f9dbc8'

    def parse(self, response:HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        print(f"self.user_login={self.user_login}")
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback= self.user_login,
            formdata={'username': self.inst_login, 'enc_password':self.inst_password},
            headers= {'X-CSRFToken':csrf_token}
        )

    def user_login(self, response:HtmlResponse):
        j_data = response.json()
        print(f"j_data={j_data}")
        if j_data['authenticated']:
            print('auth')
            for usr in self.parse_user:
                yield response.follow(
                    f'/{usr}',
                    callback= self.user_data_parse,
                    cb_kwargs={'username':usr}
                )


    def user_data_parse(self, response:HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {"id": user_id, "include_reel": True, "fetch_mutual": True, "first": 24}
        variables_s = {"id": user_id, "include_reel": True, "fetch_mutual": False, "first": 13}
        print(f"user_id={user_id}")
        url_subscribers = f'{self.graphql_url}query_hash={self.subscriber_hash}&{urlencode(variables)}'
        url_subscribe = f'{self.graphql_url}query_hash={self.subscribe_hash}&{urlencode(variables_s)}'
        for i in range(2):
            if i == 0:
                print(f"i={0}")
                yield response.follow(
                    url_subscribers,
                    callback=self.user_subscribers_parse,
                    cb_kwargs={'username':username,
                               'user_id': user_id,
                               'variables': deepcopy(variables)}
                )
            else:
                print(f"i={1}")
                yield response.follow(
                    url_subscribe,
                    callback=self.user_subscribe_parse,
                    cb_kwargs={'username': username,
                               'user_id': user_id,
                               'variables': deepcopy(variables)}
                )


    def user_subscribers_parse(self, response:HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_subscribers = f'{self.graphql_url}query_hash={self.subscriber_hash}&{urlencode(variables)}'
            yield response.follow(
                url_subscribers,
                callback=self.user_subscribers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        subscribers = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        for subscriber in subscribers:
            item = InstaparserItem(
                subscribe_user_id = user_id,
                photo = subscriber.get('node').get('profile_pic_url'),
                user_id = subscriber.get('node').get('id'),
                user_name = subscriber.get('node').get('username'),
                user_data = subscriber.get('node')
            )
            yield item


    def user_subscribe_parse(self, response:HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_subscribers = f'{self.graphql_url}query_hash={self.subscriber_hash}&{urlencode(variables)}'
            yield response.follow(
                url_subscribers,
                callback=self.user_subscribers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        subscribers = j_data.get('data').get('user').get('edge_follow').get('edges')
        for subscriber in subscribers:
            item = InstaparserItem(
                subscribe_user_id = subscriber.get('node').get('id'),
                photo = subscriber.get('node').get('profile_pic_url'),
                user_id = user_id,
                user_name = subscriber.get('node').get('username'),
                user_data = subscriber.get('node')
            )
            yield item


    # #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        print(f'fetch_csrf_token={matched}')
        return matched.split(':').pop().replace(r'"', '')


    # # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        print(f'fetch_csrf_token={matched}')
        return json.loads(matched).get('id')