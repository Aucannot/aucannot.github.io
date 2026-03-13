# Chirpy Starter

[![Gem Version](https://img.shields.io/gem/v/jekyll-theme-chirpy)][gem]&nbsp;
[![GitHub license](https://img.shields.io/github/license/cotes2020/chirpy-starter.svg?color=blue)][mit]

When installing the [**Chirpy**][chirpy] theme through [RubyGems.org][gem], Jekyll can only read files in the folders
`_data`, `_layouts`, `_includes`, `_sass` and `assets`, as well as a small part of options of the `_config.yml` file
from the theme's gem. If you have ever installed this theme gem, you can use the command
`bundle info --path jekyll-theme-chirpy` to locate these files.

The Jekyll team claims that this is to leave the ball in the user’s court, but this also results in users not being
able to enjoy the out-of-the-box experience when using feature-rich themes.

To fully use all the features of **Chirpy**, you need to copy the other critical files from the theme's gem to your
Jekyll site. The following is a list of targets:

```shell
.
├── _config.yml
├── _plugins
├── _tabs
└── index.html
```

To save you time, and also in case you lose some files while copying, we extract those files/configurations of the
latest version of the **Chirpy** theme and the [CD][CD] workflow to here, so that you can start writing in minutes.

## Usage

Check out the [theme's docs](https://github.com/cotes2020/jekyll-theme-chirpy/wiki).

## Skill 安装与使用（AI Auto Note）

仓库内置了一个用于自动沉淀学习笔记的 skill：`skills/ai-auto-note-publisher`。

如果你希望在 Codex 中全局复用，可安装到 `$CODEX_HOME/skills`：

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R skills/ai-auto-note-publisher "$CODEX_HOME/skills/"
```

如果你希望在 Claude Code 中复用，可安装到 `~/.claude/skills`：

```bash
mkdir -p ~/.claude/skills
cp -R skills/ai-auto-note-publisher ~/.claude/skills/
```

安装后，在需要时触发该 skill，并通过以下命令生成笔记：

```bash
python3 skills/ai-auto-note-publisher/scripts/create_ai_auto_note.py \
  --title "你的学习主题" \
  --input tmp/notes.txt \
  --repo-root .
```

可选：如果你要覆盖自动分类，可传 `--subcategory`（例如 `rag`、`agents`、`general`）。

生成并提交后，如需自动推送 PR 到本仓库（需要已安装并登录 `gh`）：

```bash
cat > tmp/pr-body.md <<'EOF'
## Summary
- add ai auto notes
EOF

bash skills/ai-auto-note-publisher/scripts/push_note_pr.sh \
  --branch feat/ai-auto-note-2026-03-12 \
  --title "feat: add ai auto notes" \
  --body-file tmp/pr-body.md
```

## Contributing

This repository is automatically updated with new releases from the theme repository. If you encounter any issues or want to contribute to its improvement, please visit the [theme repository][chirpy] to provide feedback.

## License

This work is published under [MIT][mit] License.

[gem]: https://rubygems.org/gems/jekyll-theme-chirpy
[chirpy]: https://github.com/cotes2020/jekyll-theme-chirpy/
[CD]: https://en.wikipedia.org/wiki/Continuous_deployment
[mit]: https://github.com/cotes2020/chirpy-starter/blob/master/LICENSE
