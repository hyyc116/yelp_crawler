__author__ = 'Lucas Ou-Yang, Mathew Sprehn'
__date__ = 'July 4th, 2013'
"""
We can be suboptimal, eg: like parse w/ beautifulsoup and not use mthreading
because Yelp will rate limit us anyways. This entire project was just for
fun, there are better scraping solutions out there and scraping yelp is
looked down upon anyways, read their robots.txt.

Check out my main scraping project, newspaper, for news extraction!
https://github.com/codelucas/newspaper
"""
from BeautifulSoup import BeautifulSoup
from urlparse import urljoin
import urllib2
import argparse
import re
import codecs
import time
import random
from collections import defaultdict
import json

get_yelp_page = \
    lambda zipcode, page_num: \
        'https://www.yelp.com/search?find_loc={0}&start={1}'.format(zipcode, page_num)

ZIP_URL = "zipcodes.txt"
FIELD_DELIM = u'###'
LISTING_DELIM = u'((('

def get_zips():
    """
    """
    f = open(ZIP_URL, 'r+')
    zips = [int(zz.strip()) for zz in f.read().split('\n') if zz.strip() ]
    f.close()
    return zips

def crawl_page(zipcode, page_num, verbose=False):
    """
    This method takes a page number, yelp GET param, and crawls exactly
    one page. We expect 10 listing per page.
    """
    try:
        page_url = get_yelp_page(zipcode, page_num)
        print page_url
        soup = BeautifulSoup(urllib2.urlopen(page_url).read())
    except Exception, e:
        print str(e)
        return []

    # print 'test'

    restaurants = soup.findAll('div', attrs={'class':re.compile
            (r'^search-result natural-search-result')})

    # print len(restaurants)

    # try:
    #     assert(len(restaurants) == 10)
    # except AssertionError, e:
    #     # We make a dangerous assumption that yelp has 10 listing per page,
    #     # however this can also be a formatting issue, so watch out
    #     print 'we have hit the end of the zip code', str(e)
    #     # False is a special flag, returned when quitting
    #     return [], False

    extracted = [] # a list of tuples
    for r in restaurants:
        img = ''
        yelpPage = ''
        title = ''
        rating = ''
        addr = ''
        phone = ''
        categories = ''
        review_count = ''
        price_range = ''

        try:
            img = r.div('div', {'class':'media-avatar'})[0].img['src']
        except Exception, e:
            if verbose: print 'img extract fail', str(e)

        # print img

        try:
            title = r.find('a', {'class':'biz-name js-analytics-click'}).getText()
        except Exception, e:
            if verbose: print 'title extract fail', str(e)

        # print title

        try:
            yelpPage = r.find('a', {'class':'biz-name js-analytics-click'})['href']
        except Exception, e:
            if verbose: print 'yelp page link extraction fail', str(e)
            continue

        # print yelpPage
        # print

        try:
            categories = r.findAll('span', {'class':'category-str-list'})
            categories = ', '.join([c.getText() for c in categories if c.getText()])
        except Exception, e:
            if verbose: print "category extract fail", str(e)

        # print categories

        try:
            rating = r.find('div', {'class':re.compile(r'^i-stars i-stars--regular')})['title']
        except Exception, e:
            if verbose: print 'rating extract fail', str(e)

        # print rating

        try:
            addr = r.find('div', {'class':'secondary-attributes'}).address.getText()
        except Exception, e:
            if verbose: print 'address extract fail', str(e)

        # print addr

        try:
            phone = r.find('span', {'class':'biz-phone'}).getText()
        except Exception, e:
            if verbose: print 'phone extract fail', str(e)

        # print phone

        # review-count rating-qualifier
        try:
            review_count = r.find('span', {'class':'review-count rating-qualifier'}).getText()
        except Exception, e:
            if verbose: print 'review count extract fail', str(e)

        # print review_count

        #business-attribute price-range
        try:
            price_range = r.find('span', {'class':'business-attribute price-range'}).getText()
        except Exception, e:
            if verbose: print 'price range extract fail', str(e)

        # print price_range

        extracted.append([img,yelpPage,title,rating,addr,phone,categories,review_count,price_range])

        time.sleep(random.randint(1, 2) * .931467298)

        # return
        # try:
        #     soup2 = BeautifulSoup(urllib2.urlopen(urljoin('http://www.yelp.com',
        #                                                 yelpPage)).read())
        #     r2 = soup2.find('div', {'class':'main-content-wrap main-content-wrap--full'})
        #     try:
        #         price = r2.find('dd', {'class':'business-attribute price-range'}).getText()
        #     except Exception, e:
        #         if verbose: print 'price extract fail', str(e)

        #     print price

        #     try:
        #         creditCards = soup2.find('dd',
        #             {'class':'attr-BusinessAcceptsCreditCards'}).getText()
        #     except Exception, e:
        #         if verbose: print 'creditCard extract fail', str(e)
        #     try:
        #         parking = soup2.find('dd', {'class':'attr-BusinessParking'}).getText()
        #     except Exception, e:
        #         if verbose: print 'parking extract fail', str(e)
        #     try:
        #         attire = soup2.find('dd', {'class':'attr-RestaurantsAttire'}).getText()
        #     except Exception, e:
        #         if verbose: print 'attire extract fail', str(e)
        #     try:
        #         groups = soup2.find('dd', {'class':'attr-RestaurantsGoodForGroups'}).getText()
        #     except Exception, e:
        #         if verbose: print 'groups extract fail', str(e)
        #     try:
        #         kids = soup2.find('dd', {'class':'attr-GoodForKids'}).getText()
        #     except Exception, e:
        #         if verbose: print 'kids extract fail', str(e)
        #     try:
        #         reservations = soup2.find('dd',
        #             {'class':'attr-RestaurantsReservations'}).getText()
        #     except Exception, e:
        #         if verbose: print 'reservations extract fail', str(e)
        #     try:
        #         delivery = soup2.find('dd', {'class':'attr-RestaurantsDelivery'}).getText()
        #     except Exception, e:
        #         if verbose: print 'delivery extract fail', str(e)
        #     try:
        #         takeout = soup2.find('dd', {'class':'attr-RestaurantsTakeOut'}).getText()
        #     except Exception, e:
        #         if verbose: print 'takeout extract fail', str(e)
        #     try:
        #         waiterService = soup2.find('dd',
        #                 {'class':'attr-RestaurantsTableService'}).getText()
        #     except Exception, e:
        #         if verbose: print 'waiterService extract fail', str(e)
        #     try:
        #         outdoor = soup2.find('dd', {'class':'attr-OutdoorSeating'}).getText()
        #     except Exception, e:
        #         if verbose: print 'outdoor extract fail', str(e)
        #     try:
        #         wifi = soup2.find('dd', {'class':'attr-WiFi'}).getText()
        #     except Exception, e:
        #         if verbose: print 'wifi extract fail', str(e)
        #     try:
        #         goodFor = soup2.find('dd', {'class':'attr-GoodForMeal'}).getText()
        #     except Exception, e:
        #         if verbose: print 'goodFor extract fail', str(e)
        #     try:
        #         alcohol = soup2.find('dd', {'class':'attr-Alcohol'}).getText()
        #     except Exception, e:
        #         if verbose: print 'alcohol extract fail', str(e)
        #     try:
        #         ambience = soup2.find('dd', {'class':'attr-Ambience'}).getText()
        #     except Exception, e:
        #         if verbose: print 'ambience extract fail', str(e)
        #     try:
        #         tv = soup2.find('dd', {'class':'attr-HasTV'}).getText()
        #     except Exception, e:
        #         if verbose: print 'tv extract fail', str(e)
        #     try:
        #         caters = soup2.find('dd', {'class':'attr-Caters'}).getText()
        #     except Exception, e:
        #         if verbose: print 'caters extract fail', str(e)
        #     try:
        #         wheelchairAccessible = soup2.find('dd',
        #             {'class':'attr-WheelchairAccessible'}).getText()
        #     except Exception, e:
        #         if verbose: print 'wheelchairAccessible extract fail', str(e)

        # except Exception, e:
            # if verbose: print "**failed to get you a page", str(e)

        # if title: print 'title:', title
        # if categories: print 'categories:', categories
        # if rating: print 'rating:', rating
        # if img: print 'img:', img
        # if addr: print 'address:', addr
        # if phone: print 'phone:', phone
        # if price: print 'price:', price
        # if menu: print 'menu:', menu
        # if creditCards: print 'creditCards:', creditCards
        # if parking: print 'parking:', parking
        # if attire: print 'attire:', attire
        # if groups: print 'groups:', groups
        # if kids: print 'kids:', kids
        # if reservations: print 'reservations:', reservations
        # if delivery: print 'delivery:', delivery
        # if takeout: print 'takeout:', takeout
        # if waiterService: print 'waiterService:', waiterService
        # if outdoor: print 'outdoor:', outdoor
        # if wifi: print 'wifi:', wifi
        # if goodFor: print 'goodFor:', goodFor
        # if alcohol: print 'alcohol:', alcohol
        # if noise: print 'noise:', noise
        # if ambience: print 'ambience:', ambience
        # if tv: print 'tv:', tv
        # if caters: print 'caters:', caters
        # if wheelchairAccessible: print 'wheelchairAccessible:', wheelchairAccessible

        # print '=============='
        # extracted.append((title, categories, rating, img, addr, phone, price, menu,
        #    creditCards, parking, attire, groups, kids, reservations, delivery, takeout,
        #    waiterService, outdoor, wifi, goodFor, alcohol, noise, ambience, tv, caters,
        #    wheelchairAccessible))
    if len(restaurants)==10:
        return extracted, True
    else:
        return extracted,False

