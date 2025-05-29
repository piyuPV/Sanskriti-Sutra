from datetime import datetime, timedelta

events = [
    {
        "title": "Art Fair 🎨",
        "start": str(datetime.now().date()),
        "end": str((datetime.now() + timedelta(days=1)).date()),
        "display": "block",
        "backgroundColor": "#FF9999",
        "extendedProps": {
            "image": "https://cdn.shopify.com/s/files/1/0663/4022/5253/files/artociti_blog_2_warli_480x480.jpg?v=1681724976"
        }
    },
    {
        "title": "Dance Festival 💃",
        "start": str((datetime.now() + timedelta(days=3)).date()),
        "end": str((datetime.now() + timedelta(days=4)).date()),
        "display": "block",
        "backgroundColor": "#99FF99",
        "extendedProps": {
            "image": "https://cdn.shopify.com/s/files/1/0663/4022/5253/files/artociti_blog_2_warli_480x480.jpg?v=1681724976"
        }
    }
]