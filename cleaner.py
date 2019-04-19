from os import environ

from registry import Registry

registry_url = environ.get('REGISTRY_URL', 'default url if you want')
registry = Registry(registry_url)
stop = False
while not stop:
    registry.get_repositories()
    print('To chose image type image name \n'
          'To keep last N on all images type last N\n'
          'To quit type q')
    cmd = input()
    if cmd == 'q':
        stop = True
        break
    elif cmd.startswith('last'):
        try:
            cmd_splited = cmd.split(' ')
            if len(cmd_splited) > 1 and ' ' not in cmd_splited[-1]:
                keep_count = int(cmd_splited[-1])
        except:
            keep_count = 10

        for image in registry.repositories:
            print(image)
            registry.delete_until(image=image, n=keep_count)
        continue
    if cmd not in registry.repositories:
        cmd = list(registry.repositories.keys())[cmd]
    repository = cmd
    while True:
        print('You chose {}, what you wanna do? \n'.format(repository) +
              'To just keep last N type: last N\n' +
              'To back type back\n' +
              'To show tags type tags\n')
        cmd = input("what say you?\n")
        if cmd == 'back':
            break
        elif cmd == 'tags':
            pass
        elif cmd.startswith('last'):
            registry.delete_until(image=repository)
            continue
        registry.get_tag_list(repository)

        print("To delete a single tag type <tag_name>\n"
              + "To just keep one tag type: exc <tag_name>\n"
              + "To delete by pattern: pat <tag_pattern> \n"
              + "To keep by pattern: pat exc <tag_pattern> \n"
              + "To delete by date: before -2 (deletes tags older than 2 days)\n"
              + "To just keep recent: last N\n")

        cmd = input("what say you?\n")
        if cmd == 'q':
            stop = True
            break
        if cmd == 'reset':
            continue
        if cmd == 'back':
            break
        if cmd.startswith('exc'):
            target_tag = cmd.split(' ')[-1]
            deletes = [x for x in registry.repositories[repository]['tags'] if x != target_tag]
        if cmd.startswith('before'):
            days = int(cmd.split(' ')[-1])
            if days < 0:
                days = -days
            if days == 0:
                continue

            bound = datetime.now() - timedelta(days=days)
            tags = registry.repositories[repository]['tags']
            deletes = [x for x in tags if tags[x]['created_date'] < bound]

        # print(deletes)
        for delete in deletes:
            if delete == 'latest':
                continue
            # print(delete)
            registry.delete_tag(repository, delete)
