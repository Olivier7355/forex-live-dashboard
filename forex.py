#https://rich.readthedocs.io/en/stable/panel.html
#https://proxiesapi-com.medium.com/scraping-currency-data-from-yahoo-finance-with-python-and-beautiful-soup-9b3e5b574691
#https://finance.yahoo.com/currencies
# https://gist.github.com/rxaviers/7360908

from datetime import datetime
from rich.table import Table
from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console, Group
from rich import box
from rich.align import Align
from bs4 import BeautifulSoup
import requests

console = Console()

class Header:
    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]FOREX[/b] Live Dashboard",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")
    
# ********************************   Scrap Technical Analysis Data  ******************************************** 
def scrap_analysis() :
    technicalAnalysis =[]

    URL = "https://www.dailyforex.com/forex-technical-analysis/page-1"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    job_elements = soup.find_all("div", class_="article_main")
    for job_element in job_elements:
        #print(job_element, end="\n"*2)
        time = job_element.find("time").text
        title = job_element.find("a").text
        subTitle = job_element.find("p", class_="hidden-xs").text
        link = job_element.find("a").get("href")
        technicalAnalysis.append([time[0:-1], title, link, subTitle])
    
    message_panel = Table.grid(padding=0)
    for i in range(7) : 
        message_panel.add_row(" ")
        message_panel.add_row(":alarm_clock: [purple]"+technicalAnalysis[i][0]+"[/purple]"+
                            "   :mega:"+technicalAnalysis[i][1])
        message_panel.add_row("[green]"+technicalAnalysis[i][3])
        message_panel.add_row("[blue]:link: https://www.dailyforex.com"+technicalAnalysis[i][2]+"[/blue]")
    
    """""
    theText=''
    for i in range(7) :    
        theText = theText + technicalAnalysis[i][0] +'\t' + technicalAnalysis[i][1] + '\n'+ technicalAnalysis[i][3]+'\n\n'
    
    message_panel = Text.assemble(theText)
    """
    return message_panel


# ********************************   Scrap Currencies Quotes  ******************************************** 
def scrap_currencies() :
    currencies =[]

    URL = "https://www.myfxbook.com/fr/forex-market/currencies"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    #currencyPairs = soup.find_all("span", class_="marketSparkline")
    currencyPairs = soup.find(id="sparkEURUSD")
    currencies.append(['EURUSD',currencyPairs["value"]])
    currencyPairs = soup.find(id="sparkGBPJPY")
    currencies.append(['GBPJPY',currencyPairs["value"]])
    currencyPairs = soup.find(id="sparkUSDJPY")
    currencies.append(['USDJPY',currencyPairs["value"]])
    currencyPairs = soup.find(id="sparkXAUUSD")
    currencies.append(['XAUUSD',currencyPairs["value"]])

    return currencies
    
def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1, size=30),
        Layout(name="footer", size=37),
    )
    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body", ratio=4, minimum_size=60),
    )
    #layout["side"].split(Layout(name="box1"), Layout(name="box2"))
    return layout

def pairs() -> Panel:
    pair = Table.grid(padding=0)
    pair.add_row(" ")
    pair.add_row(":euro: EURUSD   [red]"+scrap_currencies()[0][1]+"[/red]")
    pair.add_row(":pound: GBPJPY   [red]"+scrap_currencies()[1][1]+"[/red]")
    pair.add_row(":dollar: USDJPY   [red]"+scrap_currencies()[2][1]+"[/red]")
    pair.add_row(" ")
    pair.add_row(":trophy: XAUUSD   [red]"+scrap_currencies()[3][1][0:-1]+"[/red]"+"")
    return pair

def test() -> Panel:
    test = Table.grid(padding=0)
    
    test.add_row(":euro: EURUSD   [red]sdsdsd[/red]")

    return test

def news() -> Panel:
    theNews = Table.grid(padding=0)
    newsList =[]
    newsLink = []

    URL = "https://www.dailyfx.com/market-news/articles"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    allNews = soup.find_all("span", class_="dfx-articleCardComponent__title d-block font-weight-bold")
    allLinks = soup.find_all("a", class_="dfx-articleCardComponent dfx-articleCardComponent--menuVariant px-3")

    for news in allNews: newsList.append(news.text)
    for link in allLinks: newsLink.append(link["href"])
    
    for i in range(15) : 
        theNews.add_row(":mega: "+newsList[i])
        theNews.add_row("[blue] "+newsLink[i]+"[/blue]")
    
    return theNews
    

layout = make_layout()

#print(layout)

from time import sleep

from rich.live import Live

with Live(layout, refresh_per_second=0.5, screen=True) as live:
    try:
        while True:
            
            layout["header"].update(Header())
            layout["body"].update(Panel(news(), title=":newspaper: Market News", border_style="yellow"))
            layout["side"].update(Panel(pairs(), title=":currency_exchange: Currencies", border_style="green"))
            layout["footer"].update(Panel(scrap_analysis(), title=":chart_with_upwards_trend: Technical Analysis Forecast", border_style="purple"))
            print('REFRESH')
            sleep(60) # Refresh after 1 minutes
            
    except KeyboardInterrupt:
        exit
        










