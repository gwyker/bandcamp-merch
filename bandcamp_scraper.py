import requests as rq
from pprint import pprint
from bs4 import BeautifulSoup
from collections import defaultdict
from tqdm import tqdm


DEFAULT_TAG = 'scenecore'
HEADERS_MOBILE = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}


def get_merch_urls(tag):
    """ Get all urls for a tag. """
    camps = set()
    for page in tqdm(range(1, 11)):
        bc_url = f'https://bandcamp.com/tag/{tag}?page={page}&sort_field=date'
        r = rq.get(bc_url, headers=HEADERS_MOBILE)
        soup = BeautifulSoup(r.content, 'html.parser')
        atags = soup.find_all('a')
        camp_urls = [a['href'] for a in atags if a.has_attr('title')]
        for url in camp_urls:
            merch_url = 'https://'+url.split('/')[2]+'/merch'
            camps.add(merch_url)
    return list(camps)


def validate_merch_url(url):
    """Validate that a merch page url exists."""
    r = rq.get(url)
    return r.url == url


def get_item_cells(merch_url):
    """ Get CELLS of all items in a merch page. """
    r = rq.get(merch_url)
    if r.url != merch_url:
        print(r.url)
        return []
    soup = BeautifulSoup(r.content, 'html.parser')
    cells = soup.find_all('li')
    cells = [c for c in cells if c.has_attr('class') and 'merch-grid-item' in c['class']]
    return cells


def create_html(merch_urls, tag):
    """Create the html for a certain tag."""
    all_cells = []
    out_soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
    print('Getting merch cells')
    for i, merch_url in enumerate(tqdm(merch_urls)):
        band = merch_url.split('.')[0].split('//')[1]
        cells = get_item_cells(merch_url)
        if not cells:
            continue
        # Drop if sold out
        cells = [c for c in cells if not (c.find(class_='price').string and 'out' in c.find(class_='price').string.lower())]
        for c in cells:
            # Switch href of the art tag to use the actual bcbits img
            img = c.find(class_='art').img
            if img.has_attr('data-original'):
                img['src'] = img['data-original']
            # Edit hrefs of album names to link correctly
            a = c.find('a')
            base_url = merch_url.replace('/merch', '')
            if 'http' not in a['href']:
                a['href'] = f'{base_url}{a["href"]}'
            # Remove whitespace in divs and add band name
            div = c.find(class_='secondaryText')
            if div.string:
                div.string.replace_with(div.string.replace('\n', ''))
            # Add band name
            name_tag = out_soup.new_tag('div')
            name_tag.string = band
            name_tag['class'] = 'bandname'
            c.insert(0, name_tag)

        all_cells.extend(cells)

    def sortfunc(c):
        s = c.find(class_='merchtype').string
        band = c.find(class_='bandname').string
        return (s, band) if s else ('zzzzz', 'zzzzz')

    print('Total cells:', len(all_cells))
    all_cells = sorted(all_cells, key=sortfunc, reverse=True)
    ol_tag = out_soup.new_tag('ol')
    ol_tag.extend(all_cells)
    head = out_soup.head
    # out_soup.style = cells[0].parent.parent
    # print(cells[0].parent)
    head.append(out_soup.new_tag('style', type='text/css'))
    head.style.append('li {'
                      'display:inline-block;'
                      'vertical-align:top;'
                      'margin:0 26px 30px 0;'
                      'position:relative;'
                      'width:270px;'
                      '}')
    head.style.append('a {'
                      'text-decoration:none !important;'
                      '}')
    head.style.append('a {'
                      'padding:0px;'
                      '}')
    head.style.append('ol {'
                      'margin: 0 auto;'
                      'text-align: center;}')
    head.style.append('img {'
                      'width: 270px;}')
    head.style.append('body {'
                      'background: #202020;'
                      'color:#d7d7d7;'
                      'line-height:.9;'
                      '}')
    # 5d9ae1
    head.style.append('.title {'
                      'color: #5d9ae1;}')
    head.style.append('.bandname {'
                      'padding: 8px;'
                      'color: #c2b1e3;'
                      'font-size: 19px;'
                      '}')
    head.style.append('.merchtype {'
                      'color: #76d2de;}')
    head.append(out_soup.new_tag('body'))
    head.body.append(ol_tag)
    print('writing')
    html_path = f'{tag.replace("-", "_")}_merch.html'
    with open(html_path, 'w') as f:
        f.write(str(out_soup))
    print('writed')


