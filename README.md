# PyStream RSS Reader

A high-performance, standalone Command Line Interface (CLI) tool for parsing RSS 2.0 feeds. This utility allows users to read news directly in the terminal or export data as structured JSON.

## What is RSS?
RSS (Really Simple Syndication) is a web feed that allows users and applications to access updates to websites in a standardized, computer-readable format. [Learn more on Wikipedia](https://en.wikipedia.org/wiki/RSS).

## Features

* **RSS 2.0 Support:** Full parsing of Channel metadata and News Items.
* **Flexible Output:** Choose between human-readable text or pretty-printed JSON.
* **News Limiting:** Option to limit the number of news topics returned.
* **Clean Formatting:** Automatically handles HTML entities (like `&#39;`) for readable text.
* **Clean Terminal Output**: Automatically strips HTML tags (like `<div>`, `<li>`, and `<a>`) from descriptions to ensure terminal readability, even for content-heavy feeds like Google News.
* **PEP8 Compliant:** Built with clean, maintainable Python code.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nikolozue93/pystream.git
   cd pystream
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The basic syntax for the reader is:

```bash
python rss_reader.py [URL] [OPTIONS]
```

### Positional Arguments
* `source`: The URL of the RSS feed you wish to parse.

### Optional Arguments
* `-h, --help`: Show the help message.
* `--limit LIMIT`: Limit the number of news topics (e.g., `--limit 5`).
* `--json`: Print the result as a pretty-printed JSON string.

---

## Examples

### 1. Standard Console Output
```bash
python rss_reader.py https://www.nasa.gov/rss/dyn/breaking_news.rss --limit 1
```

**Output:**
```plaintext
Feed: NASA
Link: https://www.nasa.gov
Last Build Date: Mon, 30 Mar 2026 18:18:28 +0000
Language: en-US
Description: Official National Aeronautics and Space Administration Website

Title: Sendoff for Artemis II Crew
Published: Mon, 30 Mar 2026 18:18:27 +0000
Link: https://www.nasa.gov/image-article/sendoff-for-artemis-ii-crew/
Categories: Andre Douglas, Artemis 2, Christina H. Koch, G. Reid Wiseman, Johnson Space Center, Victor J. Glover

From left to right, NASA astronauts Andre Douglas, Victor Glover...
```

### 2. JSON Export
```bash
python rss_reader.py https://www.nasa.gov/rss/dyn/breaking_news.rss --limit 1 --json
```

**Output:**
```json
{
  "title": "NASA",
  "link": "https://www.nasa.gov",
  "description": "Official National Aeronautics and Space Administration Website",
  "items": [
    {
      "title": "Sendoff for Artemis II Crew",
      "pubDate": "Mon, 30 Mar 2026 18:18:27 +0000",
      "link": "https://www.nasa.gov/image-article/sendoff-for-artemis-ii-crew/",
      "category": "Andre Douglas",
      "description": "From left to right, NASA astronauts Andre Douglas, Victor Glover..."
    }
  ]
}
```

---

## Troubleshooting

### `UnhandledException: HTTP Error 403`
Some servers (like Yahoo or LinkedIn) block requests that do not have a browser-like User-Agent. This tool includes a default header to bypass most blocks, but if you still see this:
* Verify the URL is a direct link to an XML/RSS file.
* Check if your IP has been rate-limited by the provider.

### `xml.etree.ElementTree.ParseError: syntax error`
This usually means the URL provided did not return valid XML. This happens if:
* The URL points to a standard HTML webpage instead of an RSS feed.
* The server returned a "Captcha" or "Login" page instead of the data.

### `UnhandledException: HTTP Error 404`
This error occurs when the URL provided is not a valid RSS endpoint.
* **Note**: Most homepages (e.g., `bbc.com`) are not RSS feeds.
* **Solution**: Search for the site's official RSS directory. For example, use `http://feeds.bbci.co.uk/news/rss.xml` for BBC News.

## Testing

To run the built-in doctests and ensure the parser is functioning correctly:
```bash
python -m doctest rss_reader.py
```

To check for PEP8 style compliance:
```bash
pycodestyle --max-line-length=120 rss_reader.py
```