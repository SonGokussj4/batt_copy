# PYTHON script
import sys
sys.path.append('{parent}/pylibs'.format(parent='/'.join(__file__.split('/')[0:-1])))
from ansa import base, constants
from collections import defaultdict
from pathlib import Path
from pycolor import atr, fg, bg


def main(base_batt, modif_batt):
    # Load base battery include
    base.InputPamCrash(filename=base_batt)

    # Load PIDs to show
    print("{}[ INFO ]{} Loading file with list of battery nodes...".format(atr.bo, atr.reset_all))
    curdir = Path('.')
    batt_nodes_file = curdir / 'PID_BAT_HV_MODULE.txt'
    res = input('File with battery nodes [{}]: '.format(batt_nodes_file))
    if res:
        batt_nodes_file = curdir / res

    if not batt_nodes_file.exists():
        print("{}{}[ ERROR ]{} {} not found...".format(atr.bo, fg.lr, atr.reset_all, batt_nodes_file.absolute()))
        print("{}[ INFO ]{} Trying to find battery modules by name: '_BATTERIEMODUL_'...".format(atr.bo, atr.reset_all))
        #TODO: vybrat to pomoci NAZVU
        pids_to_show = []
    else:
        with open(str(batt_nodes_file.absolute()), 'r') as f:
            pids_to_show = [int(line.rstrip('\n').split(',')[0].strip())
                            for line in f.readlines()]

    # Collect Battery Modules
    props = [ent for ent in base.CollectEntities(constants.PAMCRASH, None, 'PART_SHELL', True)
             if '_BATTERIEMODUL_' in ent._name or ent._id in pids_to_show]

    # Show only these modules
    base.Or(props)

    props_left = props[len(props) // 2:]  # first half
    props_right = props[0:len(props) // 2]  # second half

    dc_left = defaultdict(list)
    dc_right = defaultdict(list)

    print("{}[ INFO ]{} Creating modulesX SETs within Ansa".format(atr.bo, atr.reset_all))
    for idx, pid in enumerate(props_left):
        dc_left['module{}'.format(idx % 6 + 1)].append(pid)
        #print(idx % 6 + 1, pid)

    for idx, pid in enumerate(props_right):
        dc_right['module{}'.format(idx % 6 + 1)].append(pid)
        #print(idx % 6 + 1, pid)

    # TODO: rename keys to right names
    # TODO: left side should have even numbers
    # TODO: right side should have odd numbers

    dc_left['module12'] = dc_left.pop('module6')
    dc_left['module10'] = dc_left.pop('module5')
    dc_left['module8'] = dc_left.pop('module4')
    dc_left['module6'] = dc_left.pop('module3')
    dc_left['module4'] = dc_left.pop('module2')
    dc_left['module2'] = dc_left.pop('module1')

    dc_right['module11'] = dc_right.pop('module6')
    dc_right['module9'] = dc_right.pop('module5')
    dc_right['module7'] = dc_right.pop('module4')
    dc_right['module5'] = dc_right.pop('module3')
    dc_right['module3'] = dc_right.pop('module2')

    # Merge them into one
    dc_left.update(dc_right)
    dc = dc_left

    # Create new include
    inc_name = str(Path(modif_batt).name)
    print("{}[ INFO ]{} Creating include... {}".format(atr.bo, atr.reset_all, inc_name))
    all_includes = base.CollectEntities(constants.PAMCRASH, None, 'INCLUDE', True)
    # Check if include already exists, if yes, delete it (not entities within)
    if any([include._name == inc_name for include in all_includes]):
        existing_inc = [include for include in all_includes if include._name == inc_name][0]
        base.DeleteEntity(existing_inc, compress=True)
    myinclude = base.CreateEntity(constants.PAMCRASH, 'INCLUDE', {'Name': inc_name})

    print("{}[ INFO ]{} Adding SETs (moduleX) into include...".format(atr.bo, atr.reset_all))
    for idx in range(1, 13):
        set_name = 'module{}'.format(idx)
        # Check if SET exists, if yes, delete it (not entities within)
        all_sets = base.CollectEntities(constants.PAMCRASH, None, 'GROUP', True)
        if any([SET._name == set_name for SET in all_sets]):
            existing_set = [SET for SET in all_sets if SET._name == set_name][0]
            base.DeleteEntity(existing_set, compress=True)

        # Create emtpy SET
        myset = base.CreateEntity(constants.PAMCRASH, 'GROUP', {'Name': set_name})
        # Collect all nodes from dict
        nodes = base.CollectEntities(constants.PAMCRASH, dc[set_name], 'NODE', True)
        # Add nodes to SET
        base.AddToSet(myset, nodes)
        # Add SET to INCLUDE
        base.AddToInclude(myinclude, myset)

    print("{}[ INFO ]{} Outputting to: {}".format(atr.bo, atr.reset_all, modif_batt))
    base.OutputPamCrash(modif_batt, include_output_mode='contents', include=myinclude)


# if __name__ == '__main__':
#     main()
