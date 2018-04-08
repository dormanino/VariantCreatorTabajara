import json
import time
from Data.DataProvider import DataProvider
from Models.Optional import ACC
from Models.Variant import Variant

# timer
start_time = time.time()

data_provider = DataProvider()
agr = data_provider.baumuster
basic_qvv = agr.basic_variant()

inconsistent_codes = []
acc_fixed = []
acc_optionals = []

for code in basic_qvv.codes:
    acc = data_provider.acc_list.find_acc(code)
    if acc is None:
        inconsistent_codes.append(code)
    elif not acc.optionals:
        acc_fixed.append(acc)
    else:
        cu = []
        for opt in acc.optionals:
            if agr.contains_code(opt):
                cu.append(opt)

        new_acc = ACC(code, cu)
        if not new_acc.optionals:
            acc_fixed.append(new_acc)
        else:
            acc_optionals.append(new_acc)


basic_combination = []
for acc in acc_fixed:
    basic_combination.append(acc.id)

combinations = [basic_combination]

for acc in acc_optionals:
    swap_list = [acc.id]
    for id in acc.optionals:
        swap_list.append(id)

    new_combinations = []
    for combination in combinations:
        for code in swap_list:
            new_combination = combination.copy()
            new_combination.append(code)
            new_combinations.append(new_combination)

    combinations = new_combinations

qvv_list = []
for index, combination in enumerate(combinations):
    name = 'QVV'+str(index+1)
    qvv = Variant(name, combination)
    qvv_list.append(qvv)

j = json.dumps([qvv.__dict__ for qvv in iter(qvv_list)])
with open('output.json', 'w') as file:
    file.write(j)

print('\n--------- ERROS ----------')
for code in inconsistent_codes:
    print('{} - Não disponível nos ACCs'.format(code))

print('\n--------- FIXO ----------')
print([acc.id for acc in iter(acc_fixed)])

print('\n--------- OPCIONAIS ----------')
for acc in acc_optionals:
    print('{} - {}'.format(acc.id, str(acc.optionals)))

print('\n--------- TEMPO DE EXECUCAO ----------')
print("%s segundos" % (time.time() - start_time))
