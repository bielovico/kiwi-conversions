# coding=utf-8
import argparse
from converter import Converter
import json


ap = argparse.ArgumentParser()
ap.add_argument("--amount", required=True, type=float, help="Amount of money you want to convert.")
ap.add_argument("--input_currency", required=True, type=unicode,
                help="Currency code or symbol you want to convert FROM.")
ap.add_argument("--output_currency", required=False, type=unicode,
                help="Currency code or symbol you want to convert TO. If omitted, convert to all known currencies.")
args = ap.parse_args()
# args = ap.parse_args(['--amount', '100.258', '--input_currency', u'£', '--output_currency', u'Kč'])
n = args.amount
ic = args.input_currency
oc = args.output_currency
converter = Converter()

if ic not in converter.get_currency_codes():
    inputs = converter.get_currency_symbols().get(ic, [])
    if not inputs:
        message = 'Could not resolve input currency ' + ic + '.'
        raise ValueError(message)
    if len(inputs) > 1:
        message = 'Input currency symbol ' + ic + \
                  ' is shared within more currencies. Please specify, which currency you meant ' + str(inputs)
        raise ValueError(message)
    ic = inputs[0]

if oc is None:
    oc = converter.get_currency_codes()
else:
    if oc not in converter.get_currency_codes():
        inputs = converter.get_currency_symbols().get(oc, [])
        if not inputs:
            raise ValueError('Could not resolve output currency ' + oc + '.')
        if len(inputs) > 1:
            message = 'Output currency symbol ' + oc + \
                      ' is shared within more currencies. Please specify, which currency you meant ' + str(inputs)
            raise ValueError(message)
        oc = inputs[0]
    oc = [oc]

output = converter.get_conversions(ic, oc, n)
json = json.dumps({'input': {'amount': n, 'currency': ic}, 'output': output}, sort_keys=True, indent=4)
print json

