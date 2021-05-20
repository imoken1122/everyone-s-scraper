import twint
import datetime as dt
def Twitter_Scraper(search_word,since_date,until_date,output_filename):
    c = twint.Config
    c.Search = search_word
    c.Store_json = True
    c.Output = output_filename
    c.Since = since_date
    c.Until = until_date
    #c.Hide_output = True
    twint.run.Search(c)

Twitter_Scraper("おかえりモネ", "2021-05-16 00:00:00", "2021-05-17 13:00:00","twint_scrape.json")

