# algorithms to data mine various search engines for the jobs links necessary

# the problem of redundant links is not yet implemented


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

#### ++++++++++++++++++++++++++++++++++++++ #######
# AMENDED DICE ALGORITHM

def return_jobs_from_dice2(position, location):
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
    jobs = []
    links = [i for i in br.links()]
    if len(links) > 60:
        start = links.index([i for i in links if i.text == 'Location'][0])+2
        stop = links.index([i for i in links if i.text == '1'][0], start)
        jobs += links[start:stop]
        while len([e for e in br.links() if e.text == 'Next']) > 0:
            br.follow_link([e for e in br.links() if e.text == 'Next'][0])
            current_links = [j for j in br.links()]
            cur_start = current_links.index([l for l in current_links if l.text == 'Location'][0])+2
            cur_end = current_links.index([l for l in current_links if l.text == 'Prev'][0], cur_start)
            jobs += current_links[cur_start:cur_end]
        while len([i for i in jobs if len(i.attrs) > 1]) > 0:
            for e in jobs:
                if len(e.attrs) > 1:
                    del jobs[jobs.index(e)]
    else:
        jobs = []

    return jobs


############################################################################################################


# the algorithm for stack overflow jobs
# this algorithm employs similar protocols as the return_jobs_from_dice alg
# what is returned by both is a list object called jobs containing a bunch of
# mechanize-generated Link objects


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
    while len([i for i in jobs if ('class', 'title job-link') not in i.attrs]) > 0:
        for i in jobs:
            if ('class', 'title job-link') not in i.attrs:
                del jobs[jobs.index(i)]
    return jobs


#####################################################################################################


# This monster.com algorithm had to employ some different techniques than dice and stack overflow
# due to the nature of ASP.NET, which is what monster uses.  Rather than directly opening
# a job search engine website and populating form data like before, I had to utilize an API
# and make calls to that after some slight string manipulation conforming to their specifications


# This algorithm also returns a list object of mechanize Link objects



def get_monster_jobs(position, location):
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
    monster_api = 'http://jobsearch.monster.com/search/?q={0}&where={1}'
    position = position.replace(' ', '-')
    position = position.replace(',', '__2C')
    location = location.replace(' ', '-')
    location = location.replace(',', '__2C')
    br.open(monster_api.format(position, location))
    links = [i for i in br.links()]
    jobs = []
    first_page = [i for i in links if i.text =='1']
    end_page = [i for i in links if i.text =='Next']
    if len(first_page) == 0:
        start_jobs = links.index([i for i in links if i.text == 'Advanced Search'][0]) + 1
        stop = links.index([i for i in links if i.text == '(Hiring Now) Local Jobs'][0]) - 2
        jobs += links[start_jobs:stop]
    else:
        start_jobs = links.index([i for i in links if i.text == 'Advanced Search'][0]) + 1
        stop = links.index([i for i in links if i.text == '1'][0])
        jobs += links[start_jobs:stop]
        pages = links[links.index(first_page[0]): links.index(end_page[0])]
        del pages[0]
        if len(pages) > 0:
            for i in pages:
                br.follow_link(i)
                current_links = [e for e in br.links()]
                start_jobs = current_links.index([i for i in current_links if i.text == 'Advanced Search'][0]) + 1
                #stop_jobs = current_links.index([i for i in current_links if i.text == '(Hiring Now) Local Jobs'][0]) - 2
                to_parse = current_links[start_jobs:]
    while len([i for i in jobs if ('class', 'slJobTitle fnt11') not in i.attrs or ('class', 'slJobTitle') not in i.attrs]) > 0:
        for e in jobs:
            if ('class', 'slJobTitle fnt11') not in e.attrs and ('class', 'slJobTitle') not in e.attrs:
                del jobs[jobs.index(e)]
    return jobs


#++++++++++++++++++++ AMENDED MONSTER JOBS ALGORITHM +++++++++++++++++++++++++


