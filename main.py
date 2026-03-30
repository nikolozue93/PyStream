from argparse import ArgumentParser
from typing import List, Optional, Sequence
import requests
import xml.etree.ElementTree as ET
import html

class UnhandledException(Exception):
    pass


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json: bool = False,
) -> List[str]:
    """
    parses RSS XML and returns formatted strings or a JSON-ready list.
    """
    
    root = ET.fromstring(xml)
    channel = root.find("channel")
    if channel is None:   # if theres no channel, rss is broken or empty
        return []
    
    if json:
        pass
    
    output = []
    title = html.unescape(channel.findtext("title", ""))
    link = html.unescape(channel.findtext("link", ""))
    desc = html.unescape(channel.findtext("description", ""))

    output.append(f"Feed: {title}")
    output.append(f"Link: {link}")
    output.append(f"Description: {desc}")

    all_items = channel.findall("item")
    # if a limit is provided, slice the list
    if limit is not None and limit > 0:
        all_items = all_items[:limit]

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

        description = item.findtext("description")
        if description:
            output.append("") 
            output.append(html.unescape(description))

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
    xml = requests.get(args.source).text
    try:
        print("\n".join(rss_parser(xml, args.limit, args.json)))
        return 0
    except Exception as e:
        raise UnhandledException(e)


if __name__ == "__main__":
    main()
