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
* Make a release
  * 

## Releasing new releases

- Update your `manifest.json` with your new version number, such as `1.0.1`, and the minimum Obsidian version required for your latest release.
- Update your `versions.json` file with `"new-plugin-version": "minimum-obsidian-version"` so older versions of Obsidian can download an older version of your plugin that's compatible.
- Create new GitHub release using your new version number as the "Tag version". Use the exact version number, don't include a prefix `v`. See here for an example: https://github.com/obsidianmd/obsidian-sample-plugin/releases
- Upload the files `manifest.json`, `main.js`, `styles.css` as binary attachments. Note: The manifest.json file must be in two places, first the root path of your repository and also in the release.
- Publish the release.

> You can simplify the version bump process by running `npm version patch`, `npm version minor` or `npm version major` after updating `minAppVersion` manually in `manifest.json`.
> The command will bump version in `manifest.json` and `package.json`, and add the entry for the new version to `versions.json`