import argparse
import json
import logging
from urllib.parse import parse_qs
import os
import sys

CURRENT_DIR_PATH = os.path.abspath(os.getcwd())

URL_PREFIX = "chrome-extension://klbibkeccnjlkjkiokjodocebajanakg/" \
             "suspended.html"
URL_PREFIX_WITH_DASH = f"{URL_PREFIX}#"
URL_PREFIX_WITH_DASH_LENGTH = len(URL_PREFIX_WITH_DASH)
SESSION_NAME_SUFFIX = " - cleaned"

LOGGER = logging.getLogger(__name__)


def clean_item(item: dict, verbose: bool = False) -> dict:
    url = item["url"]
    pos = url.find(URL_PREFIX_WITH_DASH)
    if pos > -1:
        url = url[pos + URL_PREFIX_WITH_DASH_LENGTH:]
        cleaned_item = parse_qs(url)
        item["url"] = cleaned_item["uri"][0]
        item["title"] = cleaned_item["ttl"][0]
        return item
    if verbose:
        LOGGER.warning(f"Skipping {item} as no suspended tab")
        LOGGER.exception(item)
    return item


def process(
    in_file: str,
    out_file: str,
    session_name_suffix: str = SESSION_NAME_SUFFIX,
    verbose: bool = False
) -> bool:
    if not os.path.isabs(in_file):
        in_file = os.path.join(CURRENT_DIR_PATH, in_file)

    with open(in_file, "r", encoding='utf8') as json_in_file:
        data = json.load(json_in_file)

    cleaned_tabs = []
    tabs = data["tabs"]

    for item in tabs:
        try:
            item = clean_item(item)
            cleaned_tabs.append(item)
        except Exception as err:
            if verbose:
                LOGGER.warning(f"Error parsing {item}")
                LOGGER.exception(err)
                LOGGER.exception(item)
            cleaned_tabs.append(item)

    data["tabs"] = cleaned_tabs
    data["title"] += session_name_suffix

    if not os.path.isabs(out_file):
        out_file = os.path.join(CURRENT_DIR_PATH, out_file)

    with open(out_file, "w+", encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

    return True


def cli():
    parser = argparse.ArgumentParser(description='Update TLD names')
    parser.add_argument(
        "--in-file",
        dest="in_file",
        required=True,
        type=str,
        help="Input file. Could be relative (to current directory)"
    )
    parser.add_argument(
        "--out-file",
        dest="out_file",
        required=True,
        type=str,
        help="Output file. Could be relative (to current directory)"
    )
    parser.add_argument(
        "--session-name-suffix",
        dest="session_name_suffix",
        type=str,
        default=SESSION_NAME_SUFFIX,
        help=f"Session name suffix. Defaults to `{SESSION_NAME_SUFFIX}`."
    )
    parser.add_argument(
        '--verbose',
        dest="verbose",
        default=False,
        action='store_true',
        help="Verbose output.",
    )
    args = parser.parse_args(sys.argv[1:])
    in_file = args.in_file
    out_file = args.out_file
    session_name_suffix = args.session_name_suffix
    verbose = args.verbose

    return int(
        not process(
            in_file,
            out_file,
            session_name_suffix=session_name_suffix,
            verbose=verbose
        )
    )


if __name__ == "__main__":
    cli()
