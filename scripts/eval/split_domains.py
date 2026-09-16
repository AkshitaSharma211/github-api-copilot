import json

records = json.load(open('data/processed/endpoints.json'))

domains = {
    'issues': '/issues',
    'pulls': '/pulls',
    'repos_contents': '/contents',
    'actions': '/actions',
    'git_database': '/git/',
    'orgs_membership': '/orgs/{org}/members',
    'teams': '/orgs/{org}/teams',
    'collaborators': '/collaborators',
    'search': '/search',
}

used_paths = set()
for name, path_fragment in domains.items():
    subset = [r for r in records if path_fragment in r['path'] and r['path'] not in used_paths]
    used_paths.update(r['path'] for r in subset)
    json.dump(subset, open(f'data/processed/{name}_subset.json', 'w'), indent=2)
    print(f"{name}: {len(subset)} endpoints")