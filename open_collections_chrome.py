import time
import webbrowser

from google_sheets import get_google_sheet_data


def open_collections(range_urls):
    urls = get_google_sheet_data(range_urls)
    urls_counter = 0
    for url in urls:
        urls_counter += 1
        webbrowser.open(url[0], new=2, autoraise=False)
        time.sleep(0.5)
        if urls_counter == 10:
            answer = input("Дальше?")
            if answer == "n":
                break
            urls_counter = 0


if __name__ == "__main__":
    open_collections("H2:H31")
