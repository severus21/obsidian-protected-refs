# Obsidian Sample Plugin

Build project
1. Install NPM dependencies with `npm i`
2. Build the plugin with `npm run dev`
3. (Optional) updates to the Obsidian API run `npm update`

Directory structure 
- `main.ts` is the entry point for the plugin
- build files are written to the root directory
  - `main.js` is the compiled plugin

Use it in Obsidian dev vault
1. Clone this repo into `.obsidian/plugins/your-plugin-name`

Install plugin 
* Manually install the plugin by copying the `main.js`, `styles.css`, `manifest.json` to your vault `VaultFolder/.obsidian/plugins/your-plugin-id/`
* Install or update from a release
```bash
  vault_folder=~/.obsidian/plugins/your-plugin-id
  plugin_version="1.0.1"

  wget https://github.com/severus21/obsidian-protected-refs/archive/refs/tags/v${plugin_version}.tar.gz
  tar -xvf v${plugin_version}.tar.gz

  if [ ! -d "$vault_folder/.obsidian/plugins" ]; then
    mkdir "$vault_folder/.obsidian/plugins"
  fi

  mv -f v${plugin_version}.tar.gz $vault_folder/.obsidian/plugins/obsidian-protected-refs
  rm -f v${plugin_version}.tar.gz
```

## Releasing new releases

```bash
version="1.0.1" # from manifest.json
git tag -a $version -m "$version"
git push origin $version
```

Then go to Github and change the release status from draft to published.

### Release numbering
- Update your `manifest.json` with your new version number, such as `1.0.1`, and the minimum Obsidian version required for your latest release.
- Update your `versions.json` file with `"new-plugin-version": "minimum-obsidian-version"` so older versions of Obsidian can download an older version of your plugin that's compatible.

> You can simplify the version bump process by running `npm version patch`, `npm version minor` or `npm version major` after updating `minAppVersion` manually in `manifest.json`.
> The command will bump version in `manifest.json` and `package.json`, and add the entry for the new version to `versions.json`