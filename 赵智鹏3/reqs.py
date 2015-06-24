# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

from dbconn import db_cursor

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/main.html")


class CourseListHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/cou_list.html", courses = dal_list_courses())

class CourseEditHandler(tornado.web.RequestHandler):
    def get(self, cou_sn):

        cou = None
        if cou_sn != 'new' :
            cou = dal_get_course(cou_sn)
        
        if cou is None:
            cou = dict(cou_sn='new', stu_no='', cou_no='', name='', sex='',grade='')

        self.render("pages/cou_edit.html", course = cou)

    def post(self, cou_sn):
        stu_no = self.get_argument('stu_no', '')
        cou_no = self.get_argument('cou_no')
        name = self.get_argument('name', '')
        sex = self.get_argument('sex', '')
        grade=self.get_argument('grade','')

        if cou_sn == 'new' :
            dal_create_course(stu_no, cou_no, name, sex,grade)
        else:
            dal_update_course(cou_sn, stu_no, cou_no, name, sex,grade)

        self.redirect('/coulist')

class CourseDelHandler(tornado.web.RequestHandler):
    def get(self, cou_sn):
        dal_del_course(cou_sn)
        self.redirect('/coulist')

# -------------------------------------------------------------------------

def dal_list_courses():
    data = []
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT cou_sn, stu_no, cou_no, name, sex ,grade FROM course ORDER BY cou_sn DESC
        """
        cur.execute(s)      
        for r in cur.fetchall():
            cou = dict(cou_sn=r[0], stu_no=r[1], cou_no=r[2], name=r[3], sex=r[4],grade=r[5])
            data.append(cou)
    return data


def dal_get_course(cou_sn):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT cou_sn, stu_no, cou_no, name, sex,grade FROM course WHERE cou_sn=%s
        """
        cur.execute(s, (cou_sn, ))
        r = cur.fetchone()
        if r :
            return dict(cou_sn=r[0], stu_no=r[1], cou_no=r[2], name=r[3], sex=r[4],grade=r[5])


def dal_create_course(stu_no, cou_no, name, sex,grade):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        cur.execute("SELECT nextval('seq_cou_sn')")
        cou_sn = cur.fetchone()
        assert cou_sn is not None

        print('新课程内部序号%d: ' % cou_sn)

        s = """
        INSERT INTO course (cou_sn, stu_no, cou_no, name, sex,grade) 
        VALUES (%(cou_sn)s, %(stu_no)s, %(cou_no)s, %(name)s, %(sex)s,%(grade)s)
        """
        cur.execute(s, dict(cou_sn=cou_sn, stu_no=stu_no, cou_no=cou_no, name=name, sex=sex,grade=grade))


def dal_update_course(cou_sn, stu_no, cou_no, name, sex,grade):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        UPDATE course SET
          stu_no=%(stu_no)s,
          cou_no=%(cou_no)s, 
          name=%(name)s, 
          sex=%(sex)s,
          grade=%(grade)s 
        WHERE cou_sn=%(cou_sn)s
        """
        cur.execute(s, dict(cou_sn=cou_sn, stu_no=stu_no, cou_no=cou_no, name=name, sex=sex,grade=grade))


def dal_del_course(cou_sn):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        DELETE FROM course WHERE cou_sn=%(cou_sn)s
        """
        cur.execute(s, dict(cou_sn=cou_sn))
        print('删除%d条记录' % cur.rowcount)
