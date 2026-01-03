from argparse import ArgumentParser, Namespace
import argcomplete
parser = ArgumentParser()

#parser.add_argument("echo", help="Echos the given string")
parser.add_argument("square", help="Squares a given number", 
        type=int, default=0, nargs="?")
parser.add_argument("-v", "--verbose", 
        help="Provides a verbose description, -vv for extra verbose",
        #action="store_true", 
        action="count",
        #required=True,
        #type=int,
        #choices=[0, 1, 2]
        )
args: Namespace = parser.parse_args()
result: int = args.square ** 2


if args.verbose == 1:
    print(f"The result is: {result}")
elif args.verbose == 2:
    print(f"{args.square} ** {args.square} = {result}")
else: 
    print(result)

