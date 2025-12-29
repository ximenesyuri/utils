from typed import typed, Str
from utils.mods.json_ import Json

class md:
    @typed
    def get_frontmatter(markdown: Str) -> Json:
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
                except yaml.YAMLError:
                    return {}
                except Exception:
                    return {}
            else:
                return {}
        return {}

    @typed
    def remove_frontmatter(markdown: Str) -> Str:
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

    @typed
    def to_html(markdown: Str) -> Str:
        from utils.mods.lib import lib
        lib.install('markdown')
        from markdown import markdown as markdown_
        return markdown_(markdown)
