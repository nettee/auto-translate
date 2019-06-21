import click

from autotrans.translator import AutoTranslator


@click.command()
@click.argument('src')
def main(src):
    translator = AutoTranslator(src)

if __name__ == '__main__':
    main()
