from argparse import ArgumentParser, Namespace
import prompt_toolkit
import cryptography
parser = ArgumentParser()
parser.usage = "USAGEEEE"
group = parser.add_mutually_exclusive_group()

parser.add_argument("a", type=int, help="The Base value")
parser.add_argument("b", type=int, help="The exponent")
group.add_argument("-v", "--verbose", action="count",
                    help="Provides a verbose description. Use -vv for extra verbose.")
group.add_argument("-s", "--silence", action="store_true",
                    help="generate a silent version")

args: Namespace = parser.parse_args()
result: int = args.a **args.b

if args.silence:
    print("SILENCED!!!")
else:
    match args.verbose:
        case 1:
            print(f"The result is {result}")
        case 2: 
            print(f"{args.a} ** {args.b} = {result}")
        case _:
            print(result)
