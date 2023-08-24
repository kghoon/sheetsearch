# sheet-search

자연어 형태로 곡제목과 원하는 조성을 입력하면, ChatGPT API를 사용해 곡제목과 조성을 분리하고 Google Custom Search API를 사용해 악보 이미지를 검색합니다.
검색된 이미지 중에 원하는 악보를 선택하여 PDF로 생성할 수 있습니다.


## Environment Variables

- `PORT` - API search listening port (default: 8000)
- `OPENAI_API_KEY` - Open AI API key
- `CUSTOM_SEARCH_API_KEY` - Key for Google Custom Search API
- `CUSTOM_SEARCH_CX` - Search Engine ID of Google Custom Search

