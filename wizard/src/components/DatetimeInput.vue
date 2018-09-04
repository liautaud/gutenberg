<template>
	<div>
		<b-datepicker
			placeholder="Cliquez pour choisir une date"
			icon="calendar-today"
			v-model="date"
			:readonly="false"
			@input="change">
		</b-datepicker>
		<b-timepicker
			placeholder="Cliquez pour choisir une heure"
			icon="clock"
			v-model="time"
			:readonly="false"
			@input="change">
		</b-timepicker>
	</div>
</template>

<script>
	export default {
		props: ['value'],

		data() {
			if (this.value === null) {
				return { date: null, time: null }
			} else {
				return {
					date: new Date(this.value),
					time: new Date(this.value)
				}
			}
		},

		watch: {
			// value(updated) {
			// 	let datetime = new Date(updated)

			// 	if (this.date != datetime) {
			// 		this.date = datetime
			// 	}

			// 	if (this.time != datetime) {
			// 		this.time = datetime
			// 	}
			// }
		},

		computed: {
			datetime() {
				let dt = new Date(this.date)

				if (this.time) {
					dt.setHours(this.time.getHours())
					dt.setMinutes(this.time.getMinutes())
					dt.setSeconds(this.time.getSeconds())
				}

				return dt
			}
		},

		methods: {
			change() {
				this.$emit('input', this.datetime)
			}
		}
	}
</script>