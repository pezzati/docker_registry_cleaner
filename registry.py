import json
import requests

from datetime import datetime, timedelta

class Registry:
    BASE_URL = 'http://your.registry.url'
    API_REP_LIST = '/v2/_catalog'
    API_TAG_LIST = '/v2/{}/tags/list'
    API_DIGEST = '/v2/{}/manifests/{}'
    API_DELETE = '/v2/{}/manifests/{}'
    API_TAG_INFO = '/v2/{}/manifests/{}'
    repositories = {}

    def __init__(self, base_url):
        self.BASE_URL = base_url
        self.API_REP_LIST = self.BASE_URL + '/v2/_catalog'
        self.API_TAG_LIST = self.BASE_URL + '/v2/{}/tags/list'
        self.API_DIGEST = self.BASE_URL + '/v2/{}/manifests/{}'
        self.API_DELETE = self.BASE_URL + '/v2/{}/manifests/{}'
        self.API_TAG_INFO = self.BASE_URL + '/v2/{}/manifests/{}'

    def get_repositories(self):
        response = requests.get(self.API_REP_LIST)
        if response.status_code != 200:
            print('Can not get the repositories')
            return
        data = json.loads(response.content)
        self.repositories = {x: {} for x in data['repositories']}

        print('select repository')
        for i in range(len(self.repositories)):
            print('{}) {}'.format(i + 1, data['repositories'][i]))

    def get_tag_list(self, image):
        url = self.API_TAG_LIST.format(image)
        #url = 'http://registry.mediaad:5000/v2/' + image + '/tags/list'
        response = requests.get(url)
        if response.status_code != 200:
            print('CAN NOT FIND')
            return
        tags = json.loads(response.content)['tags']

        self.repositories[image]['tags'] = {x: {} for x in tags}
        for tag in self.repositories[image]['tags']:
            try:
                self.repositories[image]['tags'][tag]['created_date'] = self.get_tag_info(image, tag)
            except:
                pass

        l = self._sort_by_date(self.repositories[image]['tags'])
        for i in range(len(l)):
            print('{}) {} \t {}'.format(i + 1, l[i][0], l[i][1]))

    def _sort_by_date(self, dictionary):
        d = sorted(dictionary, key=lambda x: (dictionary[x]['created_date']))
        return [(x, dictionary[x]['created_date']) for x in d]

    def delete_until(self, image, n=10):
        url = self.API_TAG_LIST.format(image)
        response = requests.get(url)
        if response.status_code != 200:
            print('CAN NOT FIND')
            return
        tags = json.loads(response.content)['tags']

        self.repositories[image]['tags'] = {x: {} for x in tags}
        for tag in self.repositories[image]['tags']:
            try:
                self.repositories[image]['tags'][tag]['created_date'] = self.get_tag_info(image, tag)
            except:
                pass

        try:
            l = self._sort_by_date(self.repositories[image]['tags'])
        except:
            return
        for i in range(len(l)):
            print('{}) {} \t {}'.format(i + 1, l[i][0], l[i][1]))
        index = 0
        while index < len(l) - n:
            try:
                print('delete: {}'.format(l[index][0]))
                self.delete_tag(image=image, tag=l[index][0])
            except Exception as e:
                print('ERRRORRRR {}'.format(str(e)))
            index += 1

    def get_tag_info(self, image, tag):
        response = requests.get(self.API_TAG_INFO.format(image, tag))
        if response.status_code != 200:
            print('CAN NOT FIND')
            return
        created_str = json.loads(json.loads(response.content)['history'][0]['v1Compatibility'])['created']
        # remove Microsecond
        created_str = created_str.split('.')[0]
        return datetime.strptime(created_str, '%Y-%m-%dT%H:%M:%S')

    def get_digest(self, image, tag):
            headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}

            response = requests.get(self.API_DIGEST.format(image, tag), headers=headers)
            digest = response.headers.get('Docker-Content-Digest')
            return digest

    def delete_tag(self, image, tag):
        digest = self.get_digest(image, tag)
        response = requests.delete(self.API_DELETE.format(image, digest))
        if response.status_code == 202:
            print('Deleted, run below command un machine\n '
                  'docker exec registry bin/registry garbage-collect /etc/docker/registry/config.yml')