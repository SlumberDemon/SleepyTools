import fastapi
from deta import Base
from fastapi.templating import Jinja2Templates

pages = Jinja2Templates(directory="pages")
links = Base("links")
cards = Base("embeds")
app = fastapi.FastAPI()


@app.get("/", response_class=fastapi.responses.HTMLResponse)
async def home(request: fastapi.Request):
    return pages.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard", response_class=fastapi.responses.HTMLResponse)
async def dashboard(request: fastapi.Request):
    return pages.TemplateResponse("dashboard.html", {"request": request})


@app.post("/shorten")
async def shorten(url: str):
    key = links.put({"item": [url]})
    return {"url": f"https://sleepy.deta.dev/url/{key['key']}"}


@app.post("/embed")
async def embed(
    title: str,
    description: str = None,
    colour: str = None,
    image: str = None,
    size: str = None,
    url: str = None,
):
    key = cards.put(
        {
            "item": [
                {
                    "title": title,
                    "description": description,
                    "image": image,
                    "colour": colour,
                    "size": size,
                    "url": url,
                }
            ]
        }
    )
    return {"url": f"https://sleepy.deta.dev/card/{key['key']}"}


@app.get("/url/{id}", response_class=fastapi.responses.HTMLResponse)
async def url(id: str):
    url = links.get(id)
    return fastapi.responses.HTMLResponse(
        f"""
        <meta http-equiv="refresh" content="0; url = {url['item'][0]}" />
        <h1>You're about to be redirected</h1>
        """
    )


@app.get("/card/{id}", response_class=fastapi.responses.HTMLResponse)
async def card(id: str):
    meta = cards.get(id)
    link = meta["item"][0]["url"]
    if not link:
        link = "https://sleepy.deta.dev"
    return fastapi.responses.HTMLResponse(
        f"""
        <meta property="og:title" content="{meta['item'][0]['title']}"/>
        <meta property="og:type" content="website"/>
        <meta property="og:image" content="{meta['item'][0]['image']}"/>
        <meta property="og:url" content="{link}"/>
        <meta property="og:description" content="{meta['item'][0]['description']}"/>
        <meta name="url" content="https://sleepy.deta.dev">
        <meta name="theme-color" content="#{meta['item'][0]['colour']}">
        <meta name="twitter:card" content="summary_{meta['item'][0]['size']}_image">
        <meta http-equiv="refresh" content="0; url = {link}" />
        """
    )
