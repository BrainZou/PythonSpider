# -*- coding: utf-8 -*-
# filename: main.py
import web
from web import form
import Music163RepetitiveRate
render = web.template.render('templates/')
urls = ('/music163', 'index')
app = web.application(urls, globals())

myform = form.Form(
    #form.Textbox("boe"),
    #form.Textbox("bax",
    #             form.notnull,
    #             form.regexp('\d+', 'Must be a digit'),
    #             form.Validator('Must be more than 5', lambda x: int(x) > 5)),
    #form.Textarea('moe'),
    #form.Checkbox('curly'),
    #form.Dropdown('french', ['mustard', 'fries', 'wine']))
    form.Textbox("fname",form.notnull, description=u"用户名1"),
    form.Textbox("sname",form.notnull, description=u"用户名2"))
class index:
    def GET(self):
	web.header('Content-Type','text/html;charset=UTF-8')
        form = myform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        print(form.render())
        return render.formtest(form)
    def POST(self):
	web.header('Content-Type','text/html;charset=UTF-8')
        form = myform()
        if not form.validates():
            print(form.render())
            return render.formtest(form)
        else:
	    print "begin"
	    playlist1=Music163RepetitiveRate.get_playlist_by_name(form.d.fname)
	    print playlist1
            playlist2=Music163RepetitiveRate.get_playlist_by_name(form.d.sname)
	    print playlist2
            content = Music163RepetitiveRate.repetitive_rate_by_playlistlink(playlist1,playlist2)
            return content
if __name__ == "__main__":
    #web.config.debug = False
    web.internalerror = web.debugerror
    app.run()
