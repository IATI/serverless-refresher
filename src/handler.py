import argparse
import library.refresher as refresher
import library.build as build
import library.validate as validate
import library.db as db
from datetime import datetime, timedelta
from constants.config import config

def main(args):
    db.migrateIfRequired()

    if args.type == "refresh":
        refresher.refresh()
    elif args.type == "reload":
        refresher.reload(
            args.errors
        )
    elif args.type == "build": 
        build.main()
    elif args.type == "validate":
        validate.main()
    elif args.type == "refreshloop":
        refresher.service_loop()
    elif args.type == "buildloop":
        build.service_loop()
    elif args.type == "validateloop":
        validate.service_loop()    
    else:
        print("Type is required - either refresh, reload, build, or validate.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Refresh/Build from IATI Registry')
    parser.add_argument('-t', '--type', dest='type', default="refresh", help="Trigger 'refresh' or 'build'")
    parser.add_argument('-e', '--errors', dest='errors', action='store_true', default=False, help="Attempt to download previous errors")
    args = parser.parse_args()
    main(args)