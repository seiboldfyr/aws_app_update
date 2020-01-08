import re

from flaskr.database.dataset_models.repository import Repository


def build_swap_inputs(self):
    for item in self.request.form.keys():
        if item.startswith('Swap From'):
            self.swaps[self.request.form[item]] = self.request.form['Swap To ' + str(item[-1])]
        if item.startswith('Bidirectional Swap') == True:
            self.swaps[self.request.form['Swap To ' + str(item[-1])]] = self.request.form['Swap From ' + str(item[-1])]


def build_group_inputs(self):
    for item in self.request.form.keys():
        if item.startswith('Group'):
            if self.groupings.get(str(item[-1])) is None:    #TODO: see the (*) TODO item in processor.py, this is source of error
                self.groupings[str(item[-1])] = {}
            self.groupings[item[-1]][item[:-2]] = self.request.form[item]


def get_collection(self):
    dataset_repository = Repository()
    dataset = dataset_repository.get_by_id(self.dataset_id)
    return dataset.get_well_collection()


def get_concentrations(string):
    if string.endswith('fM'):
        return float(re.match(r'^\d+', string).group(0)) / 1000
    elif string.endswith('pM'):
        return float(re.match(r'^\d+', string).group(0))
    elif string.endswith('nM'):
        return float(re.match(r'^\d+', string).group(0)) * 1000
    else:
        return 0

def add_custom_group_label(self, well):
    originallabel = well.get_label().split('_')
    well['label'] = '_'.join([item for item in originallabel[:2]])
    if self.groupings.get(str(well.get_group())):
        well['label'] = well.get_label() + '_' + self.groupings[str(well.get_group())]['Group Label']
    well['label'] += '_' + str(well.get_group())
    return well