def get_monster_jobs2(position, location):
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
    monster_api = 'http://jobsearch.monster.com/search/?q={0}&where={1}'
    position = position.replace(' ', '-')
    position = position.replace(',', '__2C')
    location = location.replace(' ', '-')
    location = location.replace(',', '__2C')
    br.open(monster_api.format(position, location))
    links = [i for i in br.links()]
    jobs = []
    start = links.index([e for e in links if e.text == 'Advanced Search'][0])
    if len([e for e in links if e.text == 'Next']) > 0:
        stop = links.index([j for j in links if j.text == 'Next'][0], start)
    else:
        stop = links.index([e for e in links if e.text == 'Resume Distribution'][0], start)
    
    jobs += links[start:stop]
    #first_page = [i for i in links if i.text =='1']
    #end_page = [i for i in links if i.text =='Next']
    while len([e for e in br.links() if e.text == 'Next']) > 0:
        br.follow_link([e for e in br.links() if e.text == 'Next'][0])
        current_links = [i for i in br.links()]
        start_jobs = current_links.index([e for e in current_links if e.text == 'Advanced Search'][0])
        stop_jobs = current_links.index([j for j in current_links if j.text == 'Previous'][0], start_jobs)
        jobs += current_links[start_jobs:stop_jobs]
    while len([i for i in jobs if ('class', 'slJobTitle') not in i.attrs]) > 0:
        for e in jobs:
            if ('class', 'slJobTitle') not in e.attrs:
                del jobs[jobs.index(e)]
    return jobs


#################################################################################################################333



# Similar to other mining algorithms, with the exception of monster, but alike in the final cleansing,
# the algorithm for careerbuilder followed suite with regard to algorithmic structure.

# the algorithm returns a list object of mechanize Link objects

def get_careerbuilder_jobs(position, location):
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
    br.open('http://www.careerbuilder.com')
    br.select_form(nr=0)
    br.form['s_rawwords'] = position
    br.form['s_freeloc'] = location
    br.submit()
    jobs = []
    links = [i for i in br.links()]
    if len([e for e in links if ('id', 'AskForCatSubmit') in e.attrs]) == 0:
        # starting index of desired after links within the links on the current page
        start =links.index([i for i in links if i.text == 'Posted'][0])
        stop = links.index([i for i in links if i.text == 'Cancel'][0], start)
        jobs += links[start:stop]
        while len([i for i in br.links() if i.text == 'Next Page']) > 0:
            br.follow_link([i for i in br.links() if i.text == 'Next Page'][0])
            current_links = [e for e in br.links()]
            start_jobs = current_links.index([j for j in current_links if j.text == 'Posted'][0])
            stop_jobs = current_links.index([j for j in current_links if j.text == 'Cancel'][0])
            jobs += current_links[start_jobs:stop_jobs]
        
        # now we need to clean up our jobs list and get rid of all erroneous links
        while len([i for i in jobs if ('class', 'jt prefTitle') not in i.attrs]) > 0:
            for link in jobs:
                if ('class', 'jt prefTitle') not in link.attrs:
                    del jobs[jobs.index(link)]
    else:
        jobs = []
    return jobs


######################################################################################

# indeed.com data mining algorithm was also very similar in architechture
# it returns the same data as all the others


def get_indeed_jobs(position, location):
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
    jobs = []
    br.open('http://www.indeed.com')
    # form stuff
    br.select_form(nr=0)
    br.form['q'] = position
    br.form['l'] = location
    br.submit()
    # links
    links = [i for i in br.links()]
    start = links.index([e for e in links if e.text == 'Post your resume'][0])
    if len([e for e in links if e.text == 'Next\xc2\xa0\xc2\xbb']) > 0:
        stop = links.index([e for e in links if e.text == '2'][0], start)
    else:
        stop = links.index([e for e in links if e.text == 'Jobs'][0], start)
    jobs += links[start:stop]
    while len([e for e in br.links() if e.text == 'Next\xc2\xa0\xc2\xbb']) > 0:
        br.follow_link([i for i in br.links() if i.text == 'Next\xc2\xa0\xc2\xbb'][0])
        current_links = [a for a in br.links()]
        start = current_links.index([e for e in current_links if e.text == 'Post your resume'][0])
        stop = current_links.index([e for e in current_links if e.text == 'Jobs'][0])
        jobs += current_links[start:stop]
    while len([i for i in jobs if ('itemprop', 'title') not in i.attrs]) > 0:
        for link in jobs:
            if ('itemprop', 'title') not in link.attrs:
                del jobs[jobs.index(link)] 
    return jobs




##############################################################################################################################################################################################################################################################################################################################################################################################################

# VERSION 2 OF ALGORITHMS



# stack
# returns a dictionary with job_url as key and title, company, duration been posted as values

