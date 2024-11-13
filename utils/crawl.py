import bs4
import requests
import re

# get the list of the articles
def get_table(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    articles = soup.find('table')
    return articles

def get_header_row(table):
    header = table.find('thead')
    header = [cell.text.strip() for cell in header.find_all('th')]
    return header

def get_cell_td(cell):
    # Get all text, including handling scripts if necessary
    if cell.find('a'):
        onclick_function = cell.find('a')['onclick']
        
        # url link for the answer page
        onclick_function = re.search(r"'(.*)'", onclick_function).group(1)
        
        function_args = onclick_function.split(',')
        function_args = [t.strip().replace("'", '') for t in function_args]
        
        site_answer_link = "https://www.yangcheon.go.kr//site/mayor/ex/bbs/View.do?cbIdx=" + function_args[0] + "&bcIdx=" + function_args[1] + "&parentSeq=" + function_args[3]
        return site_answer_link

    else:
        text = cell.get_text(strip=True)
        return text

def get_body_rows(table):
    rows = []
    for row in table.find_all('tr')[1:]:  # Exclude the header row
        cells = []
        for cell in row.find_all('td'):
            # Get all text, including handling scripts if necessary
            text = get_cell_td(cell)
            cells.append(text)
        rows.append(cells)
    return rows

def get_dept_code(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    dept_code = soup.find_all('select', {'title' : "카테고리 선택"})

    dept_codes = dict([(option.text, option['value'].split('=')[-1]) for option in dept_code[0].find_all('option')])

    return dept_codes


# get the pages link
def get_page_indices(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    pages = soup.find('div', class_='pagination')

    # get only
    page_links = pages.find_all('a')\
    
    page_links = [link['href'].replace("?", "&") for link in page_links]
    return page_links

# the answer page link
def get_answer_page_link(table):

    a_tags = table.find_all('a')
    links = [a['onclick'] for a in a_tags]
    return links