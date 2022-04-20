import requests
import json

WEBHOOK_URL = 'https://discord.com/api/webhooks/962181926641356900/wc0m2fnpUJHgTkFph9dDZQ0J0OOJsRrAQp9zeXTEvEDC7Ocn0g0ulkSphraJSapMwhYH'

HERO_CONTENT = [ "H.ERO", "https://pics.prcm.jp/a6b73bcfbb1b3/83801295/png/83801295_480x528.png"]

HEADRES = {'Content-Type': 'application/json'}

def get_embeds(result,index,e):
    if (result):
     return [{'title': "Notice from the H.ERO",'description': 'Got '+index+' new information.\nplease confirm!','color': 1939322}]
    else:
     return [{'title': "Notice from the H.ERO",'description': 'Update failed!\nPlease maintain immediately!/n/n['+ e +']','color': 15146762}]

def get_content(result,index,e):
        return {'username': HERO_CONTENT[0],'avatar_url':  HERO_CONTENT[1],'embeds': get_embeds(result,index,e)}

def post_requests(result,index,e):
    requests.post(WEBHOOK_URL, json.dumps(get_content(result,index,e)), headers=HEADRES)