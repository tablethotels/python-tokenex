import os
from pprint import pprint

import argparse

from .tokenex import TokenexRequest


CLI_COMMAND_MAP = {
    "positionals": {
        "action": {
            "options": {
                "choices": TokenexRequest.COMMAND_MAP.keys(),
                "help": "Command to run"
            }
        },
        "value": {
            "options": {
                "help": "Command Input Value"
            }
        }
    },
    "optionals": {
        "user_id": {
            "short_flag": "-u",
            "long_flag": "--user-id",
            "envar": "TOKENEX_USER_ID",
            "required": True,
            "options": {
                "default": None,
                "help": "Tokenex User ID"
            }
        },
        "api_key": {
            "short_flag": "-k",
            "long_flag": "--api-key",
            "envar": "TOKENEX_API_KEY",
            "required": True,
            "options": {
                "default": None,
                "help": "Tokenex API Key"
            }
        },
        "token_scheme": {
            "short_flag": "-s",
            "long_flag": "--token-scheme",
            "envar": "TOKENEX_SCHEME",
            "options": {
                "default": "TOKENfour",
                "choices": TokenexRequest.TOKEN_SCHEMES.keys(),
                "help": "Tokenization Scheme"
            }
        },
        "test_mode": {
            "short_flag": "-t",
            "long_flag": "--test-mode",
            "envar": "TOKENEX_TEST_MODE",
            "options": {
                "default": None,
                "action": "store_true",
                "help": "Enable Testing Mode"
            }
        }
    }
}


def validate_args():

    validation_errors = []
    optional_args = CLI_COMMAND_MAP['optionals']

    for key, arg in optional_args.items():

        if getattr(ARGS, key) is None:
            setattr(ARGS, key, os.environ.get(arg['envar'], None))
            if not getattr(ARGS, key) and arg.get('required', None):
                error_msg = "You must provide {0} via {1} {2}".format(
                    key,
                    arg['short_flag'],
                    "or envar " + arg.get('envar', "")
                )
                validation_errors.append(error_msg)

    # special validation for test_mode
    test_mode_envar = os.environ.get(optionals['test_mode']['envar'], None)
    if ARGS.test_mode is None or test_mode_envar is None:
        ARGS.test_mode = False
    elif ARGS.test_mode is None and test_mode_envar is True:
        ARGS.test_mode = True

    return validation_errors


def main():

    if ARGS.test_mode:
        print("*** TEST MODE ENABLED ***")

    tr = TokenexRequest(
        ARGS.user_id,
        ARGS.api_key,
        tokenex_test_mode=ARGS.test_mode,
        token_scheme_name=ARGS.token_scheme
    )

    result = None

    if ARGS.action == "tokenize":
        result = tr.tokenize(ARGS.value)
    elif ARGS.action == "tokenize_encrypted":
        result = tr.tokenize_encrypted(ARGS.value)
    elif ARGS.action == "validate":
        result = tr.validate(ARGS.value)
    elif ARGS.action == "detokenize":
        result = tr.detokenize(ARGS.value)
    elif ARGS.action == "delete":
        result = tr.delete(ARGS.value)

    if result:
        print("Result:")
        for key, value in result.json.items():
            print("\t{}: {}".format(key, value))
        print("")
    else:
        print("\n** An unexpected error has occurred **\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    positionals = CLI_COMMAND_MAP['positionals']
    for key, arg in positionals.items():
        parser.add_argument(key, **arg['options'])

    optionals = CLI_COMMAND_MAP['optionals']
    for key, arg in optionals.items():
        parser.add_argument(str(arg['short_flag']), str(arg['long_flag']), **arg['options'])

    ARGS = parser.parse_args()

    errors = validate_args()
    if len(errors) == 0:
        main()
    else:
        print("The following validation errors occurred:")
        for validation_error in errors:
            print(" - " + validation_error)
