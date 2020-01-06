from flaskr.database.dataset_models.repository import Repository


def build_swap_inputs(self):
    for item in self.request.form.keys():
        #print(self.request.form[item])
        #print(item)
        if item.startswith('Swap From'):
            self.swaps[self.request.form[item]] = self.request.form['Swap To ' + str(item[-1])]
            #print(item)
        if item.startswith('Bidirectional Swap') == True:
            self.swaps[self.request.form['Swap To ' + str(item[-1])]] = self.request.form['Swap From ' + str(item[-1])]
            #print(self.swaps)
    print(self.swaps)
    print()

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