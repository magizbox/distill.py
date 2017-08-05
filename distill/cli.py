# -*- coding: utf-8 -*-
from os import getcwd
from tempfile import mkdtemp

import click
from distill.commands import task_run, task_build, task_serve


@click.command()
@click.argument('command')
def main(command):
    click.echo("Distill run " + command + ".")
    if command == "run":
        task_run()
    if command == "build_silent":
        project_folder = getcwd()
        task_build(project_folder)
    if command == "build":
        project_folder = getcwd()
        task_build(project_folder)
        task_run()
    if command == "serve":
        task_serve()


if __name__ == "__main__":
    main()
