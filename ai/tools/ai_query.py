from langchain.tools import tool

from scrapers.inserate_by_url import scrape_by_url
from ai.config.url_builder import create_url

from utils.browser import OptimizedPlaywrightManager
    
    

def build_search_tool(browser_manager: OptimizedPlaywrightManager):

    @tool("inserat_with_ai", description="Return advertisements for given query")
    async def inserat_with_ai(
        query: str,
        location: str = None,
        radius: int = None,
        min_price: int = None,
        max_price: int = None,
    ):
        url = create_url(
            query=query,
            location=location,
            radius=radius,
            min_price=min_price,
            max_price=max_price,
        )
        scrape = await scrape_by_url(
            browser_manager=browser_manager,  
            base_url=url,
            max_pages=2,                        
            min_publish_date=None,
        )
        if scrape["results"] == []:
            print("There is nothing")
        return scrape["results"]

    return inserat_with_ai
    

