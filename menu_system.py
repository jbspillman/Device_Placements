import argparse
import os
import json
import itertools
import more_itertools as mit


rules_folder = os.path.join("rules")
os.makedirs(rules_folder, exist_ok=True)
configurations_path = os.path.join(rules_folder, "configs.json")
all_builds_path = os.path.join(rules_folder, "all_builds_path.json")


def nth(iterable, n, default=None):
    return next(itertools.islice(iterable, n, None), default)


def display_selections_menu(builds_data):

    def s_region():
        """ REGIONAL SELECTION """
        print("#### SELECT REGION NUMBER ####")
        region_choices = []
        for build in builds_data:
            region = build["region"]
            if region not in region_choices:
                region_choices.append(region)
        region_choices.append("Quit.")
        region_selection = 0
        for region in region_choices:
            region_selection += 1
            print('[' + str(region_selection) + ']'.ljust(6), region)

        assigned_region = "Quit."
        try:
            the_region = int(input("Region Choice: >> "))
            the_region_item = the_region - 1
            assigned_region = mit.nth(region_choices, the_region_item)
            if assigned_region not in region_choices:
                print("Invalid Choice. Enter one of the menu numbers.")
                s_region()
        except ValueError:
            print("Invalid Choice. Enter one of the menu numbers.")
            s_region()
        if assigned_region == "Quit.":
            print("Exiting...")
            exit(0)
        else:
            return assigned_region

    def s_site(lcl_region):
        """ SITE SELECTION FOR REGION CHOICE """
        print("#### SELECT SITE NUMBER ####")
        region = ""
        site_choices = []
        for item in builds_data:
            region = item["region"]
            if region == lcl_region:
                site_id = item["site_id"]
                site_name = item["site_name"]
                site_choice = site_id + " " + site_name
                if site_choice not in site_choices:
                    site_choices.append(site_choice)

        site_choices.append("Quit.")
        site_selection = 0
        for site_name in site_choices:
            site_selection += 1
            print('[' + str(site_selection) + ']'.ljust(6), site_name)

        assigned_site = "Quit."
        try:
            the_site = int(input("Site Choice: >> "))
            the_site_item = the_site - 1
            assigned_site = mit.nth(site_choices, the_site_item)
            if assigned_site not in site_choices:
                print("Invalid Choice. Enter one of the menu numbers.")
                s_site(region)
        except ValueError:
            print("Invalid Choice. Enter one of the menu numbers.")
            s_site(region)
        if assigned_site == "Quit.":
            print("Exiting...")
            exit(0)
        else:
            return assigned_site

    def s_pattern(lcl_region, lcl_site):
        """ PATTERN SELECTION FOR REGION, SITE CHOICE """
        print("#### SELECT PATTERN NUMBER ####")

        pattern_choices = []
        for item in builds_data:
            region = item["region"]
            if region == lcl_region:
                site_id = item["site_id"]
                site_name = item["site_name"]
                site_choice = site_id + " " + site_name
                if site_choice == lcl_site:
                    pattern_type = item["type"]
                    if pattern_type not in pattern_choices:
                        pattern_choices.append(pattern_type)

        pattern_choices.append("Quit.")
        pattern_selection = 0
        for pattern_name in pattern_choices:
            pattern_selection += 1
            print('[' + str(pattern_selection) + ']'.ljust(6), pattern_name)

        assigned_pattern = "Quit."
        try:
            the_pattern = int(input("Pattern Choice: >> "))
            the_pattern_item = the_pattern - 1
            assigned_pattern = mit.nth(pattern_choices, the_pattern_item)
            if assigned_pattern not in pattern_choices:
                print("Invalid Choice. Enter one of the menu numbers.")
                s_pattern(lcl_region, lcl_site)
        except ValueError:
            print("Invalid Choice. Enter one of the menu numbers.")
            s_pattern(lcl_region, lcl_site)
        if assigned_pattern == "Quit.":
            print("Exiting...")
            exit(0)
        else:
            return assigned_pattern

    def s_stack(lcl_region, lcl_site, lcl_pattern):
        """ STACK SELECTION FOR REGION, SITE, PATTERN CHOICE """
        print("#### SELECT ENVIRONMENT NUMBER ####")
        env_choices = []
        for item in builds_data:
            region = item["region"]
            if region == lcl_region:
                site_id = item["site_id"]
                site_name = item["site_name"]
                site_choice = site_id + " " + site_name
                if site_choice == lcl_site:
                    pattern_type = item["type"]
                    if lcl_pattern == pattern_type:
                        stack_env = item["env"]
                        if stack_env not in env_choices:
                            env_choices.append(stack_env)
        env_choices.append("Quit.")
        env_name_selection = 0
        for env_name in env_choices:
            env_name_selection += 1
            print('[' + str(env_name_selection) + ']'.ljust(6), env_name)

        assigned_env = "Quit."
        try:
            the_env = int(input("Environment Choice: >> "))
            the_env_item = the_env - 1
            assigned_env = mit.nth(env_choices, the_env_item)
            if assigned_env not in env_choices:
                print("Invalid Choice. Enter one of the menu numbers.")
                s_stack(lcl_region, lcl_site, lcl_pattern)
        except ValueError:
            print("Invalid Choice. Enter one of the menu numbers.")
            s_stack(lcl_region, lcl_site, lcl_pattern)
        if assigned_env == "Quit.":
            print("Exiting...")
            exit(0)
        else:
            return assigned_env

    """ Menu System Maybe. """
    selected_region = s_region()
    selected_site = s_site(selected_region)
    selected_pattern = s_pattern(selected_region, selected_site)
    selected_stack = s_stack(selected_region, selected_site, selected_pattern)

    choice_build_key = selected_region + "_" + selected_site + "_" + selected_pattern + "_" + selected_stack
    choice_build_key = str(choice_build_key).upper().replace(" ", "_")
    return choice_build_key