def create_html_grid(merch_urls, tag):
    """Create the html grid (top-level <ol> with tab ids) for a certain tag."""
    all_cells = []
    out_soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
    print('Getting merch cells')
    for i, merch_url in enumerate(tqdm(merch_urls)):
        band = merch_url.split('.')[0].split('//')[1]
        cells = get_item_cells(merch_url)
        if not cells:
            continue
        # Drop if sold out
        cells = [c for c in cells if
                 not (c.find(class_='price').string and 'out' in c.find(class_='price').string.lower())]
        for c in cells:
            # Switch href of the art tag to use the actual bcbits img
            img = c.find(class_='art').img
            if img.has_attr('data-original'):
                img['src'] = img['data-original']
            # Edit hrefs of album names to link correctly
            a = c.find('a')
            base_url = merch_url.replace('/merch', '')
            if 'http' not in a['href']:
                a['href'] = f'{base_url}{a["href"]}'
            # Remove whitespace in divs and add band name
            div = c.find(class_='secondaryText')
            if div.string:
                div.string.replace_with(div.string.replace('\n', ''))
            # Add band name
            name_tag = out_soup.new_tag('div')
            name_tag.string = band
            name_tag['class'] = 'bandname'
            c.insert(0, name_tag)

        all_cells.extend(cells)

    def sortfunc(c):
        s = c.find(class_='merchtype').string
        band = c.find(class_='bandname').string
        return (s, band) if s else ('zzzzz', 'zzzzz')

    print('Total cells:', len(all_cells))
    all_cells = sorted(all_cells, key=sortfunc, reverse=True)
    ol_tag = out_soup.new_tag('ol', id=tag)
    ol_tag['class'] = 'tabcontent'
    ol_tag.style = out_soup.new_tag('style')
    ol_tag.extend(all_cells)
    head = out_soup.head
    # out_soup.style = cells[0].parent.parent
    # print(cells[0].parent)
    head.append(out_soup.new_tag('style', type='text/css'))
    head.style.append('li {'
                      'display:inline-block;'
                      'vertical-align:top;'
                      'margin:0 26px 30px 0;'
                      'position:relative;'
                      'width:270px;'
                      '}')
    head.style.append('a {'
                      'text-decoration:none !important;'
                      '}')
    head.style.append('a {'
                      'padding:0px;'
                      '}')
    head.style.append('ol {'
                      'margin: 0 auto;'
                      'text-align: center;}')
    head.style.append('img {'
                      'width: 270px;}')
    head.style.append('body {'
                      'background: #202020;'
                      'color:#d7d7d7;'
                      'line-height:.9;'
                      '}')
    # 5d9ae1
    head.style.append('.title {'
                      'color: #5d9ae1;}')
    head.style.append('.bandname {'
                      'padding: 8px;'
                      'color: #c2b1e3;'
                      'font-size: 19px;'
                      '}')
    head.style.append('.merchtype {'
                      'color: #76d2de;}')
    head.append(out_soup.new_tag('body'))
    head.body.append(ol_tag)
    print('writing')
    html_path = f'bc_merch_html/grids/{tag.replace("-", "_")}_merch_grid.html'
    with open(html_path, 'w') as f:
        f.write(str(out_soup.ol))
    print('writed')


