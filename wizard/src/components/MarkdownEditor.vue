<template>
	<textarea ref="editor"></textarea>
</template>

<script>
	export default {
		props: ['value'],

		data() {
			return { editor: null }
		},

		mounted() {
			this.editor = new SimpleMDE({
				element: this.$refs.editor,
				forceSync: true,
				spellChecker: false,
				initialValue: this.value
			})

			this.editor.codemirror.on('change', _ => {
				this.$emit('input', this.editor.value())
			})
		},

		destroyed() {
			this.editor.toTextArea()
			this.editor = null
		},
	}
</script>