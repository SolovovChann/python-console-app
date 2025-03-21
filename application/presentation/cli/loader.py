import argparse
from typing import Any, Iterable, Protocol

from application.presentation.cli.command import Command


PAYLOAD_KEY: str = "payload"


class _SubParser(Protocol):
    def add_parser(
        self,
        name: str,
        *,
        deprecated: bool = False,
        **kwargs: Any,
    ) -> argparse.ArgumentParser: ...


def load_commands(
    subparsers: _SubParser,
    commands: Iterable[type[Command]],
    *,
    payload_key: str = PAYLOAD_KEY,
    **command_init_kwargs: Any,
) -> None:
    for command in commands:
        instance = command(**command_init_kwargs)
        subparser = subparsers.add_parser(
            name=instance.get_name(),
            help=instance.get_help(),
            description=instance.get_description(),
            aliases=instance.aliases,
        )

        instance.add_arguments(subparser)

        defaults_kwargs = {payload_key: instance.handle}
        subparser.set_defaults(**defaults_kwargs)


def execute_command(
    namespace: argparse.Namespace,
    *,
    payload_key: str = PAYLOAD_KEY,
) -> None:
    kwargs = {**vars(namespace)}
    payload = kwargs.pop(payload_key)

    payload(**kwargs)
