# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 23:24:28 2018

@author: YOGZ
"""

import bs4, requests, sys, csv, pyperclip
base_url = sys.argv[1] if len(sys.argv) > 2 else pyperclip.paste()
arr = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'cookie':'inweb_city=Joshimath;'}
res = requests.get(base_url, headers=headers)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
elems = soup.select("li['data-href']")
title = soup.select('.input-control')[0].get('value')
mycsvfile = open(title +'Joshimath' + '.csv','w')
csv.writer(mycsvfile).writerow(['Name','Address','Contact-1', 'Contact-2', 'Rating'])
counter = 2
while len(elems) > 0:
    for j in range(len(elems)):
        url = elems[j].get('data-href')
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text,"html.parser")
        print("Saving data for: %s" %(soup.select('span[class="fn"]')[0].getText()))
        arr.append(soup.select('span[class="fn"]')[0].getText().title())
        address = soup.select('span[class="lng_add"]')
        if len(address) <= 2:
            arr.append(soup.select('span[class="lng_add"]')[1].getText())
        else:
            arr.append(soup.select('span[class="lng_add"]')[2].getText())
        temp = soup.select('a[class="tel"]')
        rating = soup.select('.value-titles')[0].getText() if len(soup.select('.value-titles')) > 0 else 'NA'
        
        style_tag = soup.select('style')
        icons = (str(style_tag[1]).split("."))
        mp = {}
        for e in icons:
            if "icon-" in e:
                if "content" in e:
                    mp[e.split("{")[0].split(":")[0]] = (int(e.split('"')[1][-2:])) - 1

        mobile_numbers = soup.select('span[class="telnowpr"]')
        if len(mobile_numbers) > 0:
            mobile_numbers = mobile_numbers[0];
            mobile_arr = []
            for items in mobile_numbers:
                mobile_arr.append(str(items))
            res = ''.join(mobile_arr)
            soup_mobile = bs4.BeautifulSoup(res,"html.parser")
            temp = soup_mobile.findAll("a", { "class" : "tel" })
            res_one = str(soup_mobile.findAll("a", { "class" : "tel" })[0])
            soup_one = bs4.BeautifulSoup(res_one,"html.parser")
            digits = (soup_one.findAll("span", { "class" : "mobilesv" }))
            s = []
            for elem in digits:
                s.append(str(mp[elem["class"][1]] if mp[elem["class"][1]] != 10 else '+'))
            phone = ''.join(s)
            if(''.join(s[0:3]) == '033'):
                s = s[0:3] + [" "] + s[3:]
            elif(''.join(s[0:3]) == '+91'):
                s = s[0:3] + [" "] + s[3:]
            arr.append(''.join(s))

            if len(temp) > 1:
                res_two = str(soup_mobile.findAll("a", { "class" : "tel" })[1])
                soup_two = bs4.BeautifulSoup(res_two,"html.parser")
                digits = (soup_two.findAll("span", { "class" : "mobilesv" }))
                s = []
                for elem in digits:
                    s.append(str(mp[elem["class"][1]] if mp[elem["class"][1]] != 10 else '+'))
                phone = ''.join(s)
                if(''.join(s[0:3]) == '+91'):
                    s = s[0:3] + [" "] + s[3:]
                elif(''.join(s[0:3]) == '033'):
                    s = s[0:3] + [" "] + s[3:]
                arr.append(''.join(s))
            else:
                arr.append('NA')
        else:
            arr.append('NA')
            arr.append('NA')
        arr.append(rating)
        csv.writer(mycsvfile).writerow(arr)
        arr = []
    res = requests.get(base_url + '/page-' + str(counter), headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    elems = soup.select("li['data-href']")
    counter += 1