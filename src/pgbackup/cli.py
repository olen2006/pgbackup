from argparse import Action, ArgumentParser

class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        namespace.driver = driver.lower()
        namespace.destination = destination

def create_parser():
    parser = ArgumentParser(description ="""
    Backup Postgre SQL Databases locally or to AWS S3.
            """)
    parser.add_argument("url", help="URL of the database to backup")
    parser.add_argument("--driver", '-d',
            help="how & where to store backup",
            nargs=2,
            metavar=("DRIVER", "DESTINATION"),#to separate variables
            action=DriverAction,
            required=True)

    return parser

#as if we would write it as a script (from top to bottom)
def main():
    import boto3
    import time
    from pgbackup import pgdump, storage
    #parse arguments
    #no error handling here is needed
    args = create_parser().parse_args()
    #using url off those passed args
    dump = pgdump.dump(args.url)# we already have a dump here
    #applying a timestamp
    if args.driver == 's3':
        client = boto3.client('s3')
        timestamp = time.strftime("%Y-%m-%dT%H-%M", time.localtime())
        file_name = pgdump.dump_file_name(args.url, timestamp)
        #we use client to pass in
        print (f"Backing database up to {args.destination} in S3 as {file_name}")
        storage.s3(client,dump.stdout, args.destination, file_name)
    else:
        #local save. transfer contents from dump.stdout into outfile and close them both
        outfile = open(args.destination, 'wb')
        print(f"Backing database locally to {outfile.name}")
        storage.local(dump.stdout, outfile)



