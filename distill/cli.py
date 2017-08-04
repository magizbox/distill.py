# -*- coding: utf-8 -*-
import click
from distill.tasks import task_run, task_build


@click.command()
@click.argument('command')
def main(command):
    tasks = {
        "run": task_run,
        "build": task_build
    }
    click.echo("Run " + command)
    tasks[command]()


if __name__ == "__main__":
    main()
