import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--env', required=False)
args = parser.parse_args()

environment = args.env or os.getenv('MPAAS_ENVIRONMENT') or 'local'
