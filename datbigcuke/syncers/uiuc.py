"""Syncer for UIUC course catalogue."""

import datbigcuke.db
from tornado.ioloop import IOLoop
import oursql
import futures
import urllib3
import urllib3.connectionpool
from urlparse import urlparse
from xml.etree import ElementTree

# class generator query
CLASS_GENERATOR_QUERY = """
SELECT
    `course`.`institution_id` AS `institution_id`,
    `course`.`term_id` AS `term_id`,
    `course`.`id` AS `course_id`,
    `course`.`name` AS `name`,
    IF(ISNULL(`section`.`title`),`course`.`title`,`section`.`title`) AS `title`,
    CONCAT(
        `course`.`name`,
        ' ',
        IF(ISNULL(`section`.`title`), `course`.`title`, `section`.`title`)
    ) AS `class_name`
FROM `course`
INNER JOIN `section`
    ON (`course`.`id`=`section`.`course_id`)
WHERE `course`.`term_id`=?
GROUP BY `course`.`institution_id`, `course`.`term_id`, `course`.`id`, `title`;
"""



class UiucSyncer(object):
    COURSE_EXPLORER_URL = (
        'http://courses.illinois.edu/cisapp/explorer/schedule.xml'
    )

    def __init__(self, url=None):
        bootstrap_url = url or self.COURSE_EXPLORER_URL
        uri = urlparse(bootstrap_url)
        self._base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=uri)
        self._boostrap_path = uri.path
        # keep-alive connections for faster retrieval
        hdr = urllib3.util.make_headers(keep_alive=True)
        self._pool = urllib3.connectionpool.connection_from_url(bootstrap_url,
                                                                maxsize=20,
                                                                headers=hdr)
        self._conn = datbigcuke.db.mysql_connect()
        self._executor = futures.ThreadPoolExecutor(max_workers=10)
        self._cache = {}

    def close(self):
        self._executor.close()
        self._conn.close()
        self._pool.close()

    def _extract_path(self, url):
        if not url.startswith(self._base_url):
            raise Exception('cross-domain request')
        path = url[len(self._base_url):]
        if not path.startswith('/'):
           path = '/' + path
        return path

    def _prefetch_path(self, path):
        if path not in self._cache:
            def fetch():
                response = self._pool.request('GET', path)
                if response.status != 200:
                    return '<error code="{}"></error>'.format(response.status)
                return response.data

            self._cache[path] = self._executor.submit(fetch)

    def _prefetch_url(self, url):
        path = self._extract_path(url)
        self._prefetch_path(path)

    def _fetch_url(self, url):
        path = self._extract_path(url)
        self._prefetch_path(path)
        return self._cache[path].result()

    def sync(self, *years):
        with self._conn.cursor(oursql.DictCursor) as cursor:
            # make sure UIUC node exists in the database
            self._inst_id = self._sync_institution(cursor)
            # check for each of the posted years
            terms = self._sync_terms(cursor, years)
            for t in terms:
                self._sync_courses(cursor, t[0], t[1])
                # create classes from what we've scraped
                self._sync_classes(cursor, t[0])

    def _create_entity_id(self, cursor):
        cursor.execute('INSERT INTO `academic_entity` VALUES()')
        return cursor.lastrowid

    def _sync_institution(self, cursor):
        UIUC = 'University of Illinois at Urbana-Champaign'
        cursor.execute('SELECT `id`, `name` FROM `institution`'
                       'WHERE `name`=?',
                       (UIUC,))
        result = cursor.fetchone()
        if result is not None:
            return result['id']
        # create UIUC
        instid = self._create_entity_id(cursor)
        cursor.execute('INSERT INTO `institution`'
                       '(`id`, `name`) '
                       'VALUES(?,?)',
                       (instid, UIUC))
        return instid

    def _sync_terms(self, cursor, years):
        # synchronize the list of terms, then returns the terms that were
        # introduced (the ones requiring full sync)
        content = self._fetch_url(self.COURSE_EXPLORER_URL)
        root = ElementTree.fromstring(content)
        existing_terms = self._fetch_db_terms(cursor)
        # get terms from catalog
        terms = {}
        years = set(years)
        for calYear in root.iter('calendarYear'):
            year = int(calYear.text)
            # skip non-requested year, if specifically requested
            if years and year not in years:
                continue

            term_xml = self._fetch_url(calYear.attrib['href'])
            termroot = ElementTree.fromstring(term_xml)
            sindex = 0
            for term in termroot.iter('term'):
                terms[term.text] = {
                    'year': year,
                    'name': term.text,
                    'href': term.attrib['href'],
                    'sindex': sindex,
                }
                sindex += 1
        # check delta
        delta = []
        for tname in terms:
            if tname not in existing_terms:
                delta.append(terms[tname])
            else:
                et = existing_terms[tname]
                nt = terms[tname]
                # update sindex if needed
                if et['sindex'] != nt['sindex']:
                    delta.append({'id': et['id'], 'sindex': nt['sindex']})
        result = []
        # use delta to update database
        for d in delta:
            if 'id' in d:
                # update
                cursor.execute('UPDATE `term`'
                               'SET `sindex`=? '
                               'WHERE `id`=?',
                               (d['sindex'], d['id']))
            else:
                # new
                term_id = self._create_entity_id(cursor)
                result.append((term_id, d['href']))
                cursor.execute('INSERT INTO `term`'
                               '(`id`, `institution_id`, `year`,'
                               ' `sindex`, `name`) '
                               ' VALUES(?,?,?,?,?)',
                               (term_id, self._inst_id, d['year'],
                                d['sindex'], d['name']))
        return result


    def _fetch_db_terms(self, cursor):
        cursor.execute('SELECT `id`, `year`, `sindex`, `name`'
                       'FROM `term`'
                       'WHERE `institution_id`=?',
                       (self._inst_id,))
        terms = cursor.fetchall()
        result = {}
        for t in terms:
            result[t['name']] = t
        return result

    def _sync_courses(self, cursor, term_id, href):
        subjects_xml = self._fetch_url(href)
        subjectsroot = ElementTree.fromstring(subjects_xml)
        subject_list = []
        for subject in subjectsroot.iter('subject'):
            # for each subject, get courses
            subject_list.append((subject.attrib['id'], subject.attrib['href']))
            self._prefetch_url(subject_list[-1][1])
        subjectsroot.clear()

        for subject, href in subject_list:
            courses_xml = self._fetch_url(href)
            coursesroot = ElementTree.fromstring(courses_xml)
            
            courses = []
            course_url = []
            # check each course in the subject
            for course in coursesroot.iter('course'):
                course_id = self._create_entity_id(cursor)
                item = (
                    course_id,
                    self._inst_id,
                    term_id,
                    subject,
                    # cnumber
                    course.attrib['id'],
                    # name
                    '{} {}'.format(subject, course.attrib['id']),
                    # title
                    course.text,
                )
                courses.append(item)
                course_url.append(course.attrib['href'])
                self._prefetch_url(course.attrib['href'])

            # create course entities
            cursor.executemany('INSERT INTO `course`'
                               '(`id`, `institution_id`, `term_id`,'
                               '`subject`, `cnumber`, `name`, `title`)'
                               'VALUES (?, ?, ?, ?, ?, ?, ?)',
                               courses)

            for i, course in enumerate(courses):
                # find sections in each course
                self._sync_sections(cursor, term_id, course[0], course_url[i])
            coursesroot.clear()

    def _sync_sections(self, cursor, term_id, course_id, href):
        sections_xml = self._fetch_url(href)
        sectionsroot = ElementTree.fromstring(sections_xml)
        sections = []
        for section in sectionsroot.iter('section'):
            sections.append((section.get('id'),
                             section.text,
                             section.get('href')))
            self._prefetch_url(section.get('href'))
        sectionsroot.clear()
        section_details = []
        for crn, cnumber, section_href in sections:
            details = self._fetch_section_details(cursor, crn, section_href)
            if details:
                details['id'] = self._create_entity_id(cursor)
                section_details.append(details)

        cursor.executemany('INSERT INTO `section`'
                           '(`id`, `institution_id`, `term_id`,'
                           ' `course_id`, `snumber`, `title`, `ref_id`)'
                           'VALUES(?, ?, ?, ?, ?, ?, ?)',
                           ((x['id'], self._inst_id, term_id,
                            course_id, x['snumber'], x['title'], x['crn'])
                            for x in section_details))

    def _fetch_section_details(self, cursor, crn, href):
        section_xml = self._fetch_url(href)
        detailsroot = ElementTree.fromstring(section_xml)
        title_node = detailsroot.find('sectionTitle')
        title = title_node.text if title_node is not None else None
        snumber_node = detailsroot.find('sectionNumber')
        if snumber_node is None:
            return None  # probably independent study, etc.

        snumber = snumber_node.text
        result = None
        for meeting in detailsroot.iter('meeting'):
            # only record lectures
            if 'Lecture' in meeting.find('type').text:
                result = {
                    'title': title,
                    'snumber': snumber,
                    'crn': crn,
                }
                break
        detailsroot.clear()
        return result

    def _sync_classes(self, cursor, term_id):
        # generate the class using query
        cursor.execute(CLASS_GENERATOR_QUERY,
                       (term_id,))
        # for each class, generate id then insert
        for cls in cursor.fetchall():
            cls['id'] = self._create_entity_id(cursor)
            cursor.execute('INSERT INTO `class`'
                           '(`id`, `institution_id`, `term_id`,'
                           ' `course_id`, `name`, `title`, `class_name`)'
                           'VALUES (?, ?, ?, ?, ?, ?, ?)',
                           (cls['id'], cls['institution_id'], cls['term_id'],
                            cls['course_id'], cls['name'], cls['title'],
                            cls['class_name']))
