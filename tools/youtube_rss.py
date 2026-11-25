# -*- coding: utf-8 -*-
"""Piotro YouTube kanalo video sąrašas iš viešo RSS -> src/youtube.json. Paleisti rankiniu būdu: python3 tools/youtube_rss.py && ./build.sh"""
import json, os, re, urllib.request
CH = "UCcw58zifBWeADgGHDDlQALg"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "youtube.json")
x = urllib.request.urlopen(f"https://www.youtube.com/feeds/videos.xml?channel_id={CH}", timeout=30).read().decode()
def g(e, t):
    m = re.search(f"<{t}>(.*?)</{t}>", e, re.S); return m.group(1).strip() if m else ""
old = {v["id"]: v for v in json.load(open(OUT, encoding="utf-8"))} if os.path.exists(OUT) else {}
for e in re.findall(r"<entry>(.*?)</entry>", x, re.S):
    i = g(e, "yt:videoId"); v = re.search(r'views="(\d+)"', e)
    old[i] = {"id": i, "title": re.sub(r"\s+", " ", g(e, "title")).replace("&amp;", "&"), "date": g(e, "published")[:10],
              "views": int(v.group(1)) if v else 0, "desc": re.sub(r"\s+", " ", g(e, "media:description")).replace("&amp;", "&")[:500]}
vs = sorted(old.values(), key=lambda v: v["date"], reverse=True)
json.dump(vs, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(vs), "video")
