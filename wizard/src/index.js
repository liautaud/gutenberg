import App from './components/App'

Vue.use(Buefy.default)

// Instanciate the App component and bind it to
// the <main> tag of page.
let app = new Vue({
	el: 'main',
	render: h => h(App)
})