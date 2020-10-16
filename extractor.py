import gzip
import json
import sys

def make_summary(statpkgfile):
    data = json.load(gzip.open(statpkgfile))
    patchdata = []
    for p in data['patchsets']:
        assert p['version'] == '1.0.0'
        d = {
            'metadata': p['metadata'],
            'version': p['version'],
            'npatches': len(p['patches'])
        }
        patchdata.append(d)

    w = data['workspace']
    assert w['version'] == '1.0.0'

    nbins = {o['name']:len(o['data']) for o in w['observations']}

    workspace_data = {
        'version': w['version'],
        'channels': [
            {
                'name': c['name'],
                'nbins': nbins[c['name']],
                'samples': [
                    {'name': s['name']} for s in c['samples']
                ]
            } for c in  w['channels']
        ],
    }
    summary = {
        'description': data['description'],
        'patchsets': patchdata,
        'workspace': workspace_data
    }
    print(json.dumps(summary))

make_summary(sys.argv[1])