from bs4 import BeautifulSoup
import urllib.request


def find_title(site):
    title = ""
    for line in site.split("\n"):
        if "<title>" in line:
            line = line.replace('<title>', "")
            line = line.replace('</title>', "")
            title = line
    return title


site = """<html lang="ru" prefix="og: http://ogp.me/ns# video: http://ogp.me/ns/video# article: http://ogp.me/ns/article# ya: http://webmaster.yandex.ru/vocabularies/">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no">
    <meta charset="utf-8">
<meta http-equiv="x-ua-compatible" content="ie=edge">
<title>Подруга Заворотнюк: Состояние Анастасии заметно улучшилось - «Life.ru» — информационный портал</title>
    <link rel="dns-prefetch" href="//static.life.ru">
    <link rel="preconnect" href="//static.life.ru">
    <link rel="dns-prefetch" href="//comments.life.ru">
    <link rel="preconnect" href="//comments.life.ru">
    <link rel="dns-prefetch" href="//social.life.ru">
    <link rel="preconnect" href="//social.life.ru">
    <link rel="dns-prefetch" href="//www.google-analytics.com">
    <link rel="preconnect" href="//www.google-analytics.com">
    <link rel="dns-prefetch" href="//mc.yandex.ru">
    <link rel="preconnect" href="//mc.yandex.ru">
    <meta name="description" content="Врачи обнадёжили родственников &#34;прекрасной няни&#34;: шансы на её выздоровление, по их словам, немаленькие.">
    <meta name="keywords" content="">
    <meta name="theme-color" content="#fa0a0a">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <meta name="apple-itunes-app" content="app-id=1112626879">
    <meta name="google-play-app" content="app-id=ru.newsmediamobile.lifenews">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@LifeislifeRu">
    <meta name="twitter:creator" content="@LifeislifeRu">"""
title = find_title(site)
print(title)