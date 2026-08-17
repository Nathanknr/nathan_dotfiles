# qutebrowser config.py
# Adapted from Evan Chen Dotfiles
# https://github.com/vEnhance/dotfiles

from typing import TYPE_CHECKING, Any, cast

from qutebrowser.api import interceptor

if TYPE_CHECKING:
    # c and config are injected as globals by qutebrowser at runtime
    c = cast(Any, None)
    config = cast(Any, None)

config.load_autoconfig()
c.content.headers.user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"

c.backend = "webengine"
c.content.blocking.method = "both"
c.content.javascript.enabled = True
c.downloads.position = "bottom"
c.downloads.remove_finished = 5000
c.fonts.default_size = "16pt"
c.hints.auto_follow = "unique-match"
c.hints.auto_follow_timeout = 700
#c.hints.mode = "number"
c.input.insert_mode.auto_enter = True
c.input.insert_mode.auto_leave = True
c.input.insert_mode.auto_load = True
c.tabs.background = False
c.tabs.last_close = "close"
c.content.pdfjs = True
c.tabs.show = "always"
c.url.searchengines = {
    "DEFAULT": "https://duckduckgo.com/?q={}",
    'g': 'https://www.google.com/search?q={}',
}
c.url.start_pages = c.url.default_page
c.zoom.default = 100

#c.qt.force_software_rendering = "chromium" 

# config.bind(r'<Return>', 'download-clear')
config.bind(r"ss", "config-source")
config.bind(r"m", 'spawn mpv "{url}"')
config.bind(r"e", "tab-clone")
config.bind(r"B", 'spawn brave-browser "{url}"')
config.bind(r"Z", "tab-only")
config.bind(r"x", "scroll-page 0 0.5")
config.bind(r"u", "scroll-page 0 -0.5")
config.bind(r"d", "tab-close")
config.bind(r"|", "tab-give")
config.bind(r"h", "home")
config.bind("\\", "mode-enter passthrough")

ALLOW_JAVASCRIPT_WEBSITES = (
    r"*://100.100.100.100/*",
    r"*://*.0xparc.org/*",
    r"*://*.amazon.com/*",
    r"*://*.athemath.org/*",
    r"*://*.archlinux.org/*",
    r"*://*.bitwarden.com/*",
    r"*://*.cloudflare.com/*",
    r"*://*.commonapp.org/*",
    r"*://*.crosserville.com/*",
    r"*://*.duckduckgo.com/*",
    r"*://*.evanchen.cc/*",
    r"*://*.facebook.com/*",
    r"*://*.firebaseapp.com/*",
    r"*://*.galacticpuzzlehunt.com/*",
    r"*://*.g2mathprogram.org/*",
    r"*://*.github.com/*",
    r"*://*.gradescope.com/*",
    r"*://*.hanabi.github.io/*",
    r"*://*.hmmt.org/*",
    r"*://*.howtostudykorean.com/*",
    r"*://*.imo-official.org/*",
    r"*://*.instagram.com/*",
    r"*://*.itch.io/*",
    r"*://*.komal.hu/*",
    r"*://*.lmfdb.org/*",
    r"*://*.miro.com/*",
    r"*://*.mit.edu/*",
    r"*://*.mitadmissions.org/*",
    r"*://*.monkeytype.com/*",
    r"*://*.myaccount.google.com/*",
    r"*://*.naver.com/*",
    r"*://*.notion.so/*",
    r"*://*.notion.site/*",
    r"*://*.overleaf.com/*",  # their documentation is admittedly not bad
    r"*://*.okta.com/*",
    r"*://*.pretzel.rocks/*",
    r"*://*.probase.app/*",
    r"*://*.pythonanywhere.com/*",
    r"*://*.readthedocs.io/*",
    r"*://*.reference.slideroom.com/*",
    r"*://*.sagemath.org/*",
    r"*://*.stackexchange.com/*",
    r"*://*.steampowered.com/*",
    r"*://*.stripe.com/*",
    r"*://*.tailwindcss.com/*",
    r"*://*.teammatehunt.com/*",
    r"*://*.torproject.com/*",
    r"*://*.twitch.tv/*",
    r"*://*.wikipedia.org/*",
    r"*://*.wolframalpha.com/*",
    r"*://*.wikidata.org/*",
    r"*://*.usaco.org/*",
    r"*://*.youtube.com/*",
    r"*://0xparc.org/*",
    r"*://127.0.0.1/*",
    r"*://accounts.google.com/*",
    r"*://artofproblemsolving.com/*",
    r"*://arxiv.org/*",
    r"*://atcoder.jp/*",
    r"*://athemath.org/*",
    r"*://aur.chaotic.cx/*",
    r"*://axiommath.ai/*",
    r"*://bitwarden.com/*",
    r"*://calendar.google.com/*",
    r"*://calendly.com/*",
    r"*://claude.ai/*",
    r"*://codeforces.com/*",
    r"*://dennisc.net/*",
    r"*://devjoe.appspot.com/*",
    r"*://discord.com/*",
    r"*://docs.google.com/*",
    r"*://drive.google.com/*",
    r"*://duckduckgo.com/*",
    r"*://gitlab.com/*",
    r"*://github.com/*",
    r"*://groups.google.com/*",
    r"*://hackmd.io/*",
    r"*://hanabi-competitions.com/*",
    r"*://hanabi.github.io/*",
    r"*://hanabi-league.com/*",
    r"*://hanabi-league.github.io/*",
    r"*://hanab.live/*",
    r"*://ioinformatics.org/*",
    # r"*://liquipedia.net/*",
    r"*://localhost/*",
    r"*://login.artofproblemsolving.com/*",
    r"*://mathoverflow.net/*",
    r"*://mit.edu/*",
    r"*://orcid.org/*",
    r"*://poll.ma.pe/*",
    r"*://projecteuler.net/*",
    r"*://pypi.org/*",
    r"*://nightbot.tv/*",
    r"*://regex101.com/*",
    r"*://sc2replaystats.com/*",
    r"*://stackoverflow.com/*",
    r"*://steamcommunity.com/*",
    r"*://streamlabs.com/*",
    r"*://swaroopg92.github.io/*",
    r"*://tailwindcomponents.com/*",
    r"*://tailwindcss.com/*",
    r"*://translate.google.com/*",
    r"*://typst.app/*",
    r"*://usaco.guide/*",
    r"*://usaco.org/*",
    r"*://usamo.wordpress.com/*",
    r"*://wordpress.com/*",
    r"*://www.google.com/maps/*",
    r"*://xkcd.com/*",
    r"*://youtube.com/*",
)

for site in ALLOW_JAVASCRIPT_WEBSITES:
    config.set("content.javascript.enabled", True, site)
    config.set("content.javascript.clipboard", "access-paste", site)


# Block youtube ads
def filter_youtube(info: interceptor.Request):
    """Block given request if necessary"""
    url = info.request_url
    if (
        url.host() == "www.youtube.com"
        and url.path() == "/get_video_info"
        and "&adformat=" in url.query()
    ):
        info.block()


interceptor.register(filter_youtube)
