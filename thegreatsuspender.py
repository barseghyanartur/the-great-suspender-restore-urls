import argparse
import json
import logging
import os
import re
import sys
from urllib.parse import parse_qs
from typing import Tuple

__version__ = "0.4"
__author__ = "Artur Barseghyan"
__copyright__ = "2021 Artur Barseghyan"
__license__ = "MIT License"
__all__ = (
    "REGEX",
    "REGEX_PATTERN",
    "SESSION_NAME_SUFFIX",
    "clean_data",
    "clean_item",
    "cli",
    "process",
    "re_clean_data",
    "re_clean_item",
)

SESSION_NAME_SUFFIX = " - cleaned"
CURRENT_DIR_PATH = os.path.abspath(os.getcwd())
REGEX_PATTERN = r"^chrome\-extension\:\/\/[a-z]+\/suspended\.html#(.+)$"
REGEX = re.compile(REGEX_PATTERN)
LOGGER = logging.getLogger(__name__)


def get_settings(extension_id: str) -> Tuple[str, int]:
    url_prefix_with_dash = f"chrome-extension://{extension_id}/suspended.html#"
    url_prefix_with_dash_length = len(url_prefix_with_dash)
    return url_prefix_with_dash, url_prefix_with_dash_length


def clean_item(
    item: dict,
    url_prefix_with_dash: str,
    url_prefix_with_dash_length: int,
    verbose: bool = False,
) -> dict:
    url = item["url"]
    pos = url.find(url_prefix_with_dash)
    if pos > -1:
        url = url[pos + url_prefix_with_dash_length:]
        cleaned_item = parse_qs(url)
        item["url"] = cleaned_item["uri"][0]
        item["title"] = cleaned_item["ttl"][0]
        return item
    if verbose:
        LOGGER.warning(f"Skipping {item} as no suspended tab")
        LOGGER.exception(item)
    return item


def re_clean_item(
    item: dict,
    verbose: bool = False,
) -> dict:
    url = item["url"]
    match = REGEX.match(url)
    if match:
        cleaned_item = parse_qs(match.groups()[0])
        item["url"] = cleaned_item["uri"][0]
        item["title"] = cleaned_item["ttl"][0]
        return item
    if verbose:
        LOGGER.warning(f"Skipping {item} as no suspended tab")
        LOGGER.exception(item)
    return item


def clean_data(
    data: dict,
    extension_id: str,
    session_name_suffix: str = SESSION_NAME_SUFFIX,
    verbose: bool = False,
) -> dict:
    cleaned_tabs = []
    tabs = data["tabs"]

    url_prefix_with_dash, url_prefix_with_dash_length = get_settings(
        extension_id
    )

    for item in tabs:
        try:
            item = clean_item(
                item,
                url_prefix_with_dash=url_prefix_with_dash,
                url_prefix_with_dash_length=url_prefix_with_dash_length,
                verbose=verbose,
            )
        except Exception as err:
            if verbose:
                LOGGER.warning(f"Error parsing {item}")
                LOGGER.exception(err)
                LOGGER.exception(item)
        cleaned_tabs.append(item)

    data["tabs"] = cleaned_tabs
    data["title"] += session_name_suffix
    return data


def re_clean_data(
    data: dict,
    session_name_suffix: str = SESSION_NAME_SUFFIX,
    verbose: bool = False,
) -> dict:
    cleaned_tabs = []
    tabs = data["tabs"]
    for item in tabs:
        try:
            item = re_clean_item(
                item,
                verbose=verbose,
            )
        except Exception as err:
            if verbose:
                LOGGER.warning(f"Error parsing {item}")
                LOGGER.exception(err)
                LOGGER.exception(item)
        cleaned_tabs.append(item)

    data["tabs"] = cleaned_tabs
    data["title"] += session_name_suffix
    return data


def process(
    in_file: str,
    out_file: str,
    session_name_suffix: str = SESSION_NAME_SUFFIX,
    extension_id: str = None,
    verbose: bool = False,
) -> bool:
    if not os.path.isabs(in_file):
        in_file = os.path.join(CURRENT_DIR_PATH, in_file)

    with open(in_file, "r", encoding="utf8") as json_in_file:
        data = json.load(json_in_file)

    if extension_id:
        data = clean_data(
            data,
            session_name_suffix=session_name_suffix,
            extension_id=extension_id,
            verbose=verbose,
        )
    else:
        data = re_clean_data(
            data,
            session_name_suffix=session_name_suffix,
            verbose=verbose,
        )

    if not os.path.isabs(out_file):
        out_file = os.path.join(CURRENT_DIR_PATH, out_file)

    with open(out_file, "w+", encoding="utf8") as json_file:
        json.dump(data, json_file, ensure_ascii=False)

    return True


def cli():
    parser = argparse.ArgumentParser(
        description="Restore the broken URLs of the Great Suspender browser "
                    "extension"
    )
    parser.add_argument(
        "--in-file",
        dest="in_file",
        required=True,
        type=str,
        help="Input file. Could be relative (to current directory)",
    )
    parser.add_argument(
        "--out-file",
        dest="out_file",
        required=True,
        type=str,
        help="Output file. Could be relative (to current directory)",
    )
    parser.add_argument(
        "--session-name-suffix",
        dest="session_name_suffix",
        type=str,
        default=SESSION_NAME_SUFFIX,
        help=f"Session name suffix. Defaults to `{SESSION_NAME_SUFFIX}`.",
    )
    parser.add_argument(
        "--extension-id",
        dest="extension_id",
        type=str,
        help=f"ID of ``The Great Suspender`` extension. If left blank, regular"
             f"expression match will be used.",
    )
    parser.add_argument(
        "--verbose",
        dest="verbose",
        default=False,
        action="store_true",
        help="Verbose output.",
    )
    args = parser.parse_args(sys.argv[1:])
    in_file = args.in_file
    out_file = args.out_file
    session_name_suffix = args.session_name_suffix
    extension_id = args.extension_id
    verbose = args.verbose

    return int(
        not process(
            in_file,
            out_file,
            session_name_suffix=session_name_suffix,
            extension_id=extension_id,
            verbose=verbose,
        )
    )


if __name__ == "__main__":
    cli()
