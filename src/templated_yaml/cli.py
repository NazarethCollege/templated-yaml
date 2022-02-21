import click, yaml, sys, select
from . import settings, api


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.argument('path', required=False, type=click.Path(exists=True))
@click.option('--context', default="---")
def render(path, context):
    context = yaml.safe_load(context)

    if path:
        click.echo(yaml.dump(api.render_from_path(path, context), default_flow_style=False))
    else:
        stdin_text = click.get_text_stream('stdin')
        if select.select([stdin_text.buffer,], [], [], 0.0)[0]:
            click.echo(yaml.dump(api.render_from_string(stdin_text.read(), context), default_flow_style=False))
        else:
            raise Exception("render requires either a path or stdin")


@cli.command()
def version():
    major, minor, patch = settings.VERSION

    click.echo("Templated YAML version {}.{}.{} compiled on {}".format(
        major,
        minor,
        patch,
        settings.COMPILATION_DATE.strftime('%Y-%m-%d %H:%M:%S')
    ))