def get_stack_v2(position, location):
    import urllib2
    # have job be a global for all algorithms to add to
    jobs = {}
    stack_api = 'http://careers.stackoverflow.com/jobs?searchTerm={0}&location={1}'
    position = position.replace(' ', '+')
    location = location.replace(',', '%2C')
    location = location.replace(' ', '+')
    formatted = stack_api.format(position, location)
    f = urllib2.urlopen(formatted)
    f1 = f.read().split('\n')
    f1 = [i.split('\r') for i in f1]
    page = 1
    #if f1[119][0].find('title') != -1:
    if len([e for e in f1 if '<a class="title job-link"' in e[0]]) > 0:
        while len([e for e in f1 if '<a class="title job-link"' in e[0]]) > 0:
            indexes = [f1.index(e) for e in f1 if '<a class="title job-link"' in e[0] or '<a class="title job-link abbrev"' in e[0]]
            for index in indexes:
                base_url = 'http://careers.stackoverflow.com'
                # url concatenation stuff
                start = f1[index][0].find('/')
                stop = f1[index][0].find('title=')-2
                add_url = f1[index][0][start:stop]
                job_url = base_url+add_url
                # job title stuff
                start_title = stop+9
                stop_title = f1[index][0].find('"', start_title)
                title = f1[index][0][start_title:stop_title]
                # company stuff
                comp = f1[index+3][0]
                comp_new = [e for e in comp if not e.isspace()]
                company = ''.join(comp_new)
                # timeline stuff
                # job index - 6
                job_posted_time = f1[index-6][0]
                job_timeline = ''.join([e for e in job_posted_time if not e.isspace()])
                jobs[job_url] = [title, company, job_timeline]
            # make a new page
            page += 1
            formatted_new = formatted + '&pg=%s' % page
            f = urllib2.urlopen(formatted_new)
            f1 = f.read().split('\n')
            f.close()
            f1 = [i.split('\r') for i in f1]
        return jobs
    else:
        return jobs


# monster
# returns a dicionary with the link as key and title, company, duration been posted as values

def get_monster_v2(position, location):
    from search_engine_mine import states
    import urllib2
    jobs = {}
    position = position.replace(' ', '-')
    location = location.replace(',', '__2C')
    location = location.replace(' ', '-')
    api = 'http://jobsearch.monster.com/search/{0}_5?where={1}'
    formatted = api.format(position, location)
    f = urllib2.urlopen(formatted)
    f1 = f.read().split('\n')
    f.close()
    f1 = [i.split('\r') for i in f1]
    pages_api = 'http://jobsearch.monster.com/search/{0}+{1}+{2}_125?pg={3}&where={4}&rad=20-miles'
    page = 1
    if len([e for e in f1 if 'class="slJobTitle' in e[0]]) > 0:
        while len([e for e in f1 if 'class="slJobTitle' in e[0]]) > 0:
            indexes = [f1.index(e) for e in f1 if 'class="slJobTitle' in e[0]]
            for index in indexes:
                string = f1[index][0]
                # title stuff
                start_title = string.find('title=')+7
                end_title = string.find('"', start_title)
                title = string[start_title:end_title]
                # link stuff
                start_link = string.find('href=')
                start_link = start_link+6
                stop_link = string.find('">', start_link)
                link = string[start_link:stop_link]
                # index of job + 22 = time
                time_str = f1[index+22][0]
                list_time_str = [e for e in time_str if not e.isspace()]
                actual_time = ''.join(list_time_str)
                # index + 8 = company
                comp = f1[943][0]
                start = comp.find('>')
                start = comp.find('>')+1
                stop = comp.find('</', start)
                company = comp[start:stop]
                jobs[link] = [title, company, actual_time]
            page += 1
            state = states[location[len(location)-2:].upper()]
            city = location[0:location.find('_')]
            formatted_pages = pages_api.format(state, city, position, page, location)
            f = urllib2.urlopen(formatted_pages)
            f1 = f.read().split('\n')
            f1 = [i.split('\r') for i in f1]
    else:
        jobs = {}
    return jobs



# a dictionary for use in monster

states = {'AK': 'Alaska',
 'AL': 'Alabama',
 'AR': 'Arkansas',
 'AZ': 'Arizona',
 'CA': 'California',
 'CO': 'Colorado',
 'CT': 'Connecticut',
 'DE': 'Delaware',
 'FL': 'Florida',
 'GA': 'Georgia',
 'HI': 'Hawaii',
 'IA': 'Iowa',
 'ID': 'Idaho',
 'IL': 'Illinois',
 'IN': 'Indiana',
 'KS': 'Kansas',
 'KY': 'Kentucky',
 'LA': 'Louisiana',
 'MA': 'Massachusetts',
 'MD': 'Maryland',
 'ME': 'Maine',
 'MI': 'Michigan',
 'MN': 'Minnesota',
 'MO': 'Missouri',
 'MS': 'Mississippi',
 'MT': 'Montana',
 'NC': 'North Carolina',
 'ND': 'North Dakota',
 'NE': 'Nebraska',
 'NH': 'New Hampshire',
 'NJ': 'New Jersey',
 'NM': 'New Mexico',
 'NV': 'Nevada',
 'NY': 'New York',
 'OH': 'Ohio',
 'OK': 'Oklahoma',
 'OR': 'Oregon',
 'PA': 'Pennsylvania',
 'RI': 'Rhode Island',
 'SC': 'South Carolina',
 'SD': 'South Dakota',
 'TN': 'Tennessee',
 'TX': 'Texas',
 'UT': 'Utah',
 'VA': 'Virginia',
 'VT': 'Vermont',
 'WA': 'Washington',
 'WI': 'Wisconsin',
 'WV': 'West Virginia',
 'WY': 'Wyoming'}




