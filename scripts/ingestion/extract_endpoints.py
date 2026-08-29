import json

with open('/Users/akshitasharma/rest-api-description/descriptions/api.github.com/dereferenced/api.github.com.deref.json') as f:
    data = json.load(f)

records = []

for path, path_obj in data['paths'].items():
    for method, op in path_obj.items():
        # 'op' is exactly the same kind of dict you already explored
        # for GET /repos/{owner}/{repo}/issues/{issue_number}.
        # Same keys: summary, description, parameters, responses, externalDocs

        record = {
            'path': path,
            'method': method,
            'summary': op['summary'],
            'description': op.get('description'),
            'externalDocs': op.get('externalDocs', {}).get('url'),
                        'parameters': [
                {
                    'name': param.get('name'),
                    'in': param.get('in'),
                    'description': param.get('description')
                }
                for param in op.get('parameters', [])
            ],
            'responses': {
                str(status_code): resp.get('description')
                for status_code, resp in op.get('responses', {}).items()
            }
        }
        records.append(record)

print(f"Total records: {len(records)}")
print(records[0])  # sanity check on the first one

with open('../data/endpoints.json', 'w') as f:
    json.dump(records, f, indent=2)