"""
Input
config file
list of tables (to try and merge)

Output
asks if proposed merge is ok
on approval, merges tables
asks if looks good (delete old tables)
on approval, deletes old tables
"""

import tomli
config=tomli.load("config.toml")

def main():
    """
    Main entry point of the script.
    """
    # get

if __name__ == "__main__":
    main()