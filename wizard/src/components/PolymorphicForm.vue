<template>
	<div>
		<polymorphic-field
			v-for="field in fields"
			:key="field.id"
			:field="field"
			:contents="contents">
		</polymorphic-field>
	</div>
</template>

<script>
	import PolymorphicField from './PolymorphicField'

	export default {
		props: ['fields', 'contents'],
		components: { PolymorphicField },
	}
</script>