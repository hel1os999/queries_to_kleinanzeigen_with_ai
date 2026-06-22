from urllib.parse import urlencode

def create_url(
    query: str,
    location: str = None,
    radius: int = None,
    min_price: int = None,
    max_price: int = None,
) -> str:

    url_parts = ["https://www.kleinanzeigen.de"]
    
    
    if min_price is not None and max_price is not None:
        url_parts.append(f"preis:{min_price}:{max_price}")

    elif min_price is not None:
        url_parts.append(f"preis:{min_price}:")
    elif max_price is not None:
        url_parts.append(f"preis::{max_price}")

    keywords_parts = {"keywords": query,}
    
    if location is not None:
        keywords_parts["locationStr"] = location
    if radius is not None:
        keywords_parts["radius"] = radius

    keywords = urlencode(keywords_parts)
    

    if all(i is None for i in (location, radius, min_price, max_price)):
        url_parts.append("k0")
        url = "/".join(url_parts)
        return f"{url}?{keywords}"
        
    url = "/".join(url_parts)

    return f"{url}?{keywords}"