def generate_all_build_keys():
    all_possible_builds = []
    with open(configurations_path, 'r', encoding="utf-8") as file_in:
        configurations = json.loads(file_in.read())
        for region, sites in configurations.items():
            for site_cfg in sites.values():
                for site_info, values in site_cfg.items():
                    site_id = site_info.split(" ")[0]
                    site_name = site_info.split(site_id)[1].lstrip(" ").rstrip(" ").replace(" ", "-")
                    stacks = values["ENVS"]
                    patterns = values["PATTERNS"]
                    for pattern in patterns:
                        for stack in stacks:
                            build_key = region + "_" + site_id + "_" + site_name + "_" + pattern + "_" + stack
                            build_key = str(build_key).upper()
                            info = {
                                "region": region,
                                "site_id": site_id,
                                "site_name": site_name,
                                "type": pattern,
                                "env": stack,
                                "build_key": build_key
                            }
                            if info not in all_possible_builds:
                                all_possible_builds.append(info)

    json_string = json.dumps(all_possible_builds, indent=4, sort_keys=False)
    with open(all_builds_path, "w", encoding="utf-8") as json_out:
        json_out.write(json_string)
    return all_possible_builds


def main():
    parser = argparse.ArgumentParser(description='Generate Cluster Configuration.')
    parser.add_argument('-b', '--build', required=False, help='"a predefined build configuration key"')
    args = parser.parse_args()
    all_builds = generate_all_build_keys()

    available_builds = []
    for item in all_builds:
        b = str(item["build_key"]).upper()
        available_builds.append(b)

    cluster_build_key = args.build
    if cluster_build_key is not None:
        if cluster_build_key not in available_builds:
            print("")
            print("ERROR: You have specified an invalid build key:".ljust(30), cluster_build_key)
            exit(0)
        else:
            print("You have supplied a valid build key:".ljust(30), cluster_build_key)
    else:
        cluster_build_key = display_selections_menu(all_builds)
        print("You have selected build key:".ljust(30), cluster_build_key)


if __name__ == "__main__":
    main()