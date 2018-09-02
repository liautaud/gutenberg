<template>

    <b-tabs type="is-boxed">
        <b-tab-item v-for="(content, i) in value" :label="i">
        	<markdown-input v-model="value[i]"></markdown-input>
        </b-tab-item>
        <b-tab-item icon="plus"></b-tab-item>
    </b-tabs>

<!-- 	<b-select placeholder="Cliquez pour choisir une option" expanded v-model="value">
		<option
			v-for="(name, value) in definition.choices"
			:value="value">
			{{ name }}
		</option>
	</b-select>
 --></template>

<script>
	import MarkdownInput from './MarkdownInput'

	export default {
		components: { MarkdownInput },
		props: {
			value: Array,
		},

		methods: {
			add() {
				// this.$emit('input', this.editor.value())
			},

			remove() {
				// this.$emit('input', this.editor.value())
			}
		}
	}
</script>