def crawl(zipcode=None):
    page = 0
    some_zipcodes = [zipcode] if zipcode else get_zips()

    crawled_zipcodes = set()
    for line in open('crawled_zipcode.txt'):
        crawled_zipcodes.add(line.strip())

    f = open('yelp_data.json','w+')
    zf = open('crawled_zipcode.txt','w+')

    if zipcode is None:
        print '\n**We are attempting to extract all zipcodes in America!**'

    for zipcode in some_zipcodes:
        flag = True

        if zipcode in crawled_zipcodes:
            print '\n=== <', zipcode ,'> already crawled.====\n'
            continue

        print '\n===== Attempting extraction for zipcode <', zipcode, '>=====\n'
        data = defaultdict(list)
        while flag:
            # print '----page',page,'----'
            extracted, flag = crawl_page(zipcode, page,True)
            if not flag:
                print 'extraction stopped or broke at zipcode'
                break


            data[zipcode].extend(extracted)

            page += 10
            time.sleep(random.randint(1, 2) * .931467298)

        print 'writing to yelp_data.json.'
        f.write(json.dumps(data)+'\n')
        zf.write(str(zipcode)+'\n')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracts all yelp restaurant \
        data from a specified zip code (or all American zip codes if nothing \
        is provided)')
    parser.add_argument('-z', '--zipcode', type=int, help='Enter a zip code \
        you\'t like to extract from.')
    args = parser.parse_args()
    crawl(args.zipcode)
