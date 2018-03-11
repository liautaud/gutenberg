<template>
	<b-field :label="field.name" horizontal>
		<component :is="components[field.type]"
			:required="field.required"
			v-model="contents[field.id]">
		</component>
	</b-field>
</template>

<script>
	const Swatches = window.VueSwatches.default

	import MarkdownInput from './MarkdownInput'
	import DatetimeInput from './DatetimeInput'

	export default {
		props: ['field', 'contents'],

		computed: {
			components() {
				return {
					'text': 'b-input',
					'markdown': MarkdownInput,
					'datetime': DatetimeInput,
					'color': Swatches,
					'image': 'b-input',    // TODO(liautaud)
					'choice': 'b-input',   // TODO(liautaud)
					'list': 'b-input',     // TODO(liautaud)
				}
			}
		}
	}
</script>