def create_html_grid(merch_urls, tag):
    """Create the html grid (top-level <ol> with tab ids) for a certain tag."""
    all_cells = []
    out_soup = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
    print('Getting merch cells')
    for i, merch_url in enumerate(tqdm(merch_urls)):
        band = merch_url.split('.')[0].split('//')[1]
        cells = get_item_cells(merch_url)
        if not cells:
            continue
        # Drop if sold out
        cells = [c for c in cells if
                 not (c.find(class_='price').string and 'out' in c.find(class_='price').string.lower())]
        for c in cells:
            # Switch href of the art tag to use the actual bcbits img
            img = c.find(class_='art').img
            if img.has_attr('data-original'):
                img['src'] = img['data-original']
            # Edit hrefs of album names to link correctly
            a = c.find('a')
            base_url = merch_url.replace('/merch', '')
            if 'http' not in a['href']:
                a['href'] = f'{base_url}{a["href"]}'
            # Remove whitespace in divs and add band name
            div = c.find(class_='secondaryText')
            if div.string:
                div.string.replace_with(div.string.replace('\n', ''))
            # Add band name
            name_tag = out_soup.new_tag('div')
            name_tag.string = band
            name_tag['class'] = 'bandname'
            c.insert(0, name_tag)

        all_cells.extend(cells)

    def sortfunc(c):
        s = c.find(class_='merchtype').string
        band = c.find(class_='bandname').string
        return (s, band) if s else ('zzzzz', 'zzzzz')

    print('Total cells:', len(all_cells))
    all_cells = sorted(all_cells, key=sortfunc, reverse=True)
    ol_tag = out_soup.new_tag('ol', id=tag)
    ol_tag['class'] = 'tabcontent'
    ol_tag.style = out_soup.new_tag('style')
    ol_tag.extend(all_cells)
    head = out_soup.head
    # out_soup.style = cells[0].parent.parent
    # print(cells[0].parent)
    head.append(out_soup.new_tag('style', type='text/css'))
    head.style.append('li {'
                      'display:inline-block;'
                      'vertical-align:top;'
                      'margin:0 26px 30px 0;'
                      'position:relative;'
                      'width:270px;'
                      '}')
    head.style.append('a {'
                      'text-decoration:none !important;'
                      '}')
    head.style.append('a {'
                      'padding:0px;'
                      '}')
    head.style.append('ol {'
                      'margin: 0 auto;'
                      'text-align: center;}')
    head.style.append('img {'
                      'width: 270px;}')
    head.style.append('body {'
                      'background: #202020;'
                      'color:#d7d7d7;'
                      'line-height:.9;'
                      '}')
    # 5d9ae1
    head.style.append('.title {'
                      'color: #5d9ae1;}')
    head.style.append('.bandname {'
                      'padding: 8px;'
                      'color: #c2b1e3;'
                      'font-size: 19px;'
                      '}')
    head.style.append('.merchtype {'
                      'color: #76d2de;}')
    head.append(out_soup.new_tag('body'))
    head.body.append(ol_tag)
    print('writing')
    html_path = f'bc_merch_html/grids/{tag.replace("-", "_")}_merch_grid.html'
    with open(html_path, 'w') as f:
        f.write(str(out_soup.ol))
    print('writed')


def scrape_tag(tag=None):
    if tag is None:
        tag = DEFAULT_TAG
    print(f'Running {tag} tag')
    # Get urls
    print('Getting band urls...')
    merch_urls = get_merch_urls(tag)
    print('Bands found:', len(merch_urls))

    # # Validate urls
    # print('Validating urls')
    # valid_urls = []
    # for url in tqdm(merch_urls):
    #     if validate_merch_url(url):
    #         valid_urls.append(url)
    #
    # print('Valid urls:', len(merch_urls))

    # Create html
    create_html_grid(merch_urls, tag)


if __name__ == "__main__":
    # tags = ['hardcore', 'black-metal','death-metal', 'thrash-metal', 'grindcore', 'doom', 'post-hardcore',
    #         'progressive-metal', 'metalcore', 'sludge-metal','heavy-metal', 'deathcore', 'noise']
    tags = ['noise']
    for tag in tags:
        scrape_tag(tag)