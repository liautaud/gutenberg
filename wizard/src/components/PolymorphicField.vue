<template>
	<b-field :label="field.name" horizontal>
		<!-- Text field -->
		<b-input
			v-if="field.type == 'text'"
			:required="field.required"
			v-model="contents[field.id]">
		</b-input>

		<!-- Markdown field -->
		<markdown-editor
			v-else-if="field.type == 'markdown'"
			:required="field.required"
			v-model="contents[field.id]">
		</markdown-editor>

		<!-- TODO(liautaud): Implement more field types. -->
	</b-field>
</template>

<script>
	import MarkdownEditor from './MarkdownEditor'

	export default {
		props: ['field', 'contents'],
		components: { MarkdownEditor }
	}
</script>