# careerbuilder

def careerbuilder_v2(position, location):
    import urllib2
    jobs = {}
    api = 'http://www.careerbuilder.com/Jobseeker/Jobs/JobResults.aspx?IPath=QH&qb=1&s_rawwords={0}&s_freeloc={1}&s_jobtypes=ALL'
    pages_api = 'http://www.careerbuilder.com/Jobseeker/Jobs/JobResults.aspx?excrit=freeLoc%3d{0}%3bQID%3dA6660204858735%3bst%3da%3buse%3dALL%3brawWords%3d{1}%3bCID%3dUS%3bSID%3d%3f%3bTID%3d0%3bENR%3dNO%3bDTP%3dDRNS%3bYDI%3dYES%3bIND%3dALL%3bPDQ%3dAll%3bPDQ%3dAll%3bPAYL%3d0%3bPAYH%3dgt120%3bPOY%3dNO%3bETD%3dALL%3bRE%3dALL%3bMGT%3dDC%3bSUP%3dDC%3bFRE%3d30%3bCHL%3dAL%3bQS%3dsid_unknown%3bSS%3dNO%3bTITL%3d0%3bOB%3d-relv%3bJQT%3dRAD%3bJDV%3dFalse%3bMaxLowExp%3d-1%3bRecsPerPage%3d25&pg={2}&IPath=QHKV'
    position = position.replace(' ', '+')
    location = location.replace(',', '%2C')
    location = location.replace(' ', '+')
    formatted = api.format(position, location)
    f = urllib2.urlopen(formatted)
    f1 = f.read().split('\n')
    f1 = [i.split('\r') for i in f1]
    page = 1
    if len([e for e in f1 if 'class="jt prefTitle"' in e[0]]) > 0:
        # eliminate erroneous pages
        index_of_pages = [f1.index(e) for e in f1 if 'class="jobresults_count"' in e[0]][0]+2
        stuff = f1[index_of_pages][0]
        stuff = ''.join([e for e in stuff if not e.isspace()])
        one = stuff.find('-')
        first_num = int(stuff[0:one])
        two = stuff.find('of')+2
        three = stuff.find('jobs')
        second_num = int(stuff[two:three])
        while second_num > first_num:
     
        #while len([e for e in f1 if 'class="jt prefTitle"' in e[0]]) > 0:
            indexes = [f1.index(e) for e in f1 if 'class="jt prefTitle"' in e[0]]
            # link stuff
            for cur in range(len(indexes)):
                index = indexes[cur] 
                first = f1[index][0]
                one = first.find('href=')+6
                two = first.find('>', one)
                link = first[one:two-1]
                # title
                three = first.find('</a>', two)
                title = first[two+1:three]
                # company stuff
                comp = f1[index + 33][0]
                one_2 = comp.find('href')
                two_2 = comp.find('>', one_2)+1
                three_2 = comp.find('</a>', two_2)
                company = comp[two_2:three_2]
                # duration posted
                if index != indexes[len(indexes)-1]:
                    current = f1[index:indexes[cur+1]]
                else:
                    current = f1[index:]
                dur_loc = [f1.index(e) for e in current if 'class="jl_rslt_posted_cell"' in e[0]][0]
                dur = f1[dur_loc][0]
                #dur = f1[index + 38][0]
                one_3 = dur.find('title=')
                two_3 = dur.find('>', one_3)+1
                three_3 = dur.find('</span>', two_3)
                duration = dur[two_3:three_3]
                # make dictionary
                jobs[link] = [title, company, duration]
            page += 1
            new_formatted = pages_api.format(location, position, page)
            f = urllib2.urlopen(new_formatted)
            f1 = f.read().split('\n')
            f1 = [i.split('\r') for i in f1]
            index_of_pages = [f1.index(e) for e in f1 if 'class="jobresults_count"' in e[0]][0]+2
            stuff = f1[index_of_pages][0]
            stuff = ''.join([e for e in stuff if not e.isspace()])
            one = stuff.find('-')
            first_num = int(stuff[0:one])
            two = stuff.find('of')+2
            three = stuff.find('jobs')
            second_num = int(stuff[two:three])
    else:
        jobs = {}
    return jobs
