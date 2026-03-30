from argparse import ArgumentParser
from typing import List, Optional, Sequence
import requests
import xml.etree.ElementTree as ET
import html
import json
import re


class UnhandledException(Exception):
    pass

def clean_html(raw_html: str) -> str:
    """Removes HTML tags and cleans up whitespace."""
    if not raw_html:
        return ""
    clean_text = re.sub(r'<[^>]+>', '', raw_html)
    return clean_text.strip()

def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json_format: bool = False,
) -> List[str]:
    """
    RSS parser

    Args:
        xml: XML document as a string.
        limit: Number of the news to return. if None, returns all news.
        json: If True, format output as JSON.

    Returns:
        List of strings.

    Examples:
        >>> xml = ('<rss><channel><title>RSS Channel</title><link>https://some.rss.com</link>'
        ...        '<description>RSS Channel</description></channel></rss>')
        >>> rss_parser(xml)
        ['Feed: RSS Channel', 'Link: https://some.rss.com', 'Description: RSS Channel']
        >>> print("\\n".join(rss_parser(xml)))
        Feed: RSS Channel
        Link: https://some.rss.com
        Description: RSS Channel
    """
    root = ET.fromstring(xml)
    channel = root.find("channel")
    if channel is None:   # if theres no channel, rss is broken or empty
        return []

    all_items = channel.findall("item")  # if a limit is provided, slice the list
    if limit is not None and limit > 0:
        all_items = all_items[:limit]
        
    if json_format:
        data = {
            "title": html.unescape(channel.findtext("title", "")),
            "link": html.unescape(channel.findtext("link", "")),
            "description": html.unescape(channel.findtext("description", "")),
            "items": []
        }

        for item in all_items:
            item_dict = {}

            # exact tag names from the rss spec as keys
            fields = ["title", "author", "pubDate", "link", "category", "description"]
            for field in fields:  
                val = item.findtext(field)
                if val:
                    item_dict[field] = html.unescape(val)
            data["items"].append(item_dict)

        json_result = json.dumps(data, indent=2)
        return [json_result]

    # --- CONSOLE OUTPUT HEADERS ---
    output = []

    feed_title = channel.findtext("title")
    if feed_title:
        output.append(f"Feed: {html.unescape(feed_title)}")

    feed_link = channel.findtext("link")
    if feed_link:
        output.append(f"Link: {html.unescape(feed_link)}")

    lbd = channel.findtext("lastBuildDate")
    if lbd:
        output.append(f"Last Build Date: {html.unescape(lbd)}")

    pd = channel.findtext("pubDate")
    if pd:
        output.append(f"Publish Date: {html.unescape(pd)}")

    lang = channel.findtext("language")
    if lang:
        output.append(f"Language: {html.unescape(lang)}")
    
    ch_cats = [html.unescape(c.text) for c in channel.findall("category") if c.text]
    if ch_cats:  # categories for channel, comma separated
        output.append(f"Categories: {', '.join(ch_cats)}")
    
    editor = channel.findtext("managingEditor")
    if editor:
        output.append(f"Editor: {html.unescape(editor)}")
    
    feed_desc = channel.findtext("description")
    if feed_desc:
        output.append(f"Description: {html.unescape(feed_desc)}")

    for item in all_items:
        output.append("")

        title = item.findtext("title")
        if title:
            output.append(f"Title: {html.unescape(title)}")

        author = item.findtext("author")
        if author:
            output.append(f"Author: {html.unescape(author)}")

        pub_date = item.findtext("pubDate")
        if pub_date:
            output.append(f"Published: {html.unescape(pub_date)}")

        link = item.findtext("link")
        if link:
            output.append(f"Link: {html.unescape(link)}")

        categories = [html.unescape(c.text) for c in item.findall("category") if c.text]
        if categories:
            output.append(f"Categories: {', '.join(categories)}")

        desc = item.findtext("description")
        if desc:
            cleaned_desc = clean_html(html.unescape(desc))
            output.append("") 
            output.append(html.unescape(cleaned_desc))

    return output
        

def main(argv: Optional[Sequence] = None):
    parser = ArgumentParser(
        prog="PyStream",
        description="high-performance, standalone RSS parser with JSON serialization support",
    )
    parser.add_argument("source", help="RSS URL", type=str, nargs="?")
    parser.add_argument(
        "--json", help="Print result as JSON in stdout", action="store_true"
    )
    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )

    args = parser.parse_args(argv)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(args.source, headers=headers, timeout=10)

        if response.status_code == 404:
            print(f"Error: The URL {args.source} was not found (404).")
            return 1
        response.raise_for_status()
        
        # check if the request actually worked before parsing
        if response.status_code != 200:
            raise UnhandledException(f"HTTP Error {response.status_code}")

        xml_content = response.text

        results = rss_parser(xml_content, args.limit, args.json)

        if results:
            print("\n".join(results))

        return 0
    except Exception as e:
        # this catches the ParseError or connection errors and wraps them
        raise UnhandledException(e)


if __name__ == "__main__":
    main()
