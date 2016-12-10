import requests

key = 'AIzaSyA1ECU2Ue7cJh047hRei-eysej6clVxBDM'


def url_shortener(url):
    r = requests.post('https://www.googleapis.com/urlshortener/v1/url?fields=id&key=%s' % key, json={"longUrl": url})
    return r.text[10:-4]
