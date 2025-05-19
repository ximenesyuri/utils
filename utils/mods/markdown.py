import yaml
import json

class markdown:
    class frontmatter:
        def to_json(markdown_file_path):
            with open(markdown_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            if content.startswith('---'):
                frontmatter, body = content.split('---', 2)[1:]
                data = yaml.safe_load(frontmatter)
                return json.dumps(data, indent=4)
            else:
                raise ValueError("No frontmatter found")

        def from_json(json_data, markdown_file_path):
            with open(markdown_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            if content.startswith('---'):
                _, body = content.split('---', 2)[1:]
                try:
                    data = json.loads(json_data)
                    yaml_frontmatter = yaml.dump(data, default_flow_style=False, sort_keys=False).strip()
                except:
                    yaml_frontmatter = yaml.dump(json_data, default_flow_style=False, sort_keys=False).strip()

                updated_content = f"---\n{yaml_frontmatter}\n---\n{body}"
                with open(markdown_file_path, 'w', encoding='utf-8') as file:
                    file.write(updated_content)
            else:
                frontmatter = "---\n"
                for key, value in json_data.items():
                    frontmatter = frontmatter + f"{key}: {value}\n"
                frontmatter = frontmatter + "---"
                with open(markdown_file_path, 'w', encoding='utf-8') as file:
                    file.write(frontmatter)
