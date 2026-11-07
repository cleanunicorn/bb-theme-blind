# Blind — a readable palette for bb

A custom [bb](https://getbb.app) palette with warm light surfaces, neutral charcoal dark surfaces, clear blue accents, and stronger secondary text. Built for comfortable reading during long work sessions.

- Light and dark modes in one stylesheet.
- **Default bb font sizes** — no size or zoom overrides.
- Bundled Inter and system monospace fonts; no external font downloads.
- Readable prompt placeholders without an extra blue outline inside the composer.
- Native bb focus styling, subdued decorative borders, and standard terminal colors.
- Reduced-motion styling for control transitions and smooth scrolling.

| Role | Light | Dark |
| --- | --- | --- |
| Canvas | `#F7F6F2` | `#232529` |
| Main text | `#282B30` | `#E3E4E6` |
| Accent | `#285EA0` | `#A4C4EE` |
| Secondary text | `#454B54` | `#C5CAD2` |

## Install

Run these commands **on the host running the target bb instance**. The installer uses that instance's `bb theme dir`; it does not assume `~/.bb` or a particular operating system.

Requirements: bb with custom palette support and its CLI on PATH, Git, and Python 3.9 or newer. The bb instance should be running. No Python packages are required.

```sh
git clone https://github.com/cleanunicorn/bb-theme-blind.git
cd bb-theme-blind
python3 install.py
```

On Windows, use `py -3 install.py` instead of `python3 install.py`.

The installer copies `theme.css` into `<bb theme dir>/blind/theme.css`, makes a uniquely named backup if a stylesheet already exists, and runs `bb theme set blind`. Activation applies across open windows of that bb instance. Each client keeps its own light/dark mode setting.

To install without activating:

```sh
python3 install.py --no-activate
```

Then choose **Settings → Appearance → Palette → blind**, or run:

```sh
bb theme set blind
```

If you run several bb instances, first point your `bb` CLI at the intended instance using your normal bb configuration. Run `bb theme dir` to verify its destination. For remote instances, run the installer on the server host where that path exists.

### Manual installation (no Python required)

1. Clone this repository, or obtain its `theme.css`.
2. Run `bb theme dir` on the target bb host.
3. Create a **regular folder** named `blind` inside that directory.
4. Back up an existing `blind/theme.css`, then copy this repository's `theme.css` there.
5. Run `bb theme set blind`.

Use a real folder rather than a symbolic link: bb's Settings palette discovery may skip symlinked folders. If the dropdown was already open, close and reopen Settings.

## Update

From your repository checkout:

```sh
git pull --ff-only
python3 install.py
```

Existing stylesheet backups remain alongside the installed file as `theme-*.css.bak`. You can restore one by copying it over `theme.css` and re-running `bb theme set blind`.

## Remove

First switch to another palette, for example `bb theme set default`. Then remove the `blind` folder from the directory printed by `bb theme dir`. This also removes any installer-created backups in that folder.

## Customize

Edit `theme.css`, then rerun the installer. The `:root, .light` block defines the light palette and shared settings; `.dark` overrides colors for dark mode. bb derives most surfaces and focus colors from the `--canvas`, `--ink`, and `--primary` tokens.

The theme deliberately leaves font sizes and terminal ANSI colors to bb. It also uses bb's fallback syntax-highlighting themes rather than shipping custom code-theme JSON.

## Validation

The palette was visually checked in bb in both modes. Main text against canvas measured approximately **13.13:1 in light mode** and **12.06:1 in dark mode**. The tested main and secondary text tokens against canvas, sidebar, muted, and selected surfaces measured at least **5.39:1**.

These measurements cover the tested token combinations, not every bb component. Component opacity, plugins, syntax highlighting, disabled states, and future bb changes can affect rendered contrast. This is a readability-focused palette, not a claim of full accessibility conformance.

The installer tests use temporary directories and mock only the bb CLI boundary; they do not change your bb settings:

```sh
python3 -m unittest discover -s tests -v
```

## License

MIT — see [LICENSE](LICENSE).
