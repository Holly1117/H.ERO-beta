# -*- coding: utf-8 -*-
import requests
import re
import json
import codecs
import webHook
import traceback

HERO_FILE_PATH = './json/hero.json'

CALENDAR_FILE_PATH = './json/calendar.json'

CONTEXT_URL = 'https://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/before_hatubai_yotei.php'

DETAIL_URL = 'https://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/'

REQUEST_HTML = None

KINDS_NAME = ['(PS4)', '(PS5)', '(NS)', '(XBO)']

IMAGE_NAME = 'HI00_'

TITLE_PATTERN = r'<ahref="(game.+?)"class="tooltip.+?">(.+?)<.a>(.*?)<ahref'

KINDS_PATTERN = r'<.*?>(.*?)<.*?>'

BRAND_PATTERN = r'<ahref="brand.*?">(.*?)<.a>'

DETAIL_PATTERN = r'<h2id="game_title"class="bottom-margin"><ahref="(.*?)">.*?<ahref="(.*?)">.*?発売日.*?>(\d.*?-\d.*?-\d.*?)<'

IMAGE_PATTERN = r'imgsrc="(.*?)".*?'

BRAND_URL_PATTERN = r'<divid="soft-title"><ahref="(.*?)"target="_blank">.*?<.a>'

MENU_DATE_PATTERN = r'(\d.*?)-(\d.*?)-.*?'

CALENDAR_LIST = []

HERO_LIST = []

TITLE_LIST = []

URL_LIST = []

DATE_LIST = []

BRAND_LIST = []

BRAND_URL_LIST = []

IMAGE_LIST = []

YOUTUBE_LIST = []

KINDS_LIST = []

DETAIL_LIST = []

BRAND_DETAIL_LIST = []


def get_title():
    html = requests.get(CONTEXT_URL,timeout=10).text
    html = html.replace('\n', '').replace('\t', '').replace(' ', '')
    result_html = re.findall(TITLE_PATTERN, html)
    for title in result_html:
        DETAIL_LIST.append(title[0])
        TITLE_LIST.append(title[1])
        kinds_list = re.findall(KINDS_PATTERN, title[2])
        if len(kinds_list) != 0:
            KINDS_LIST.append(get_kinds(kinds_list))
        else:
            KINDS_LIST.append(None)


def get_kinds(kinds_list):
    for kinds in kinds_list:
        if kinds in KINDS_NAME:
            return kinds


def get_brand():
    html = requests.get(CONTEXT_URL,timeout=10).text
    html = html.replace('\n', '').replace('\t', '').replace(' ', '')
    result_html = re.findall(BRAND_PATTERN, html)
    for brand in result_html:
        BRAND_LIST.append(brand)


def get_detail():
    for detail in DETAIL_LIST:
        requests_html = requests.get(
            DETAIL_URL + detail).text.replace('\n', '').replace('\t', '').replace(' ', '')
        result_html = re.findall(DETAIL_PATTERN, requests_html)
        for result in result_html:
            IMAGE_LIST.append(get_image(requests_html))
            URL_LIST.append(result[0])
            BRAND_DETAIL_LIST.append(result[1])
            DATE_LIST.append(result[2])


def get_image(requests_html):
    if 'imgsrc' in requests_html:
        result_html = re.findall(IMAGE_PATTERN, requests_html)
        return result_html[0]
    else:
        return None


def get_brand_url():
    for brand in BRAND_DETAIL_LIST:
        requests_html = requests.get(
            DETAIL_URL + brand).text.replace('\n', '').replace('\t', '').replace(' ', '')
        result_html = re.findall(BRAND_URL_PATTERN, requests_html)
        if len(result_html) != 0:
            BRAND_URL_LIST.append(result_html[0])
        else:
            BRAND_URL_LIST.append(None)


def set_hero():
    get_title()
    get_brand()
    get_detail()
    get_brand_url()
    calendar_list = []
    for index, title in enumerate(TITLE_LIST):
        menu_date = re.findall(MENU_DATE_PATTERN, DATE_LIST[index])
        year = int(menu_date[0][0])
        month = int(menu_date[0][1])
        if menu_date[0][0] + "-" + menu_date[0][1] not in calendar_list:
            calendar_list.append(menu_date[0][0] + "-" + menu_date[0][1])
            set_calendar(year, month)
        HERO_LIST.append({
            "game_name": title,
            "game_date": DATE_LIST[index],
            "game_url": URL_LIST[index],
            "game_image": IMAGE_NAME + str(index),
            "game_youtube": None,
            "game_kinds": KINDS_LIST[index],
            "brand_name": BRAND_LIST[index],
            "brand_url": BRAND_URL_LIST[index],
            "menu_date_year": year,
            "menu_date_month": month,
        })
    return HERO_LIST


def get_hero():
    js_rerd_data = open('./json/hero.json', 'r', encoding="utf-8_sig")
    hero_data = json.load(js_rerd_data)
    return hero_data


def get_image_name(hero_list):
    image_name = IMAGE_NAME + str(len(hero_list))
    return image_name


def get_unfinished_list(old_hero_list, new_hero):
    for old_hero in old_hero_list:
        if (new_hero["game_name"] == old_hero["game_name"]) and (new_hero["game_kinds"] == old_hero["game_kinds"]):
            return False
    return True


def set_calendar(year, month):
    CALENDAR_LIST.append({
        "date_year": year,
        "date_month": month
    })


def parse_json(info_jsons, path):
    codecs_open = codecs.open(path, 'w', 'utf-8')
    json.dump(info_jsons, codecs_open, ensure_ascii=False, indent=2)
    codecs_open.close()


def get_new_hero_list(new_hero_list, path):
    try:
        js_r = open(path, 'r', encoding="utf-8_sig")
        info_jsons = json.load(js_r)
        old_index = len(info_jsons)
        old_hero_list = info_jsons
        for new_hero in new_hero_list:
            if get_unfinished_list(old_hero_list, new_hero):
                new_hero["game_image"] = get_image_name(old_hero_list)
                old_hero_list.append(new_hero)
        old_hero_list = sorted(old_hero_list, key=lambda x: x['game_date'])
        parse_json(old_hero_list, path)
        new_index = len(old_hero_list)
        update_index = new_index - old_index
        webHook.post_requests(True, str(update_index), '')
    except Exception:
        e = traceback.format_exc()
        webHook.post_requests(False, str(0), e)


get_new_hero_list(set_hero(), HERO_FILE_PATH)
parse_json(CALENDAR_LIST, CALENDAR_FILE_PATH)
