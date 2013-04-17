# algorithms to data mine various search engines for the jobs links necessary



# This algorithm is written for http://www.dice.com jobs website.  I'm utilizing the mechanize
# module for emulating a web browser to crawl around their website and grab what I want.
# Once I've mined all I want, I return a list of Link objects.  Each object has attributes 
# that enable us to find out more about the specific URL.  For consistency, I will have all
# algorithms return a list of Link objects.

def return_jobs_from_dice(position, location):
    import mechanize
    import cookielib
    cj = cookielib.LWPCookieJar()
    br = mechanize.Browser()
    br.addheaders = [('User-Agent', 'Mozilla/5.0(X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_debug_http(True)
    br.set_debug_redirects(True)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_robots(False)
    br.open('http://www.dice.com')
    br.select_form(nr=0)
    br.form['FREE_TEXT'] = position
    br.form['WHERE'] = location
    br.submit()
    links = [i for i in br.links()]
    start_of_pages = links.index([i for i in links if i.text == '1'][0])
    stop_pages_index = None
    stop_link = [i for i in links if i.text == 'Next']
    if len(stop_link) > 0:
        stop_pages_index = links.index(stop_link[0])
    if stop_pages_index != None:
        pages = links[start_of_pages:stop_pages_index]
    else:
        pages = [links[start_of_pages]]
    start_of_jobs = links.index([i for i in links if i.text == 'Location'][0]) + 2
    stop_of_jobs  = links.index([i for i in links if i.text == '1'][0], start_of_jobs)
    jobs = links[start_of_jobs:stop_of_jobs]
    # parse other pages and get their links
    del pages[0]
    if len(pages) > 0:
        for i in pages:
            br.follow_link(i)
            current_links = [i for i in br.links()]
            start_of_jobs = current_links.index([i for i in current_links if i.text == 'Location'][0]) + 2
            stop_of_jobs = current_links.index([i for i in current_links if i.text == 'Prev'][0], start_of_jobs)
            current_page_jobs = current_links[start_of_jobs:stop_of_jobs]
            jobs += current_page_jobs
    # get rid of all the company and city links
    to_delete = []
    count = 0
    for j in range(len(jobs)):
        if j != count:
            to_delete.append(jobs[j])
        else:
            count = count + 3
    for obsolete in to_delete:
        del jobs[jobs.index(obsolete)]
    return jobs



############################################################################################################


# the algorithm for stack overflow jobs


def stack_jobs(position, location):
    import mechanize
    import cookielib
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.addheaders = [('User-Agent', 'Mozilla/5.0(X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_debug_http(True)
    br.set_debug_redirects(True)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_robots(False)
    br.open('http://careers.stackoverflow.com/jobs')
    br.select_form(nr=0)
    br.form['searchTerm'] = position
    br.form['location'] = location
    br.submit()
    links = [L for L in br.links()]
    jobs = []
    first_page = [i for i in links if i.text == '1']
    end_pages = [i for i in links if i.text == 'next']
    if len(first_page) == 0:
        start_cared_about = links.index([i for i in links if i.text == 'my profile'][0]) + 3
        stop_cared_about = links.index([i for i in links if i.text == 'view all'][0])
        jobs = links[start_cared_about:stop_cared_about]

    else:
        start_cared_about = links.index([i for i in links if i.text == 'my profile'][0]) + 3
        stop_cared_about = links.index([i for i in links if i.text == '1'][0], start_cared_about)
        jobs = links[start_cared_about:stop_cared_about]
        pages = links[links.index(first_page[0]): links.index(end_pages[0])]
        del pages[0]
        if len(pages) > 0:
            for i in pages:
                br.follow_link(i)
                cur_links = [e for e in br.links()]
                start_cared = cur_links.index([j for j in cur_links if j.text == 'my profile'][0]) + 3
                stop_cared = cur_links.index([j for j in cur_links if j.text == 'previous'][0], start_cared)
                jobs += cur_links[start_cared:stop_cared]
    # to delete the unnecessary links to languages
    # while there are still Link objects containing the parameters....
    while len([i for i in jobs if ('class', 'post-tag job-link') in i.attrs or ('class', 'fav-toggle') in i.attrs]) > 0:
        for i in jobs:
            if ('class', 'post-tag job-link') in i.attrs or ('class', 'fav-toggle') in i.attrs:
                del jobs[jobs.index(i)]
    return jobs
