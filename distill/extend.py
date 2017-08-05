from os.path import join


class PageExtendWorker():
    @staticmethod
    def extend(doc_folder, temp_site_folder, page, livereload):
        f = page.page
        content = open(join(doc_folder, f), "r", encoding="utf-8").read()
        template_file = "{}.html".format(page.type)
        if livereload:
            livereload_inject = "<script src='http://localhost:35729/livereload.js'></script>"
        else:
            livereload_inject = ""
        template = '{% extends "' + template_file + '" %}\n' + \
                   '{% block content %}\n' + \
                   content + \
                   livereload_inject + \
                   '{% endblock %}'
        with open(join(temp_site_folder, f), "w", encoding="utf-8") as f:
            f.write(template)
