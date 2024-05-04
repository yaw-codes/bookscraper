import scrapy
from bookscraper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    #name of spider
    name = "bookspider"
    #domain we're scraping
    allowed_domains = ["books.toscrape.com"]
    #start domain
    start_urls = ["https://books.toscrape.com"]
    
    #using custom setting to store the file into a local directory
    custom_settings = {
        'FEEDS' : {
    'bookdata.json' : {'format':'json', 'overwrite': True}
    } 
        }

    def parse(self, response):
        #the response we get is stored in a response variable so we extract the individual books into book variable from response
        books = response.css("article.product_pod")
        
        #iterating through every book
        for book in books:
            #getting the urls of the individual books from the page to get more data
            relative_url = book.css('h3 a::attr(href)').get() #href attribute to get the links
                
             #check the url to see if it has catalogue else add it   
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            
            #opens the urls of the book and extracts data using the  parse_book_page fxn
            yield response.follow(book_url,callback = self.parse_book_page)
        
        #use this to go to the website's next page  
        next_page = response.css('li.next a::attr(href)').get()
        
        #Checking to see if there is catalogue in url
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_Url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_Url = 'https://books.toscrape.com/catalogue/' + next_page
            
            #Following the various pages to get the data
            yield response.follow(next_page_Url,callback = self.parse)
            
    #Parsing the book page to get data
    def parse_book_page(self, response):
        #storing the table row from the individual book pages
        table_rows = response.css("table tr")
        
        #using BookItem to categorize the data and store it well
        book_item = BookItem()
        
        #extracting the various data using css selectors and xpath
        book_item['url'] =response.url,
        book_item['title']= response.css(".product_main h1::text").get(),
        book_item['upc'] = table_rows[0].css('td ::text').get(),
        book_item['product_type']= table_rows[1].css('td ::text').get(),
        book_item['price_excl_tax']= table_rows[2].css('td ::text').get(),
        book_item['price_incl_tax']= table_rows[3].css('td ::text').get(),
        book_item['tax']= table_rows[4].css('td ::text').get(),
        book_item['availability']= table_rows[5].css('td ::text').get(),
        book_item['num_reviews']= table_rows[6].css('td ::text').get(),
        book_item['stars']=response.css('p.star-rating').attrib['class'],
        book_item['category']= response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item['description']=response.xpath("//div[@id ='product_description']/following-sibling ::p/text()").get(),
        book_item['price']=response.css('p.price_color ::text').get(),
        
        yield book_item
        
        
        
        
        
# #saving mysql pipline
# import mysql.connector
# class SaveToMySQLPipelines:
#     def __init__(self) :
#         self.com = mysql.connector.connect(
#             host = 'localhost',
#             user = 'root',
#             password = '',#add your password here if you have one set
#             database = 'books',
#         )
#         ## create cursor, used to execute commands
#         self.cur = self.conn.cursor()
        
#         ## create books table if none exists
#         self.cur.execute("""
#                             CREATE TABLE IF NOT EXISTS books(
#                                 id int NOT NULL auto_increment,
#                                 url VARCHAR(255),
#                                 title text,
#                                 upc VARCHAR(255),
#                                 product_type VARCHAR(255),
#                                 product_excl_tax DECIMAL,
#                                 product_incl_tax DECIMAL,
#                                 tax DECIMAL,
#                                 price DECIMAL,
#                                 availability INTEGER,
#                                 num_reviews INTEGER,
#                                 stars INTEGER,
#                                 category VARCHAR(255),
#                                 description text,
#                                 PRIMARY KEY (id)
#                                 )""")
        
        
#     #use insert into the mysql database using process_item to insert the data that we have in our item
    
#     def process_item(self, item, spider):
#         #Define insert statement 
#         self.cur.execute(""" insert into books (
#             url,
#             title,
#             upc,
#             product_type,
#             price_excl_tax,
#             price_incl_tax,
#             tax,
#             price,
#             availability,
#             num_reviews,
#             stars,
#             category,
#             description
#             ) values(
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,
#                 %s,

                
#             )
#                          """, (
#             item['url'] ,
#             item['title'],
#             item['upc'] ,
#             item['product_type'],
#             item['price_excl_tax'],
#             item['price_incl_tax'],
#             item['tax'],
#             item['availability'],
#             item['num_reviews'],
#             item['stars'],
#             item['category'],
#             str(item['description'][0]),
#             item['price'],
#             )
#         )
        
#         ## Execute insert of data into database
#         self.conn.commit()
        
#         return item
    
#     ## we want the connection closed once the spider is finished
    
#     def close_spider(self,spider):
#         ##close cursor & connection to database
#         self.cur.close()
#         self.conn.close()
        
                    