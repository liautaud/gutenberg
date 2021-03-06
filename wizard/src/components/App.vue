<template>
	<div class="page">
		<header class="section">
			<div class="container">
				<h1 class="title">
					<img src="/static/logo.png" alt="Gutenberg">
				</h1>
				<h2 class="subtitle">
					Générateur de diffusions associatives.
				</h2>
			</div>
		</header>

		<b-loading :active="!templates || !saves"></b-loading>

		<b-modal :active.sync="previewActive" :width="1100">
			<iframe class="preview" frameborder="0" ref="previewFrame"></iframe>
		</b-modal>

		<b-modal :active.sync="htmlActive" :width="1100">
			<div class="box">
				<h3 class="title is-4">Code source HTML</h3>
				<h4 class="subtitle">À copier/coller dans le webmail.</h4>
				<pre>{{ htmlContent }}</pre>
			</div>
		</b-modal>

		<transition name="fade" mode="out-in">
			<div class="container" v-if="contents === null" key="menu">
				<div class="columns">
					<div class="column">
						<section class="box">
							<b-field>
								<b-select
									v-model="selectedTemplate"
									placeholder="Créer une nouvelle diffusion"
									size="is-medium"
									expanded>
									<option
										v-for="template, name in templates"
										:key="name"
										:value="name">
										{{ template.title }}
									</option>
								</b-select>
								<p class="control">
									<button class="button is-primary is-medium" @click="create">Créer</button>
								</p>
							</b-field>
						</section>
					</div>

					<div class="column">
						<section class="box">
							<b-field>
								<b-select
									v-model="selectedSave"
									placeholder="Charger une diffusion précédente"
									size="is-medium"
									expanded>
									<option
										v-for="save, name in saves"
										:key="name"
										:value="name">
										{{ save.title }}
									</option>
								</b-select>
								<p class="control">
									<button class="button is-primary is-medium" @click="load">Charger</button>
								</p>
							</b-field>
						</section>
					</div>
				</div>
			</div>

			<div class="container" v-else key="editor">
				<section class="box level">
					<div class="level-left" v-if="selectedSave">
						<p>Vous modifiez la diffusion <strong>{{ saves[selectedSave].title }}</strong>.</p>
					</div>
					<div class="level-left" v-else-if="selectedTemplate">
						<p>Vous écrivez une nouvelle diffusion selon le modèle <strong>{{ templates[selectedTemplate].title }}</strong>.</p>
					</div>
					<div class="level-right">
						<a class="button is-danger is-outlined" @click="reset">Annuler</a>
					</div>
				</section>

				<section class="box">
					<b-field label="Nom de l'auteurice" horizontal>
						<b-input v-model="contents.author" required></b-input>
					</b-field>
					<b-field label="Nom de la diffusion" horizontal>
						<b-input v-model="contents.title" required></b-input>
					</b-field>
					<b-field label="Date de la diffusion" horizontal>
						<b-datepicker
							v-model="contents.date"
							placeholder="Cliquez pour choisir une date"
							icon="calendar-today">
						</b-datepicker>
					</b-field>

					<hr>

					<polymorphic-form
						:fields="rootFields"
						:contents="contents">
					</polymorphic-form>

					<hr>

					<b-collapse class="panel" v-for="section, id in contents.sections">
						<div slot="trigger" class="panel-heading level">
							<div class="level-left">
								<strong>{{ section.title }}</strong>
							</div>
							<div class="level-right">
								<a class="button is-medium" @click="deleteSection(id)">
									<b-icon icon="delete"></b-icon>
								</a>
							</div>
						</div>
						<div class="panel-block">
							<div class="container is-v-padded">
								<polymorphic-form
									:fields="sectionFields"
									:contents="contents.sections[id]">
								</polymorphic-form>
							</div>
						</div>
					</b-collapse>

					<b-field grouped position="is-right">
						<p class="control">
							<button class="button is-medium" @click="addSection">
								<span>Ajouter une section</span>
								<b-icon icon="plus"></b-icon>
							</button>
						</p>
					</b-field>

					<hr>

					<b-field grouped position="is-centered">
						<p class="control">
							<button class="button is-primary is-medium is-outlined"
								@click="preview">Prévisualiser</button>
						</p>
						<p class="control">
							<button class="button is-primary is-medium is-outlined"
								@click="html">Récupérer le HTML</button>
						</p>
						<p class="control">
							<button class="button is-primary is-medium"
								@click="save">Sauvegarder</button>
						</p>
					</b-field>
				</section>
			</div>
		</transition>
	</div>
</template>

