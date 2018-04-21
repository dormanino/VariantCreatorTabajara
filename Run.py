import json
import time
from Data.DataProvider import DataProvider
from Helper.Utils import Utils
from Parser.VariantGenerator import VariantGenerator

# timer
start_time = time.time()

# gather data
data_provider = DataProvider()
baumuster = data_provider.load_baumuster('C958174')

# generate variants
variants = VariantGenerator.variants_generator(baumuster)
final_list = []
for variant in variants:
    print(variant.id)
    final_list.append(variant)

Utils.print_list_info('Variants', final_list)
# j = json.dumps(variants)
# with open('output.json', 'w') as file:
#      file.write(j)

print('\n--------- TEMPO DE EXECUCAO ----------')
print("%s segundos" % (time.time() - start_time))
