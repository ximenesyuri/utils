from typed import typed, Str, Json
from typed.examples import Markdown

class md:
    @typed
    def get_frontmatter(markdown: Markdown) -> Json:
        if markdown.startswith('---'):
            parts = markdown.split('---', 2)
            if len(parts) >= 3:
                frontmatter_raw = parts[1].strip()
                if not frontmatter_raw:
                    return {}
                try:
                    from utils.mods.lib import lib
                    lib.install('pyyaml')
                    import yaml
                    data = yaml.safe_load(frontmatter_raw)
                    if data is None:
                        return {}
                    return data
                except yaml.YAMLError as e:
                    return {}
                except Exception as e:
                    return {}
            else:
                return {}
        return {}

    @typed
    def remove_frontmatter(markdown: Markdown) -> Str:
        if markdown.startswith('---'):
            parts = markdown.split('---', 2)
            if len(parts) == 3:
                remaining_content = parts[2]
                if remaining_content.startswith('\n'):
                    return remaining_content[1:]
                return remaining_content
            else:
                if len(parts) == 2 and parts[0] == '' and parts[1] == '':
                    return ""
                return markdown
        return markdown
