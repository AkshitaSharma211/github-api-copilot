import json
subset = json.load(open('data/processed/orgs_teams_users_subset.json'))
for r in subset[:10]:
    print(r['path'])
    