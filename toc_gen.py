from bs4 import BeautifulSoup
import sys

def open_file():
    file = sys.argv[1]
    with open(file, 'r') as f:
        page = BeautifulSoup(f, 'html.parser')
    return page


def write_file(page):
    outfile = sys.argv[1][:-5] + "_out.html"
    with open(outfile, "w") as file:
        file.write(str(page))


def write_toc(ids):
    lines = ['<p><a href="{0}">{1}</a></p>\n'.format(i['id'], i['full']) for i in ids]
    for i in lines:
        print(lines)
    outfile = sys.argv[1][:-5] + "_toc.html"
    with open(outfile, "a") as file:
        for line in lines:
            file.write(line)


def get_existing_ids(ids):
    # ids = list containing dictionaries with 'id' and 'full' keys
    existing_ids = []
    for i in ids:
        existing_ids.append(i['id'])
    return existing_ids


def make_header_id(ids, header_base, header_split):
    if header_split:
        header_try = header_base + header_split[0]
        if header_try not in get_existing_ids(ids):
            return header_try
        else:
            try:
                return make_header_id(ids, header_try, header_split[1:])
            except indexError:
                return make_header_id(ids, header_try, None)
    else:
        return header_base + '1'


def main():
    page = open_file()
    ids = []
    for header in page.find_all('h2'):
        header_split = header.string.split()
        header_meta = {'full': header.string}
        if header_split[0] not in get_existing_ids(ids):
            header_meta['id'] = header_split[0]
        else:
            try:
                header_meta['id'] = make_header_id(ids, header_split[0], header_split[1:])
            except indexError:
                header_meta['id'] = make_header_id(ids, header_split[0], None)
        header['id'] = header_meta['id']
        ids.append(header_meta)

    write_file(page)
    write_toc(ids)


if __name__ == '__main__':
    main()