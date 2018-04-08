import json
import time
from Data.DataProvider import DataProvider
from Parser.VariantGenerator import VariantGenerator

# timer
start_time = time.time()

# gather data
data_provider = DataProvider()
baumuster = data_provider.load_baumuster('C958174')

# generate variants
variants = VariantGenerator.generate_basic_variants(baumuster)
print(len(variants), type(variants))

# j = json.dumps(for variant.codes in variants)
# with open('output.json', 'w') as file:
#      file.write(j)

print('\n--------- TEMPO DE EXECUCAO ----------')
print("%s segundos" % (time.time() - start_time))
