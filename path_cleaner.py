import json
from rich import print

with open('paths.json') as f:
    paths = json.load(f)

api_descriptions = []
counter = 0

for path, details in paths.items():
    print(f"[bold blue]Path:[/bold blue] {path}")
    api_desc = {}
    api_desc['path'] = path
    for method, method_details in details.items():
        # Skip non-HTTP method keys like 'parameters' at the root level
        if method == 'parameters' or not isinstance(method_details, dict):
            continue
        
        try:
            api_desc['method'] = method
            api_desc['summary'] = method_details.get('summary', 'N/A')
            api_desc['description'] = method_details.get('description', 'N/A')
            api_desc['query_params'] = []
            for parameter_ in method_details.get('parameters', []):
                if parameter_['in'] == 'query':
                    api_desc['query_params'].append({
                        'name': parameter_['name'],
                        'type': parameter_.get('schema', {}).get('type', 'N/A'),
                        'description': parameter_.get('description', 'N/A')
                    })
        except Exception as e:
            print(f"Error processing {path} - {method}: {e}")
    api_descriptions.append(api_desc)
    counter += 1


with open('api_description.json', 'w') as f:
    json.dump(api_descriptions, f, indent=4)

print(f"Processed {counter} paths.")