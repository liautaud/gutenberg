<template>
	<b-select placeholder="Cliquez pour choisir une option" expanded v-model="value">
		<option
			v-for="(name, value) in definition.choices"
			:value="value">
			{{ name }}
		</option>
	</b-select>
</template>

<script>
	export default {
		props: ['value', 'definition'],
	}
</script>