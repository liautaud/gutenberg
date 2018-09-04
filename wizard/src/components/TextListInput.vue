<template>
	<section>
		<section v-for="content, i in value" class="box is-clearfix">
			<markdown-input v-model="value[i]"></markdown-input>
			<a class="button is-danger is-pulled-right" style="margin-top: 10px;" @click="remove(i)">
				<b-icon icon="delete" size="is-small"></b-icon>&nbsp;
				Supprimer
			</a>
		</section>
		<a @click="add" class="button is-fullwidth">
			<b-icon icon="plus"></b-icon>&nbsp;
			Ajouter un élément
		</a>
	</section>
</template>

<script>
	import MarkdownInput from './MarkdownInput'

	export default {
		components: { MarkdownInput },
		props: {
			value: Array,
		},

		methods: {
			add() {
				this.value.push("")
			},

			remove(i) {
				this.value.splice(i, 1)
			}
		}
	}
</script>