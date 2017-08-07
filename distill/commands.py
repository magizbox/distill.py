# -*- coding: utf-8 -*-
import os
import shutil
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from os.path import join, dirname
from tempfile import mkdtemp
from jinja2 import Environment, select_autoescape, FileSystemLoader
from livereload import Server

from distill.extend import PageExtendWorker
from distill.site import load_site


def task_open_website():
    url = 'http://127.0.0.1:8000/index.html'
    webbrowser.open(url)


def task_run():
    os.chdir('site')
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    task_open_website()
    httpd.serve_forever()


def _bootstrap(site_folder, temp_site_folder):
    try:
        shutil.rmtree(site_folder)
    except:
        pass
    try:
        shutil.rmtree(temp_site_folder)
    except:
        pass


def _copy_template(template_folder, temp_site_folder):
    shutil.copytree(template_folder, temp_site_folder)


def _render_file(temp_site_folder, site_folder, filename):
    site = load_site()
    env = Environment(
        autoescape=select_autoescape(['html', 'xml']),
        loader=FileSystemLoader(temp_site_folder))
    template = env.get_template(filename)
    output = template.render(site)
    with open(join(site_folder, filename), "w", encoding="utf-8") as f:
        f.write(output)


def _extend_template(doc_folder, temp_site_folder, livereload=False):
    site = load_site()
    for page in site["pages"]:
        PageExtendWorker.extend(doc_folder, temp_site_folder, page, livereload)


def _render_template(temp_site_folder, site_folder):
    site = load_site()
    files = [p.page for p in site["pages"]]
    shutil.copytree(temp_site_folder, site_folder)
    for f in files:
        _render_file(temp_site_folder, site_folder, f)


def _copy_static_folders(doc_folder, site_folder):
    static_folders = [f for f in os.listdir(doc_folder) if os.path.isdir(join(doc_folder, f))]
    for f in static_folders:
        try:
            shutil.copytree(join(doc_folder, f), join(site_folder, f))
        except:
            pass


def _sweep(temp_site_folder):
    try:
        shutil.rmtree(temp_site_folder)
    except:
        pass


def task_build(project_folder, livereload=False):
    site_folder = join(project_folder, 'site')
    cwd = os.getcwd()
    doc_folder = join(cwd, 'docs')
    template_folder = join(dirname(__file__), "distill_template")
    temp_site_folder = join(project_folder, '_site')
    _bootstrap(site_folder, temp_site_folder)
    _copy_template(template_folder, temp_site_folder)
    _extend_template(doc_folder, temp_site_folder, livereload)
    _render_template(temp_site_folder, site_folder)
    _sweep(temp_site_folder)
    _copy_static_folders(doc_folder, site_folder)


def task_serve():
    # build temp folder
    tmp_folder = mkdtemp()
    print(tmp_folder)
    task_build(tmp_folder, livereload=True)
    server = Server()
    doc_files = join(os.getcwd(), "docs", "*")
    rebuild = lambda: task_build(tmp_folder)
    server.watch(doc_files, rebuild)
    webbrowser.open("http://127.0.0.1:5500")
    server.serve(root=join(tmp_folder, "site"), liveport=35729)
    shutil.rmtree(tmp_folder)
