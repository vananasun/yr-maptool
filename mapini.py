import argparse
from internal.preview_base import PreviewBase
from internal.map_file import MapFile
from internal.sort_triggers import TriggerSorter
from internal.zombies.gen_zombie_spawns import GenZombieSpawns
from internal.csra2_exporter import CSRA2Exporter



parser = argparse.ArgumentParser()
group_mode = parser.add_mutually_exclusive_group(required=True)
group_mode.add_argument(
    "--replace-preview",
    help="Add or replace a map\'s preview image.",
    nargs=2,
    metavar=("MAP_FILE", "IMAGE_FILE"))

group_mode.add_argument(
    "--extract-preview",
    help="Extract the preview image from a map file.",
    nargs=2,
    metavar=("MAP_FILE", "IMAGE_FILE"))

group_mode.add_argument(
    "--show-preview",
    help="Display the preview of a map file.",
    nargs=1,
    metavar=("MAP_FILE",))

group_mode.add_argument(
    "--merge-ini",
    help="Patch the ini rules of a map file with those of the given ini file. You can choose between overwriting, completely replacing, or only adding the sections.",
    nargs=3,
    metavar=("MAP_FILE", "INI_FILE", "PATCH_MODE=(overwrite|replace|add)"),
)

group_mode.add_argument(
    "--gen-zombie-spawns",
    help="Generate zombie spawnpoint logic for all waypoint IDs 100-300.",
    nargs=2,
    metavar=("MAP_FILE", "SPAWNS_JSON_FILE")
)

group_mode.add_argument(
    "--sort-triggers",
    help="Sort map INI trigger and tag IDs. Will not affect gameplay.",
    nargs=1,
    metavar=("MAP_FILE",))

group_mode.add_argument(
    "--rename",
    help="Rename the map file.",
    nargs=2,
    metavar=("MAP_FILE", "NAME")
)

group_mode.add_argument(
    "--export-csra2",
    help="For Nuclear Kommando.",
    nargs=1,
    metavar=("MAP_FILE",)
)

# group_mode.add_argument(
#     "--set-author",
#     help="Set the author of the map.",
#     nargs=1,
#     metavar=("MAP_FILE",)
# )


args = parser.parse_args()


#
# Select mode
#
if args.extract_preview:
    print("Extracting preview...")
    map = MapFile()
    map.from_file(args.extract_preview[0])
    preview = map.read_preview()
    preview.save_image(args.extract_preview[1])


elif args.replace_preview:
    print("Replacing preview...")
    preview = PreviewBase()
    preview.from_image(args.replace_preview[1])
    map = MapFile()
    map.from_file(args.replace_preview[0])
    map.set_preview(preview)
    map.save(args.replace_preview[0])


elif args.show_preview:
    print("Displaying preview...")
    map = MapFile()
    map.from_file(args.show_preview[0])
    preview = map.read_preview()
    preview.show()


elif args.merge_ini:

    patch_mode = args.merge_ini[2]
    if not patch_mode in [ "overwrite", "replace", "add" ]:
        parser.error('unrecognized PATCH_MODE "{}", choose between "overwrite", "replace" or "add"'.format(patch_mode))

    pretty_names = { "overwrite": "Overwriting", "replace": "Replacing", "add": "Adding"}
    print("{} ini rules...".format(pretty_names[patch_mode]))

    map = MapFile()
    map.from_file(args.merge_ini[0])
    map.merge(args.merge_ini[1], patch_mode)
    map.save(args.merge_ini[0])


elif args.sort_triggers:
    print("Sorting all IDs...")
    map = MapFile()
    map.from_file(args.sort_triggers[0])
    trigger_sorter = TriggerSorter(map)
    trigger_sorter.sort_triggers()
    map.save(args.sort_triggers[0])


elif args.gen_zombie_spawns:
    print("Generating zombie spawn system...")
    map = MapFile()
    map.from_file(args.gen_zombie_spawns[0])
    gen_zombie_spawns = GenZombieSpawns(map, args.gen_zombie_spawns[1])
    gen_zombie_spawns.generate()
    map.save(args.gen_zombie_spawns[0])


elif args.rename:
    print("Renaming map...")
    map = MapFile()
    map.from_file(args.rename[0])
    map.set_name(args.rename[1])
    map.save(args.rename[0])


elif args.export_csra2:
    print("Exporting map info for csra2.com...")
    map = MapFile()
    map.from_file(args.export_csra2[0])
    exporter = CSRA2Exporter(map)
    exporter.export()