<script>
	import PolymorphicForm from './PolymorphicForm'

	/**
	 * Build a promise that sends a JSON-serialized object to
	 * a given URL using POST, and returns the response text.
	 */
	const postJson = (url, data) =>
		fetch(url, {
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			method: 'POST',
			body: JSON.stringify(data)
		})

	/**
	 * Fetches the list of templates and saves from the server.
	 */
	const fetchTemplatesAndSaves = (vm) =>
		fetch('/templates')
			.then(res => res.json())
			.then(data => {
				vm.templates = data
				return fetch('/saves')
			})
			.then(res => res.json())
			.then(data => {
				castSaves(data, vm.templates)
				vm.saves = data
			})

	/**
	 * The fields which are defined implicitely for every template.
	 */
	const metaFields = [
		{ id: 'title', type: 'text' },
		{ id: 'author', type: 'text' },
		{ id: 'date', type: 'date' },
	]

	/**
	 * Cast the data of a field to match the type expected by its template.
	 */
	const castField = (container, field) => {
		if (!field.required &&
			typeof container[field.id] == 'undefined') {
			container[field.id] = null
		}

		if (field.type == 'date' && container[field.id] !== null) {
			container[field.id] = new Date(container[field.id])
		}

		if (field.type == 'list' && container[field.id] == null) {
			container[field.id] = []
		}
	}

	/**
	 * Cast the data in a save to match the type expected by its template.
	 */
	const castSave = (save, template) => {
		for (let field of metaFields)
			castField(save, field)

		for (let field of template.root)
			castField(save, field)

		if (!save.sections)
			save.sections = []

		save.sections.forEach(section => {
			for (let field of template.sections)
				castField(section, field)
		})
	}

	/**
	 * Apply the castSave function to a set of saves and templates.
	 */
	const castSaves = (saves, templates) => {
		for (let id in saves) {
			let save = saves[id]
			let template = templates[save.template]

			castSave(save, template)
		}
	}

	/**
	 * Generate an empty save for a given template.
	 */
	const emptySave = (template) => {
		let save = {}

		for (let field of metaFields)
			save[field.id] = null

		for (let field of template.root)
			save[field.id] = null

		save.sections = []

		castSave(save, template)

		save.template = template.id
		return save
	}

	export default {
		components: { PolymorphicForm },

		data: () => ({
			templates: null,
			saves: null,

			selectedTemplate: null,
			selectedSave: null,

			contents: null,

			previewActive: false,
			htmlActive: false,
			htmlContent: null,
		}),

		computed: {
			rootFields() {
				return this.templates[this.selectedTemplate].root
			},

			// Return the fields which are nested in a section.
			sectionFields() {
				return this.templates[this.selectedTemplate].sections
			}
		},

		mounted() {
			fetchTemplatesAndSaves(this)
		},

		methods: {
			create() {
				// The value of this.selectedTemplate is given by the dropdown.
				this.selectedSave = null
				this.contents = emptySave(this.templates[this.selectedTemplate])
			},

			load() {
				// The value of this.selectedSave is given by the dropdown.
				this.selectedTemplate = this.saves[this.selectedSave].template
				this.contents = this.saves[this.selectedSave]
			},

			reset() {
				this.$dialog.confirm({
					title: 'Effacer les modifications',
					message: 'Êtes-vous sûr de vouloir effacer les modifications ? ' +
							 'Tous les changements effectués depuis la dernière ' +
							 'sauvegarde seront perdus.',
					cancelText: 'Annuler',
					confirmText: 'Effacer',
					type: 'is-danger',
					hasIcon: true,
					onConfirm: () => {
						this.selectedTemplate = null
						this.selectedSave = null
						this.contents = null
					}
				})
			},

			addSection() {
				let section = {}

				for (let field of this.templates[this.selectedTemplate].sections)
					castField(section, field)

				this.contents.sections.push(section)
			},

			deleteSection(id) {
				this.contents.sections.splice(id, 1)
			},

			preview() {
				this.previewActive = true

				postJson('/render', this.contents)
					.then(res => res.text())
					.then(text => {
						let previewDocument = (
							this.$refs.previewFrame.contentDocument ||
							this.$refs.previewFrame.contentWindow.document)

						previewDocument
							.getElementsByTagName('html')[0]
							.innerHTML = text
					})
			},

			html() {
				this.htmlActive = true

				postJson('/render', this.contents)
					.then(res => res.text())
					.then(text => {
						// We use the DOM to isolate the contents of the body,
						// because we want the user to copy that to the webmail
						// instead of the entire HTML output.
						let virtualDom = document.createElement('html')
						virtualDom.innerHTML = text

						let virtualBody = virtualDom.getElementsByTagName('body')[0]
						this.htmlContent = virtualBody.innerHTML
					})
			},

			save() {
				// FIXME: This is not very pretty.
				let target = '/save'
				if (this.selectedSave) {
					target += '?name=' + encodeURIComponent(this.selectedSave)
				}

				postJson(target, this.contents)
					.then(response => {
						if (!response.ok) {
							throw Error()
						}

						return response.json()
					})
					.then(data => {
						fetchTemplatesAndSaves(this)
							.then(_ => {
								this.selectedSave = data.name

								this.$toast.open({
									message: "La diffusion a bien été sauvegardée !",
									type: 'is-success'
								})
							})
					})
					.catch(error => {
						this.$toast.open({
							message: "La diffusion n'a pas pu être sauvegardée !",
							type: 'is-danger'
						})
					})
			}
		}
	}
</script>
