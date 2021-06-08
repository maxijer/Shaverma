import requests
from bs4 import BeautifulSoup as bs


def i_search_your_shaurmu(x: str, y: str, kak: int):
    response = requests.get("https://www.google.com/search?hl=ru&tbs=lf:1,lf_ui:9&tbm=lcl&q=%D1%88%D0%B0%D1%83%D1%80%D0%BC%D0%B0&rflfq=1&num=10&sa=X&ved=2ahUKEwiN1PKCsYHxAhWJjosKHaEsD6cQjGp6BAgFEEI&biw=1366&bih=657#rlfi=hd:;si:;mv:[[52.7794964,41.5055468],[52.5737898,41.3815482]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:9")
    htmlka = bs(response.content, 'html.parser')
    print(htmlka)
    print("-------------")
    for i in htmlka.select(".wYWDAd"):
        print(i)

print(i_search_your_shaurmu("52.766858", "41.406565", 1))

