import { App, Editor, MarkdownView, Modal, Notice, Plugin, PluginSettingTab, Setting, RequestUrlParam} from 'obsidian';
//import request from 'request';

import { MarkdownView, MarkdownRenderer } from 'obsidian';



  
  

// Remember to rename these classes and interfaces!

interface MyPluginSettings {
	host: string;
}

const DEFAULT_SETTINGS: Partial<MyPluginSettings> = {
	host: 'http://localhost:8800',
}


export class MyPluginSettingTab extends PluginSettingTab {
  plugin: MyPlugin;

  constructor(app: App, plugin: MyPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    let { containerEl } = this;

    containerEl.empty();

    new Setting(containerEl)
      .setName("Host")
      .setDesc("Url of the server to send the encrypted text for decryption.")
      .addText((text) =>
        text
          .setPlaceholder("url")
          .setValue(this.plugin.settings.host)
          .onChange(async (value) => {
            this.plugin.settings.host = value;
            await this.plugin.saveSettings();
          })
      );
  }
}

export default class MyPlugin extends Plugin {
	settings: MyPluginSettings;

	processTextSection = async (el: HTMLElement, ctx: MarkdownPostProcessorContext) => {
		const protected_spans = el.querySelectorAll("span.inline-protected");

		for (let index = 0; index < protected_spans.length; index++) {
			const protected_span = protected_spans.item(index);
			const text = protected_span.innerText.trim();
			//alert(text);

			// Make the POST request			
			try{
				{
					fetch(this.settings.host+'/decrypt', {
						method: 'POST', 
						mode: 'cors',
						body: JSON.stringify(
							{'to_decrypt': text}
						), 
						headers:{
						    "Content-Type": "application/json",
						},
					})
						.then(response => response.json())
						.then(data => {
							protected_span.setText(data['raw_string']);
						}
						)
						.catch(err => console.error(err));
				}
			} catch (error){
				console.error('error in execution', error);
			}
		}
	};

	async onload() {
		await this.loadSettings();
		this.addSettingTab(new MyPluginSettingTab(this.app, this));

		this.registerMarkdownPostProcessor(this.processTextSection);
	}

	async loadSettings() {
		this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
	}

	async saveSettings() {
		await this.saveData(this.settings);
	}
}