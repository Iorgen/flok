from config.config import Config
from parser.managers.manager import ParserManager
from entrypoint.k_agent import parse_k_agent_target_page


def main():
    cfg = Config()
    """ Execute parser script for OKVED parsing"""
    print("------------------------------------")
    parse_k_agent_target_page()

# my cap "91588f4fb9475bde03fdfee20cd709ed" -
# TODO optimize selenium settings page upload too long
# TODO An idea to mix selenium and bs4 - selenium for captcha insert bs4 for information retrieving
# TODO all dynamic params or in config or in args
# TODO if very after N captcha resolving setup new proxy change proxy
# TODO insert parsed url into result page
# Start not on server parser for MUST

# Read configs from config/config.py
# change folder structure to parser - resource - resource_file
#


if __name__ == '__main__':
    main()
